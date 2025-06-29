# Triple DES Encryption CLI Tool

A professional command-line interface for secure file and text encryption using Triple DES algorithm.

## Features

- **🔒 Secure File Encryption**: Uses Triple DES in CBC mode with proper PKCS7 padding
- **📝 Text Encryption**: Encrypt and decrypt text with base64 encoding
- **🎨 Professional CLI Interface**: Colorized output with formatted success messages
- **🔑 Advanced Key Management**: Secure key generation and storage with unique key IDs
- **📊 Operation History**: SQLite database tracking all encryption/decryption operations
- **⚡ Interactive & Command-Line Modes**: Both menu-driven and direct command support
- **🛡️ Military-Grade Security**: 24-byte Triple DES keys with random initialization vectors
- **💾 Automatic File Handling**: Smart output naming and secure file operations

## Fixed Issues

This project has been updated to fix several critical issues:

✅ **Path Configuration**: Replaced hardcoded absolute paths with relative paths  
✅ **Database Setup**: Fixed database initialization and path consistency  
✅ **Template Structure**: Removed duplicate templates and fixed inheritance  
✅ **Dependencies**: Added proper requirements.txt file  
✅ **Cross-platform Compatibility**: Works on different systems and directories  

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialize the database**:
   ```bash
   python database/db_setup.py
   ```

## Usage

### Quick Start

```bash
# Interactive mode (recommended for beginners)
python encrypt.py

# Or use the main CLI directly
python cli_main.py
```

### Command Line Usage

```bash
# Encrypt a file
python cli_main.py --encrypt --file document.pdf

# Decrypt a file
python cli_main.py --decrypt --file encrypted_document.pdf.bin --key a1b2c3d4e5f6g7h8

# Encrypt text
python cli_main.py --encrypt --text "Hello World"

# Decrypt text
python cli_main.py --decrypt --text "base64_encrypted_text" --key a1b2c3d4e5f6g7h8

# Show operation history
python cli_main.py --history

# List stored keys
python cli_main.py --list-keys
```

### Interactive Mode Features

The interactive mode provides a user-friendly menu system:

1. **🔒 Encrypt File** - Secure file encryption with automatic key generation
2. **🔓 Decrypt File** - File decryption using stored key IDs
3. **📝 Encrypt Text** - Text encryption with optional file output
4. **📖 Decrypt Text** - Text decryption from file or direct input
5. **📊 View History** - Display recent encryption/decryption operations
6. **🔑 List Keys** - Show all stored encryption key IDs
7. **❓ Help** - Comprehensive help and usage information
8. **🚪 Exit** - Clean application exit

## Testing

Run the comprehensive test suite to verify all functionality:

```bash
python test_functionality.py
```

This will test:
- Triple DES encryption/decryption
- Key management (save/load)
- Database operations
- File handling

## Project Structure

```
Triple-DES/
├── src/
│   ├── app.py                    # Main Flask application
│   └── triple_des_example.py     # Triple DES implementation
├── templates/                    # HTML templates
│   ├── base.html                # Base template with navigation
│   ├── index.html               # Home page
│   ├── encryption_tool.html     # Encryption/decryption interface
│   ├── history.html             # Operation history
│   └── about.html               # About page
├── static/
│   └── style.css                # Custom CSS styles
├── database/
│   ├── db_setup.py              # Database initialization
│   └── encryption_history.db    # SQLite database
├── secure_keys/
│   └── secure_keys.json         # Encrypted key storage
├── uploads/                     # File upload directory
├── requirements.txt             # Python dependencies
├── test_functionality.py       # Test suite
└── README.md                    # This file
```

## Security Features

- **Triple DES Encryption**: Military-grade encryption with CBC mode
- **Secure Key Generation**: Cryptographically secure random key generation
- **Key Management**: Keys stored securely with unique identifiers
- **File Security**: Secure filename handling and automatic cleanup
- **Input Validation**: Proper validation of user inputs

## Dependencies

- **Flask**: Web framework
- **Werkzeug**: WSGI utilities and security helpers
- **pycryptodome**: Cryptographic library for Triple DES

## Browser Compatibility

The web interface works with all modern browsers and is fully responsive for mobile devices.

## Development

To run in development mode with debug enabled:

```bash
python src/app.py
```

The application will automatically reload when you make changes to the code.

## 👨‍💻 Author

**bvivek2148**
- GitHub: [@bvivek2148](https://github.com/bvivek2148)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is for educational and demonstration purposes.
