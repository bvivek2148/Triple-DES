# 🔐 Triple DES Encryption CLI Tool

<div align="center">

```
  ████████╗██████╗ ██╗██████╗ ██╗     ███████╗    ██████╗ ███████╗███████╗
  ╚══██╔══╝██╔══██╗██║██╔══██╗██║     ██╔════╝    ██╔══██╗██╔════╝██╔════╝
     ██║   ██████╔╝██║██████╔╝██║     █████╗      ██║  ██║█████╗  ███████╗
     ██║   ██╔══██╗██║██╔═══╝ ██║     ██╔══╝      ██║  ██║██╔══╝  ╚════██║
     ██║   ██║  ██║██║██║     ███████╗███████╗    ██████╔╝███████╗███████║
     ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝╚══════╝    ╚═════╝ ╚══════╝╚══════╝
```

**🛡️ Professional Security Tool for File Encryption**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](README.md)

</div>

---

## 🌟 Overview

A **world-class command-line interface** and **web application** for secure file encryption using the Triple DES algorithm. This professional-grade tool combines military-level security with an intuitive user experience, featuring beautiful animations, comprehensive key management, and enterprise-ready functionality.

## ✨ Key Features

### 🔒 **Security & Encryption**
- **🛡️ Military-Grade Triple DES**: CBC mode with proper PKCS7 padding
- **🔑 Advanced Key Management**: Secure 24-byte key generation with unique IDs
- **🎲 Random Initialization Vectors**: Enhanced security for each operation
- **📊 Operation Tracking**: Complete audit trail with SQLite database
- **🔐 Secure Key Storage**: JSON-based encrypted key management

### 🎨 **Enhanced User Experience**
- **🚀 Beautiful Startup Animation**: ASCII art logo with typing effects
- **⚡ Loading Animations**: Professional progress indicators and spinners
- **🌈 Colorized Output**: Cross-platform color support with fallbacks
- **📱 Responsive Design**: Adapts to terminal width automatically
- **🎯 Interactive Wizards**: Step-by-step file encryption/decryption guides

### 💻 **Dual Interface System**
- **🖥️ Enhanced CLI Interface**: Professional terminal-based operations
- **🌐 Web Application**: Bootstrap-based responsive web interface
- **📋 Menu-Driven Navigation**: Intuitive interactive mode
- **⌨️ Command-Line Support**: Direct commands for automation and scripting

### 📂 **File Management**
- **📁 Organized Storage**: Dedicated `encrypted_decrypted_files` directory
- **🏷️ Smart Naming**: Automatic `decrypted_filename.extension` convention
- **🔍 Intelligent File Detection**: Auto-search in organized directories
- **💾 Secure File Handling**: Automatic cleanup and path management

## 🚀 Quick Start

### 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/bvivek2148/Triple-DES.git
   cd Triple-DES
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database** (Optional - auto-created on first run)
   ```bash
   python database/db_setup.py
   ```

4. **Launch the Application**
   ```bash
   # Enhanced CLI with animations (Recommended)
   python encrypt.py

   # Web interface
   python src/app.py
   ```

### ⚡ Instant Usage

```bash
# 🔒 Encrypt a file
python encrypt.py --encrypt --file document.pdf

# 🔓 Decrypt a file
python encrypt.py --decrypt --file encrypted_document.pdf.bin --key a1b2c3d4e5f6g7h8

# 📊 View operation history
python encrypt.py --history

# 🔑 List all stored keys
python encrypt.py --list-keys
```

## 💻 Usage Guide

### 🎯 Interactive Mode (Recommended)

Launch the enhanced CLI with beautiful animations:

```bash
python encrypt.py
```

**Features:**
- 🎨 **Stunning ASCII Art Logo** with typing animation
- 🎯 **Interactive File Wizards** with step-by-step guidance
- ⚡ **Real-time Progress Indicators** for all operations
- 📊 **Enhanced Data Visualization** with formatted tables
- 🛡️ **Professional Error Handling** with clear recovery options

### ⌨️ Command Line Mode

Direct commands for automation and scripting:

#### 📁 File Operations
```bash
# Encrypt files with auto-generated keys
python encrypt.py --encrypt --file document.pdf
python encrypt.py --encrypt --file image.jpg --output custom_name.bin

# Decrypt files using stored Key IDs
python encrypt.py --decrypt --file encrypted_document.pdf.bin --key a1b2c3d4e5f6g7h8
python encrypt.py --decrypt --file custom_name.bin --key a1b2c3d4e5f6g7h8 --output restored.jpg
```

