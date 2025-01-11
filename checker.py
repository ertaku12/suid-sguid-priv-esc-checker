import subprocess
import sys

# Reference list for comparison
reference_suid = """-rwsr-xr-x 1 root root 48128 Jun 16  2024 /usr/sbin/mount.cifs
-rwsr-xr-- 1 root dip 428424 Nov 22 10:27 /usr/sbin/pppd
-rwsr-xr-x 1 root root 146480 Dec 11 04:23 /usr/sbin/mount.nfs
-rwsr-sr-x 1 root root 14672 Nov  6 21:50 /usr/lib/xorg/Xorg.wrap
-rwsr-xr-x 1 root root 18744 Sep 19 04:47 /usr/lib/polkit-1/polkit-agent-helper-1
-rwsr-xr-x 1 root root 494144 Oct 27 09:58 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 15568 Dec 11 15:33 /usr/lib/chromium/chrome-sandbox
-rwsr-xr-- 1 root messagebus 51272 Dec 16 09:26 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 52936 Dec  6 07:51 /usr/bin/chsh
-rwsr-xr-x 1 root root 18680 Jul  2  2024 /usr/bin/rsh-redone-rlogin
-rwsr-xr-x 1 root root 18816 Dec  6 07:35 /usr/bin/newgrp
-rwsr-xr-x 1 root root 118168 Dec  6 07:51 /usr/bin/passwd
-rwsr-xr-- 1 root kismet 158504 Sep 12 00:50 /usr/bin/kismet_cap_linux_bluetooth
-rwsr-xr-x 1 root root 80264 Dec  6 07:35 /usr/bin/su
-rwsr-xr-x 1 root root 30952 Sep 19 04:47 /usr/bin/pkexec
-rwsr-xr-x 1 root root 88568 Dec  6 07:51 /usr/bin/gpasswd
-rwsr-xr-- 1 root kismet 154408 Sep 12 00:50 /usr/bin/kismet_cap_ti_cc_2531
-rwsr-xr-- 1 root kismet 277288 Sep 12 00:50 /usr/bin/kismet_cap_hak5_wifi_coconut
-rwsr-xr-x 1 root root 35128 Sep 21 08:06 /usr/bin/fusermount3
-rwsr-xr-x 1 root root 14848 Jul 12 16:31 /usr/bin/vmware-user-suid-wrapper
-rwsr-xr-x 1 root root 63880 Dec  6 07:35 /usr/bin/mount
-rwsr-xr-x 1 root root 18680 Jul  2  2024 /usr/bin/rsh-redone-rsh
-rwsr-xr-x 1 root root 166848 Oct  5 03:45 /usr/bin/ntfs-3g
-rwsr-xr-- 1 root kismet 154408 Sep 12 00:50 /usr/bin/kismet_cap_ti_cc_2540
-rwsr-xr-- 1 root kismet 150312 Sep 12 00:50 /usr/bin/kismet_cap_ubertooth_one
-rwsr-xr-- 1 root kismet 154408 Sep 12 00:50 /usr/bin/kismet_cap_rz_killerbee
-rwsr-xr-x 1 root root 35200 Dec  6 07:35 /usr/bin/umount
-rwsr-xr-- 1 root kismet 154408 Sep 12 00:50 /usr/bin/kismet_cap_nxp_kw41z
-rwsr-xr-- 1 root kismet 150312 Sep 12 00:50 /usr/bin/kismet_cap_nrf_52840
-rwsr-xr-- 1 root kismet 228680 Sep 12 00:50 /usr/bin/kismet_cap_linux_wifi
-rwsr-xr-x 1 root root 306456 Nov 13 12:08 /usr/bin/sudo
-rwsr-xr-- 1 root kismet 154408 Sep 12 00:50 /usr/bin/kismet_cap_nrf_mousejack
-rwsr-xr-- 1 root kismet 150312 Sep 12 00:50 /usr/bin/kismet_cap_nrf_51822
-rwsr-xr-x 1 root root 70888 Dec  6 07:51 /usr/bin/chfn
-rwsr-xr-x 1 root root 54192 Nov 27 20:07 /usr/share/code/chrome-sandbox
""".strip().splitlines()

reference_sguid = """-rwsr-sr-x 1 root root 14672 Nov  6 21:50 /usr/lib/xorg/Xorg.wrap
""".strip().splitlines()


def find_suid_binaries():
    """Find binaries with SUID permission."""
    command = r"find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Extract only paths from the output
    return [line.split()[-1] for line in result.stdout.strip().splitlines()]


def find_sguid_binaries():
    """Find binaries with SGUID permission."""
    command = r"find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Extract only paths from the output
    return [line.split()[-1] for line in result.stdout.strip().splitlines()]


def find_new_binaries(current_list, reference_list):
    """Find binaries present in current_list but not in reference_list."""
    return [binary for binary in current_list if binary not in reference_list]


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["suid", "sguid"]:
        print("Usage: python3 script.py <suid|sguid>")
        sys.exit(1)

    option = sys.argv[1]

    if option == "suid":
        print("[INFO] Checking SUID binaries...\n")
        current_list = find_suid_binaries()
        reference_list = [line.split()[-1] for line in reference_suid]
    else:  # sguid
        print("[INFO] Checking SGUID binaries...\n")
        current_list = find_sguid_binaries()
        reference_list = [line.split()[-1] for line in reference_sguid]

    print("[INFO] Identifying new binaries...\n")
    new_binaries = find_new_binaries(current_list, reference_list)

    if not new_binaries:
        print("[INFO] No new binaries found.")
    else:
        print("[WARNING] New binaries detected:")
        for binary in new_binaries:
            print("[+]", binary)


if __name__ == "__main__":
    main()
