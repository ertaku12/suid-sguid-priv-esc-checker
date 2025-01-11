# suid-sguid-priv-esc-checker
 A Python tool to identify unusual SUID and SGUID binaries in Linux systems for privilege escalation assessments.

## Features
- Checks for **SUID** binaries (`setuid` permission).
- Checks for **SGUID** binaries (`setgid` permission).
- Compares the current state against a predefined reference list.
- Outputs only the binaries that are newly detected and not part of the reference list.

## Usage
Clone the repository and run the script:
```bash
python3 checker.py <suid|sguid>

python3 checker.py suid
```

## License
This project is licensed under the **Apache License 2.0**. See the [`LICENSE`](./LICENSE) file for details.


## Disclaimer
This tool is intended for educational and authorized security testing purposes only. Unauthorized use on systems without explicit permission is strictly prohibited.