#### 📊 Management Operations
```bash
# View operation history with formatted tables
python encrypt.py --history
python encrypt.py --history --limit 20

# List all stored keys with associated files
python encrypt.py --list-keys

# Get comprehensive help
python encrypt.py --help
```

### 🌐 Web Interface

Launch the responsive web application:

```bash
python src/app.py
```

**Access:** `http://127.0.0.1:5000`

**Features:**
- 📱 **Responsive Bootstrap Design** for all devices
- 🔒 **Drag & Drop File Upload** with real-time feedback
- 📊 **Interactive History Management** with search and filters
- 💻 **CLI Guide Integration** with copy-paste commands
- 🎨 **Professional UI/UX** with modern design patterns

### 📋 Enhanced Interactive Menu

```
📋 MAIN MENU

1. 🔒 Encrypt File      - Secure file encryption with auto-generated keys
2. 🔓 Decrypt File      - Decrypt files using stored key IDs
3. 📊 View History      - Display recent operations with clear option
4. 🔑 List Keys         - Show keys with filenames and clear option
5. ❓ Help              - Comprehensive help and usage information
6. 🚪 Exit              - Exit the application safely
```

## 🏗️ Project Architecture

### 📁 Directory Structure

```
Triple-DES/
├── 🚀 CLI Interface
│   ├── encrypt.py                    # Quick launcher script
│   ├── cli_main.py                   # Enhanced CLI application
│   └── CLI_USAGE_GUIDE.md           # Comprehensive CLI documentation
│
├── 🌐 Web Application
│   ├── src/
│   │   ├── app.py                   # Flask web application
│   │   └── triple_des_example.py    # Core encryption engine
│   ├── templates/                   # Jinja2 HTML templates
│   │   ├── base.html               # Base template with navigation
│   │   ├── index.html              # Dashboard homepage
│   │   ├── encryption_tool.html    # File encryption interface
│   │   ├── history.html            # Operation history viewer
│   │   ├── cli_guide.html          # CLI integration guide
│   │   └── about.html              # Project information
│   └── static/
│       └── style.css               # Custom CSS styling
│
├── 💾 Data & Storage
│   ├── database/
│   │   ├── db_setup.py             # Database initialization
│   │   └── encryption_history.db   # SQLite operation history
│   ├── secure_keys/
│   │   └── secure_keys.json        # Encrypted key storage
│   ├── encrypted_decrypted_files/  # Organized file storage
│   │   ├── encrypted_*.bin         # All encrypted files
│   │   └── decrypted_*.*           # All decrypted files
│   └── uploads/                    # Web upload working directory
│
├── 📚 Documentation & Testing
│   ├── requirements.txt            # Python dependencies
│   ├── test_functionality.py      # Comprehensive test suite
│   ├── CLI_IMPROVEMENTS_SUMMARY.md # Enhancement documentation
│   └── README.md                   # This comprehensive guide
```

### 🔧 Core Components

#### 🛡️ **Encryption Engine** (`triple_des_example.py`)
- **Triple DES Implementation**: CBC mode with PKCS7 padding
- **Key Management**: Secure generation, storage, and retrieval
- **File Operations**: Efficient handling of files of any size
- **Data Encryption**: Text and binary data processing

#### 🎨 **Enhanced CLI** (`cli_main.py`)
- **Interactive Interface**: Menu-driven navigation with wizards
- **Command-line Support**: Direct commands for automation
- **Visual Enhancements**: Animations, colors, and progress indicators
- **Professional Output**: Formatted tables and success messages

#### 🌐 **Web Application** (`app.py`)
- **Flask Framework**: Modern web interface with Bootstrap
- **File Upload/Download**: Drag & drop functionality
- **Real-time Feedback**: AJAX-powered operations
- **Responsive Design**: Mobile-friendly interface

#### 📊 **Database System** (`encryption_history.db`)
- **SQLite Backend**: Lightweight, serverless database
- **Operation Tracking**: Complete audit trail
- **History Management**: Search, filter, and export capabilities
- **Data Integrity**: ACID compliance and backup support

## 🧪 Testing & Quality Assurance

### 🔬 Comprehensive Test Suite

```bash
python test_functionality.py
```

