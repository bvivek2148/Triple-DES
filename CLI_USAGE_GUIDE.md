# Triple DES CLI Usage Guide

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive mode
python encrypt.py
```

## 🎯 Usage Modes

### 1. Interactive Mode (Recommended)
```bash
python encrypt.py
```

Features a beautiful menu-driven interface with:
- 🔒 File encryption with auto-generated keys
- 🔓 File decryption using stored key IDs
- 📝 Text encryption with optional file output
- 📖 Text decryption from files or direct input
- 📊 Operation history with formatted tables
- 🔑 Key management and listing
- ❓ Comprehensive help system

### 2. Command Line Mode
Direct commands for automation and scripting:

#### File Operations
```bash
# Encrypt a file
python encrypt.py --encrypt --file document.pdf
python encrypt.py --encrypt --file image.jpg --output custom_encrypted.bin

# Decrypt a file
python encrypt.py --decrypt --file encrypted_document.pdf.bin --key a1b2c3d4e5f6g7h8
python encrypt.py --decrypt --file custom_encrypted.bin --key a1b2c3d4e5f6g7h8 --output restored.jpg
```

#### Text Operations
```bash
# Encrypt text (display in terminal)
python encrypt.py --encrypt --text "Secret message"

# Encrypt text to file
python encrypt.py --encrypt --text "Secret message" --output encrypted_text.bin

# Decrypt text
python encrypt.py --decrypt --text "base64_encrypted_string" --key a1b2c3d4e5f6g7h8
```

#### Management Operations
```bash
# View operation history
python encrypt.py --history
python encrypt.py --history --limit 20

# List all stored keys
python encrypt.py --list-keys
```

## 🔐 Security Features

### Encryption Specifications
- **Algorithm**: Triple DES (3DES) in CBC mode
- **Key Size**: 192-bit (24 bytes) with proper parity
- **Block Size**: 64-bit (8 bytes)
- **Padding**: PKCS7 for compatibility
- **IV**: Random 8-byte initialization vector per operation

### Key Management
- **Key Generation**: Cryptographically secure random keys
- **Key Storage**: JSON format in `secure_keys/` directory
- **Key IDs**: 16-character hexadecimal identifiers
- **Key Persistence**: All keys stored for future decryption

## 📊 Output Formats

### Success Messages
The CLI displays professional formatted output boxes:

```
============================================================
                 FILE ENCRYPTION COMPLETED!                 
============================================================
Original file: document.pdf
Encrypted file: encrypted_document.pdf.bin
Key ID: a1b2c3d4e5f6g7h8

IMPORTANT: Save this Key ID to decrypt your file later!
Store it securely - you cannot decrypt without it!
============================================================

ℹ️  Encryption Key: a1b2c3d4e5f6g7h8
```

### History Display
Operations are tracked in a formatted table:

```
📊 OPERATION HISTORY (Last 10 operations)

+----+---------------------------+------------------+-----------------+---------------------+
| ID | Filename                  | Key ID           | Operation       | Timestamp           |
+====+===========================+==================+=================+=====================+
| 24 | document.pdf              | a1b2c3d4e5f6g7h8 | Encryption      | 2025-06-29 16:13:51 |
| 23 | encrypted_document.pdf.bin| a1b2c3d4e5f6g7h8 | Decryption      | 2025-06-29 16:13:30 |
+----+---------------------------+------------------+-----------------+---------------------+
```

## 🛡️ Best Practices

### Security Recommendations
1. **Backup Key IDs**: Store them in a secure password manager
2. **Test Decryption**: Always verify you can decrypt immediately after encryption
3. **Secure Storage**: Keep the `secure_keys/` folder backed up safely
4. **Key Rotation**: Generate new keys for different projects/purposes

### File Handling
1. **Original Files**: The CLI preserves original files during encryption
2. **Output Naming**: Auto-generates logical names (e.g., `encrypted_file.pdf.bin`)
3. **Path Handling**: Supports both relative and absolute file paths
4. **Large Files**: Efficiently handles files of any size

## 🔧 Troubleshooting

### Common Issues
1. **Missing Dependencies**: Run `pip install -r requirements.txt`
2. **File Not Found**: Check file paths and permissions
3. **Invalid Key ID**: Verify the key exists with `--list-keys`
4. **Permission Errors**: Ensure write access to output directories

### Error Messages
The CLI provides clear, colored error messages:
- ❌ Red for errors
- ⚠️ Yellow for warnings  
- ✅ Green for success
- ℹ️ Blue for information

## 📁 Project Structure
```
Triple-DES/
├── encrypt.py              # Quick launcher
├── cli_main.py             # Main CLI application
├── src/
│   └── triple_des_example.py # Encryption engine
├── database/
│   └── encryption_history.db # Operation history
├── secure_keys/
│   └── secure_keys.json    # Encrypted key storage
└── uploads/                # Working directory
```

## 🎨 Features Showcase

- **Professional Interface**: Clean, colorized terminal output
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Flexible Input**: Files, text, stdin/stdout support
- **Smart Defaults**: Automatic output naming and path handling
- **Comprehensive Logging**: Full operation history with timestamps
- **Error Handling**: Graceful error recovery and user feedback
- **Security First**: Military-grade encryption with best practices
