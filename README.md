# Triple DES File Encryption Web Application

A secure web application for encrypting and decrypting files using Triple DES encryption algorithm.

## Features

- **Secure File Encryption**: Uses Triple DES in CBC mode with proper padding
- **Web Interface**: Clean, responsive Bootstrap-based UI
- **Key Management**: Secure key generation and storage with unique key IDs
- **Operation History**: SQLite database tracking all encryption/decryption operations
- **File Handling**: Secure file upload/download with automatic cleanup

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

### Running the Web Application

```bash
python src/app.py
```

The application will start on `http://127.0.0.1:5000`

### Using the Command Line Tool

You can also use the Triple DES cipher directly from command line:

```bash
# Encrypt a file
python src/triple_des_example.py --action encrypt --input myfile.txt --output encrypted.bin

# Decrypt a file
python src/triple_des_example.py --action decrypt --input encrypted.bin --output decrypted.txt --key-name your_key_id

# Encrypt text
python src/triple_des_example.py --action encrypt --input "Hello World" --text

# Decrypt text
python src/triple_des_example.py --action decrypt --input "base64_encrypted_text" --text --key-name your_key_id
```

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

## License

This project is for educational and demonstration purposes.