**Test Coverage:**
- ✅ **Encryption/Decryption Accuracy**: Verify data integrity
- ✅ **Key Management**: Generation, storage, and retrieval
- ✅ **Database Operations**: CRUD operations and consistency
- ✅ **File Handling**: Path management and cleanup
- ✅ **Cross-platform Compatibility**: Windows, macOS, Linux
- ✅ **Error Handling**: Graceful failure recovery
- ✅ **Performance**: Large file processing efficiency

## 🛡️ Security Specifications

### 🔐 Encryption Standards

| Component | Specification | Details |
|-----------|---------------|---------|
| **Algorithm** | Triple DES (3DES) | Industry-standard symmetric encryption |
| **Mode** | CBC (Cipher Block Chaining) | Enhanced security with initialization vectors |
| **Key Size** | 192-bit (24 bytes) | Military-grade key strength |
| **Block Size** | 64-bit (8 bytes) | Standard DES block size |
| **Padding** | PKCS7 | Ensures compatibility with all file types |
| **IV Generation** | Cryptographically Secure Random | Unique IV for each operation |

### 🔑 Key Management

- **🎲 Secure Generation**: Uses `os.urandom()` for cryptographic randomness
- **🏷️ Unique Identifiers**: 16-character hexadecimal Key IDs
- **💾 Secure Storage**: JSON-based encrypted key vault
- **🔄 Key Rotation**: Support for multiple keys per user
- **📊 Usage Tracking**: Complete key usage audit trail

### 🛡️ Security Best Practices

- **✅ No Hardcoded Keys**: All keys generated dynamically
- **✅ Secure File Handling**: Automatic cleanup and path validation
- **✅ Input Sanitization**: Comprehensive validation of all inputs
- **✅ Error Handling**: No sensitive information in error messages
- **✅ Audit Trail**: Complete operation logging
- **✅ Cross-platform Security**: Consistent security across all platforms

## 📦 Dependencies & Requirements

### 🐍 Python Requirements

```python
# Core encryption dependencies
pycryptodome==3.19.0      # Cryptographic library for Triple DES

# Web interface dependencies
Flask==2.3.3              # Modern web framework
Werkzeug==2.3.7           # WSGI utilities and security helpers

# Enhanced CLI dependencies
colorama==0.4.6           # Cross-platform colored terminal output
tabulate==0.9.0           # Professional table formatting
```

### 🖥️ System Requirements

| Platform | Version | Status |
|----------|---------|--------|
| **Python** | 3.8+ | ✅ Required |
| **Windows** | 10/11 | ✅ Fully Supported |
| **macOS** | 10.14+ | ✅ Fully Supported |
| **Linux** | Ubuntu 18.04+ | ✅ Fully Supported |
| **Memory** | 512MB+ | ✅ Recommended |
| **Storage** | 100MB+ | ✅ For dependencies |

### 🌐 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| **Chrome** | 90+ | ✅ Fully Supported |
| **Firefox** | 88+ | ✅ Fully Supported |
| **Safari** | 14+ | ✅ Fully Supported |
| **Edge** | 90+ | ✅ Fully Supported |
| **Mobile** | All Modern | ✅ Responsive Design |

## 🚀 Development & Deployment

### 🔧 Development Mode

```bash
# CLI Development
python encrypt.py

# Web Development with auto-reload
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
python src/app.py
```

### 📊 Performance Optimization

- **⚡ Efficient File Processing**: Handles files of any size
- **🧠 Memory Management**: Optimized for large file operations
- **🔄 Async Operations**: Non-blocking UI during processing
- **📱 Responsive Design**: Optimized for all screen sizes
- **🎨 Smooth Animations**: Hardware-accelerated where possible

## 🎯 Use Cases & Applications

### 🏢 **Enterprise Applications**
- **📄 Document Security**: Protect sensitive business documents
- **💾 Data Backup**: Secure backup file encryption
- **📧 Email Attachments**: Encrypt files before sending
- **🗄️ Archive Management**: Long-term secure storage

### 🎓 **Educational & Research**
- **📚 Learning Cryptography**: Hands-on encryption experience
- **🔬 Security Research**: Analyze encryption implementations
- **👨‍🎓 Academic Projects**: Demonstrate security concepts
- **🧪 Algorithm Testing**: Validate encryption accuracy

### 👤 **Personal Use**
- **🔒 Privacy Protection**: Secure personal files
- **☁️ Cloud Storage**: Encrypt before uploading to cloud
- **💻 Device Security**: Protect files on shared computers
- **📱 Mobile Security**: Secure file transfer between devices

