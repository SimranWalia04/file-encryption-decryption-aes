
# CipherSafe — AES File Encryption and Decryption

## Overview
CipherSafe is a Python-based file encryption and decryption application. It provides a command-line interface and a dark navy blue graphical user interface (GUI) to help users protect files using password-based encryption.

## Features
- AES-256-GCM authenticated encryption
- Password-based key derivation using PBKDF2-HMAC-SHA256
- Random salt and nonce for encryption
- File encryption and decryption
- Graphical interface built with Tkinter
- Incorrect-password and modified-file error handling
- Protection against overwriting existing output files

## Technologies Used
- Python
- Tkinter
- `cryptography` library
- AES-256-GCM
- PBKDF2-HMAC-SHA256

## Requirements
- Python 3
- `cryptography` package

## Installation
1. Install Python 3.
2. Open a terminal in the project folder.
3. Install the required package:

   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Graphical Interface
Run:

```bash
python gui.py
```

Choose a file, enter a password, and select Encrypt File or Decrypt File.

### Command-Line Interface
Run:

```bash
python main.py
```

Follow the menu instructions.

## Test File
The `test_files` folder contains a sample text file that can be used to demonstrate encryption and decryption.

## Security Note
Keep your passwords private and use a strong password. Always keep a backup of important original files. This project is intended for educational purposes.

## Author
# CipherSafe – File Encryption and Decryption Using AES

**Project developed by:**
- **Samtajpreet Kaur**
- **[Simranjeet Kaur]**

**Course:** B.Tech – Computer Science and Engineering (Cybersecurity)  
**College:** Guru Nanak Dev Engineering College (GNDEC), Ludhiana  
**Semester:** 5th Semester