## 🌟 Advanced Features

### 🎨 **Enhanced CLI Experience**
```bash
# Beautiful startup animation with ASCII art
python encrypt.py
```

**Visual Features:**
- 🎭 **ASCII Art Logo**: Professional branding with typing animation
- 🌈 **Color-coded Output**: Success (Green), Error (Red), Warning (Yellow), Info (Blue)
- ⚡ **Loading Animations**: Spinning indicators and progress bars
- 📊 **Formatted Tables**: Professional data presentation with borders
- 🎪 **Smooth Transitions**: Elegant screen clearing and updates

### 📊 **Data Management**
```bash
# Enhanced history with file associations
python encrypt.py --list-keys
```

**Management Features:**
- 📁 **File Association Tracking**: See which files used each key
- 📈 **Usage Statistics**: Track key usage frequency
- 🗑️ **Bulk Operations**: Clear all keys or history with confirmation
- 🔍 **Smart Search**: Find files and keys quickly
- 📋 **Export Options**: Save history and key information

### 🛡️ **Security Enhancements**
- **🔐 Key ID Validation**: Verify key integrity before operations
- **📂 Organized Storage**: Dedicated `encrypted_decrypted_files` directory
- **🏷️ Smart Naming**: Automatic `decrypted_filename.extension` convention
- **🔍 File Detection**: Intelligent search in organized directories
- **⚠️ Safety Confirmations**: Prevent accidental data loss

## 🚨 Important Security Notes

### ⚠️ **Critical Reminders**
- **🔑 Key ID Storage**: Always backup your Key IDs securely
- **💾 Key Recovery**: Lost Key IDs cannot be recovered - files will be permanently inaccessible
- **🔒 Secure Backup**: Keep the `secure_keys` folder backed up safely
- **🧪 Test Decryption**: Always verify decryption immediately after encryption
- **🚫 Key Sharing**: Never share Key IDs through insecure channels

### 🛡️ **Best Practices**
1. **📝 Document Key IDs**: Maintain a secure record of important Key IDs
2. **🔄 Regular Backups**: Backup both encrypted files and key storage
3. **🧪 Test Recovery**: Periodically test your backup and recovery process
4. **🔐 Secure Environment**: Use the tool in a secure, trusted environment
5. **📊 Monitor Usage**: Review operation history regularly

## 🤝 Contributing & Community

### 🛠️ **Development Contributions**

1. **🍴 Fork the Repository**
   ```bash
   git clone https://github.com/bvivek2148/Triple-DES.git
   ```

2. **🌿 Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-enhancement
   ```

3. **💻 Develop & Test**
   ```bash
   # Make your changes
   python test_functionality.py  # Run tests
   ```

4. **📝 Commit Changes**
   ```bash
   git commit -m "✨ Add amazing enhancement"
   ```

5. **🚀 Submit Pull Request**
   ```bash
   git push origin feature/amazing-enhancement
   ```

### 🐛 **Bug Reports & Feature Requests**

- **🐛 Bug Reports**: Use GitHub Issues with detailed reproduction steps
- **💡 Feature Requests**: Describe the use case and expected behavior
- **📚 Documentation**: Help improve documentation and examples
- **🧪 Testing**: Contribute test cases and platform compatibility

### 👨‍💻 **Author & Maintainer**

**bvivek2148**
- 🐙 **GitHub**: [@bvivek2148](https://github.com/bvivek2148)
- 📧 **Contact**: Available through GitHub Issues
- 🌟 **Contributions**: Always welcome and appreciated

## 📄 License & Legal

This project is developed for **educational and demonstration purposes**.

### 📋 **Usage Terms**
- ✅ **Educational Use**: Free for learning and research
- ✅ **Personal Projects**: Use in personal applications
- ✅ **Open Source**: Contribute back to the community
- ⚠️ **Commercial Use**: Contact author for licensing
- 🛡️ **Security**: Use at your own risk for production systems

### 🔒 **Disclaimer**
This tool is provided "as-is" without warranty. Users are responsible for:
- 🔐 **Key Management**: Secure storage and backup of encryption keys
- 📊 **Data Backup**: Maintaining backups of important data
- 🛡️ **Security Assessment**: Evaluating suitability for specific use cases
- 🧪 **Testing**: Thorough testing before production use

---

<div align="center">

**🌟 Star this repository if you find it useful! 🌟**

**Made with ❤️ by [bvivek2148](https://github.com/bvivek2148)**

</div>
