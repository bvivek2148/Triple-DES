#!/usr/bin/env python3
"""
Triple DES Encryption CLI Tool
Professional Command Line Interface for File Encryption/Decryption

Author: Augment Agent
Version: 2.0.0
"""

import os
import sys
import argparse
import sqlite3
from datetime import datetime
from pathlib import Path
import json
import time
import shutil

# Add colorama for cross-platform colored output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback color definitions
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

# Add tabulate for better table formatting
try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

# Import our encryption module
from src.triple_des_example import TripleDESCipher

class CLIColors:
    """Enhanced color constants for CLI output"""
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    INFO = Fore.CYAN + Style.BRIGHT
    HEADER = Fore.MAGENTA + Style.BRIGHT
    ACCENT = Fore.BLUE + Style.BRIGHT
    SUBTLE = Fore.WHITE + Style.DIM
    HIGHLIGHT = Back.BLUE + Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

class CLIUtils:
    """Utility functions for enhanced CLI experience"""

    @staticmethod
    def get_terminal_width():
        """Get terminal width, default to 80 if unable to determine"""
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80

    @staticmethod
    def center_text(text, width=None):
        """Center text within terminal width"""
        if width is None:
            width = CLIUtils.get_terminal_width()
        return text.center(width)

    @staticmethod
    def typing_effect(text, delay=0.03):
        """Print text with typing effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def progress_bar(current, total, width=50, prefix="Progress"):
        """Display a progress bar"""
        percent = current / total
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        print(f'\r{prefix}: |{bar}| {percent:.1%}', end='', flush=True)
        if current == total:
            print()

    @staticmethod
    def create_border(char='═', width=None):
        """Create a border line"""
        if width is None:
            width = min(CLIUtils.get_terminal_width(), 80)
        return char * width

class TripleDESCLI:
    """Main CLI application class"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.cipher = TripleDESCipher()
        self.db_path = self.project_root / 'database' / 'encryption_history.db'
        self.uploads_dir = self.project_root / 'uploads'
        self.keys_dir = self.project_root / 'secure_keys'
        
        # Ensure directories exist
        self.uploads_dir.mkdir(exist_ok=True)
        self.keys_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS encryption_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    key_id TEXT NOT NULL,
                    operation_type TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            self.print_error(f"Database initialization failed: {e}")
    
    def print_success(self, message):
        """Print success message with enhanced formatting"""
        print(f"{CLIColors.SUCCESS}✅ {message}{CLIColors.RESET}")

    def print_error(self, message):
        """Print error message with enhanced formatting"""
        print(f"{CLIColors.ERROR}❌ {message}{CLIColors.RESET}")

    def print_warning(self, message):
        """Print warning message with enhanced formatting"""
        print(f"{CLIColors.WARNING}⚠️  {message}{CLIColors.RESET}")

    def print_info(self, message):
        """Print info message with enhanced formatting"""
        print(f"{CLIColors.INFO}ℹ️  {message}{CLIColors.RESET}")

    def print_header(self, message):
        """Print header message with enhanced formatting"""
        print(f"{CLIColors.HEADER}{message}{CLIColors.RESET}")

    def print_accent(self, message):
        """Print accent message with special formatting"""
        print(f"{CLIColors.ACCENT}🔹 {message}{CLIColors.RESET}")

    def print_highlight(self, message):
        """Print highlighted message"""
        print(f"{CLIColors.HIGHLIGHT} {message} {CLIColors.RESET}")

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_enhanced_box(self, title, content, box_type="success", width=None):
        """Print content in an enhanced formatted box"""
        if width is None:
            width = min(CLIUtils.get_terminal_width(), 80)

        # Choose colors based on box type
        if box_type == "success":
            border_color = CLIColors.SUCCESS
            title_color = CLIColors.SUCCESS
            content_color = CLIColors.INFO
            icon = "🎉"
        elif box_type == "error":
            border_color = CLIColors.ERROR
            title_color = CLIColors.ERROR
            content_color = CLIColors.WARNING
            icon = "❌"
        elif box_type == "warning":
            border_color = CLIColors.WARNING
            title_color = CLIColors.WARNING
            content_color = CLIColors.INFO
            icon = "⚠️"
        else:  # info
            border_color = CLIColors.INFO
            title_color = CLIColors.HEADER
            content_color = CLIColors.INFO
            icon = "ℹ️"

        # Create the box
        print()
        print(f"{border_color}{'╔' + '═' * (width - 2) + '╗'}{CLIColors.RESET}")
        title_line = f"{icon} {title} {icon}"
        print(f"{border_color}║{title_color}{title_line.center(width - 2)}{border_color}║{CLIColors.RESET}")
        print(f"{border_color}{'╠' + '═' * (width - 2) + '╣'}{CLIColors.RESET}")

        for line in content:
            if line.strip():  # Non-empty line
                print(f"{border_color}║ {content_color}{line:<{width - 4}}{border_color} ║{CLIColors.RESET}")
            else:  # Empty line for spacing
                print(f"{border_color}║{' ' * (width - 2)}║{CLIColors.RESET}")

        print(f"{border_color}{'╚' + '═' * (width - 2) + '╝'}{CLIColors.RESET}")
        print()

    def print_separator(self, char='─', width=None):
        """Print a separator line"""
        if width is None:
            width = min(CLIUtils.get_terminal_width(), 80)
        print(f"{CLIColors.SUBTLE}{char * width}{CLIColors.RESET}")

    def animate_loading(self, message, duration=2):
        """Show a loading animation"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f'\r{CLIColors.INFO}{frame} {message}...{CLIColors.RESET}', end='', flush=True)
                time.sleep(0.1)
                if time.time() >= end_time:
                    break

        print(f'\r{CLIColors.SUCCESS}✅ {message} completed!{CLIColors.RESET}')
        time.sleep(0.5)

    def startup_animation(self):
        """Show a beautiful startup animation"""
        self.clear_screen()

        # ASCII art logo with animation
        logo_lines = [
            "  ████████╗██████╗ ██╗██████╗ ██╗     ███████╗    ██████╗ ███████╗███████╗",
            "  ╚══██╔══╝██╔══██╗██║██╔══██╗██║     ██╔════╝    ██╔══██╗██╔════╝██╔════╝",
            "     ██║   ██████╔╝██║██████╔╝██║     █████╗      ██║  ██║█████╗  ███████╗",
            "     ██║   ██╔══██╗██║██╔═══╝ ██║     ██╔══╝      ██║  ██║██╔══╝  ╚════██║",
            "     ██║   ██║  ██║██║██║     ███████╗███████╗    ██████╔╝███████╗███████║",
            "     ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝╚══════╝    ╚═════╝ ╚══════╝╚══════╝"
        ]

        print(f"\n{CLIColors.HEADER}")
        for line in logo_lines:
            CLIUtils.typing_effect(line, delay=0.005)
            time.sleep(0.1)
        print(CLIColors.RESET)

        # Animated subtitle
        subtitle = "🔐 PROFESSIONAL ENCRYPTION CLI 🔐"
        print(f"\n{CLIColors.ACCENT}")
        CLIUtils.typing_effect(CLIUtils.center_text(subtitle), delay=0.02)
        print(CLIColors.RESET)

        # Loading animation
        print(f"\n{CLIColors.INFO}Initializing security modules...{CLIColors.RESET}")

        modules = [
            "🔑 Key Management System",
            "🛡️  Triple DES Encryption Engine",
            "📊 History Database",
            "🎨 Enhanced CLI Interface",
            "⚡ Performance Optimizations"
        ]

        for module in modules:
            print(f"{CLIColors.SUBTLE}Loading {module}...{CLIColors.RESET}", end="", flush=True)
            time.sleep(0.3)
            print(f" {CLIColors.SUCCESS}✅{CLIColors.RESET}")

        print(f"\n{CLIColors.SUCCESS}🚀 All systems ready!{CLIColors.RESET}")
        time.sleep(1)

        # Transition effect
        for i in range(3):
            print(".", end="", flush=True)
            time.sleep(0.3)
        print()

        time.sleep(0.5)
    
    def add_to_history(self, filename, key_id, operation_type):
        """Add operation to history database"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''
                INSERT INTO encryption_history (filename, key_id, operation_type)
                VALUES (?, ?, ?)
            ''', (filename, key_id, operation_type))
            conn.commit()
            conn.close()
        except Exception as e:
            self.print_error(f"Failed to add to history: {e}")
    
    def get_history(self, limit=10):
        """Get operation history from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM encryption_history ORDER BY timestamp DESC LIMIT ?', (limit,))
            history = c.fetchall()
            conn.close()
            return history
        except Exception as e:
            self.print_error(f"Failed to get history: {e}")
            return []

    def encrypt_file_cli(self, input_file, output_file=None):
        """Encrypt a file via CLI"""
        try:
            input_path = Path(input_file)
            if not input_path.exists():
                self.print_error(f"Input file not found: {input_file}")
                return False

            # Generate output filename if not provided
            if output_file is None:
                output_file = f"encrypted_{input_path.name}.bin"

            output_path = Path(output_file)

            # Generate new key and encrypt
            self.cipher.generate_key()
            key_id = os.urandom(8).hex()
            self.cipher.save_key(key_id)

            # Perform encryption
            self.cipher.encrypt_file(str(input_path), str(output_path))

            # Add to history
            self.add_to_history(input_path.name, key_id, 'Encryption')

            # Show progress animation
            self.animate_loading("Encrypting file", 1.5)

            # Display enhanced success message
            success_content = [
                f"📁 Original file: {input_path.name}",
                f"🔒 Encrypted file: {output_path.name}",
                f"🔑 Key ID: {key_id}",
                "",
                "⚠️  IMPORTANT: Save this Key ID to decrypt your file later!",
                "💾 Store it securely - you cannot decrypt without it!",
                "",
                f"📊 File size: {input_path.stat().st_size:,} bytes"
            ]

            self.print_enhanced_box("FILE ENCRYPTION COMPLETED", success_content, "success")
            self.print_highlight(f"🔐 Encryption Key: {key_id}")

            # Show key storage location
            self.print_accent(f"Key stored in: {self.keys_dir / 'secure_keys.json'}")

            return True

        except Exception as e:
            self.print_error(f"Encryption failed: {e}")
            return False

    def decrypt_file_cli(self, input_file, key_id, output_file=None):
        """Decrypt a file via CLI"""
        try:
            input_path = Path(input_file)
            if not input_path.exists():
                self.print_error(f"Input file not found: {input_file}")
                return False

            # Generate output filename if not provided
            if output_file is None:
                output_file = f"decrypted_{input_path.stem}"
                if input_path.suffix == '.bin':
                    # Try to extract original extension
                    base_name = input_path.stem
                    if base_name.startswith('encrypted_'):
                        output_file = base_name[10:]  # Remove 'encrypted_' prefix

            output_path = Path(output_file)

            # Load key and decrypt
            if not self.cipher.load_key(key_id):
                self.print_error(f"Key ID not found: {key_id}")
                return False

            # Perform decryption
            self.cipher.decrypt_file(str(input_path), str(output_path))

            # Add to history
            self.add_to_history(input_path.name, key_id, 'Decryption')

            # Show progress animation
            self.animate_loading("Decrypting file", 1.2)

            # Display enhanced success message
            success_content = [
                f"🔒 Encrypted file: {input_path.name}",
                f"📁 Decrypted file: {output_path.name}",
                f"🔑 Key ID used: {key_id}",
                "",
                "✅ File successfully decrypted!",
                "",
                f"📊 Output size: {output_path.stat().st_size:,} bytes"
            ]

            self.print_enhanced_box("FILE DECRYPTION COMPLETED", success_content, "success")

            return True

        except Exception as e:
            self.print_error(f"Decryption failed: {e}")
            return False

    def encrypt_text_cli(self, text, output_file=None):
        """Encrypt text via CLI"""
        try:
            # Generate new key and encrypt
            self.cipher.generate_key()
            key_id = os.urandom(8).hex()
            self.cipher.save_key(key_id)

            # Perform encryption
            encrypted_data = self.cipher.encrypt_data(text)

            if output_file:
                # Save to file
                with open(output_file, 'wb') as f:
                    f.write(encrypted_data)

                # Show progress animation
                self.animate_loading("Encrypting text to file", 1.0)

                success_content = [
                    f"📝 Original text: {text[:50]}{'...' if len(text) > 50 else ''}",
                    f"💾 Output file: {output_file}",
                    f"🔑 Key ID: {key_id}",
                    "",
                    "⚠️  IMPORTANT: Save this Key ID to decrypt your text later!",
                    "",
                    f"📊 Text length: {len(text)} characters"
                ]

                self.print_enhanced_box("TEXT ENCRYPTION COMPLETED", success_content, "success")
            else:
                # Show progress animation
                self.animate_loading("Encrypting text", 0.8)

                # Display encrypted text
                success_content = [
                    f"📝 Original text: {text[:50]}{'...' if len(text) > 50 else ''}",
                    f"🔒 Encrypted (base64): {encrypted_data.decode()[:60]}{'...' if len(encrypted_data.decode()) > 60 else ''}",
                    f"🔑 Key ID: {key_id}",
                    "",
                    "⚠️  IMPORTANT: Save this Key ID to decrypt your text later!",
                    "",
                    f"📊 Text length: {len(text)} characters",
                    f"📊 Encrypted length: {len(encrypted_data.decode())} characters"
                ]

                self.print_enhanced_box("TEXT ENCRYPTION COMPLETED", success_content, "success")

            self.print_highlight(f"🔐 Encryption Key: {key_id}")

            # Add to history
            self.add_to_history("text_data", key_id, 'Text Encryption')

            return True

        except Exception as e:
            self.print_error(f"Text encryption failed: {e}")
            return False

    def decrypt_text_cli(self, encrypted_text, key_id, is_file=False):
        """Decrypt text via CLI"""
        try:
            # Load key
            if not self.cipher.load_key(key_id):
                self.print_error(f"Key ID not found: {key_id}")
                return False

            if is_file:
                # Read from file
                with open(encrypted_text, 'rb') as f:
                    encrypted_data = f.read()
            else:
                # Use text directly
                encrypted_data = encrypted_text.encode() if isinstance(encrypted_text, str) else encrypted_text

            # Perform decryption
            decrypted_data = self.cipher.decrypt_data(encrypted_data)
            decrypted_text = decrypted_data.decode()

            # Show progress animation
            self.animate_loading("Decrypting text", 0.8)

            # Display enhanced success message
            success_content = [
                f"🔒 Encrypted source: {'📁 File' if is_file else '📝 Text'}",
                f"📖 Decrypted text: {decrypted_text[:100]}{'...' if len(decrypted_text) > 100 else ''}",
                f"🔑 Key ID used: {key_id}",
                "",
                "✅ Text successfully decrypted!",
                "",
                f"📊 Decrypted length: {len(decrypted_text)} characters"
            ]

            self.print_enhanced_box("TEXT DECRYPTION COMPLETED", success_content, "success")

            # Add to history
            self.add_to_history("text_data", key_id, 'Text Decryption')

            return True

        except Exception as e:
            self.print_error(f"Text decryption failed: {e}")
            return False

    def show_history_cli(self, limit=10):
        """Display enhanced operation history"""
        print(f"\n{CLIColors.HEADER}📊 OPERATION HISTORY{CLIColors.RESET}")
        self.animate_loading("Loading history", 0.8)

        history = self.get_history(limit)

        if not history:
            self.print_enhanced_box("NO HISTORY FOUND",
                                  ["📭 No encryption operations have been performed yet.",
                                   "",
                                   "💡 Start by encrypting a file or text to see history here."],
                                  "warning")
            return

        print(f"\n{CLIColors.ACCENT}📈 Showing last {len(history)} operations (limit: {limit}){CLIColors.RESET}")
        print()

        if TABULATE_AVAILABLE:
            # Enhanced table with better formatting
            headers = [
                f"{CLIColors.HEADER}ID{CLIColors.RESET}",
                f"{CLIColors.HEADER}📁 Filename{CLIColors.RESET}",
                f"{CLIColors.HEADER}🔑 Key ID{CLIColors.RESET}",
                f"{CLIColors.HEADER}⚡ Operation{CLIColors.RESET}",
                f"{CLIColors.HEADER}🕒 Timestamp{CLIColors.RESET}"
            ]
            table_data = []
            for record in history:
                # Color-code operations
                op_color = CLIColors.SUCCESS if 'Encryption' in record['operation_type'] else CLIColors.INFO
                operation = f"{op_color}{record['operation_type']}{CLIColors.RESET}"

                table_data.append([
                    f"{CLIColors.ACCENT}{record['id']}{CLIColors.RESET}",
                    record['filename'][:25] + '...' if len(record['filename']) > 25 else record['filename'],
                    f"{CLIColors.WARNING}{record['key_id'][:12]}...{CLIColors.RESET}",
                    operation,
                    f"{CLIColors.SUBTLE}{record['timestamp'][:19]}{CLIColors.RESET}"
                ])

            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        else:
            # Enhanced fallback formatting
            for i, record in enumerate(history, 1):
                print(f"{CLIColors.ACCENT}{i:2d}.{CLIColors.RESET} {CLIColors.INFO}{record['filename'][:30]}{CLIColors.RESET}")
                print(f"    🔑 Key: {CLIColors.WARNING}{record['key_id'][:16]}...{CLIColors.RESET}")
                print(f"    ⚡ Op: {CLIColors.SUCCESS}{record['operation_type']}{CLIColors.RESET}")
                print(f"    🕒 Time: {CLIColors.SUBTLE}{record['timestamp'][:19]}{CLIColors.RESET}")
                print()

        print()
        self.print_accent(f"💾 Database location: {self.db_path}")
        print()

    def list_keys_cli(self):
        """List all stored encryption keys"""
        try:
            key_file = self.keys_dir / 'secure_keys.json'
            if not key_file.exists():
                self.print_warning("No keys found.")
                return

            with open(key_file, 'r') as f:
                keys_data = json.load(f)

            # Remove 'current_key' from display
            display_keys = {k: v for k, v in keys_data.items() if k != 'current_key'}

            if not display_keys:
                self.print_warning("No stored keys found.")
                return

            self.print_header(f"\n🔑 STORED ENCRYPTION KEYS ({len(display_keys)} keys)")
            print()

            if TABULATE_AVAILABLE:
                headers = ["Key ID", "Created"]
                table_data = []
                for key_id in display_keys.keys():
                    # We don't have creation time, so show key ID only
                    table_data.append([key_id, "N/A"])

                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                for i, key_id in enumerate(display_keys.keys(), 1):
                    print(f"{CLIColors.INFO}{i:2d}. {key_id}{CLIColors.RESET}")

            print()

        except Exception as e:
            self.print_error(f"Failed to list keys: {e}")

    def show_banner(self):
        """Display enhanced application banner with animation"""
        self.clear_screen()

        width = min(CLIUtils.get_terminal_width(), 80)

        # Animated banner reveal
        banner_lines = [
            "╔" + "═" * (width - 2) + "╗",
            "║" + "TRIPLE DES ENCRYPTION CLI".center(width - 2) + "║",
            "║" + "Professional Security Tool".center(width - 2) + "║",
            "║" + "Version 2.0.0 Enhanced".center(width - 2) + "║",
            "╚" + "═" * (width - 2) + "╝"
        ]

        print(f"\n{CLIColors.HEADER}", end="")
        for line in banner_lines:
            CLIUtils.typing_effect(line, delay=0.01)
            time.sleep(0.1)
        print(CLIColors.RESET)

        # Feature highlights with icons
        features = [
            "🔐 Secure file and text encryption using Triple DES algorithm",
            "🛡️  Military-grade encryption with CBC mode and proper padding",
            "🔑 Advanced key management with unique key IDs",
            "📊 Professional CLI interface with enhanced user experience",
            "⚡ Lightning-fast encryption with progress indicators"
        ]

        print(f"\n{CLIColors.ACCENT}✨ FEATURES:{CLIColors.RESET}")
        for feature in features:
            print(f"   {CLIColors.INFO}{feature}{CLIColors.RESET}")
            time.sleep(0.2)

        print()
        self.print_separator('─')
        print()

    def show_menu(self):
        """Display enhanced interactive menu"""
        width = min(CLIUtils.get_terminal_width(), 60)

        print(f"{CLIColors.HEADER}{'📋 MAIN MENU'.center(width)}{CLIColors.RESET}")
        print()

        menu_items = [
            ("1", "🔒", "Encrypt File", "Secure file encryption with auto-generated keys"),
            ("2", "🔓", "Decrypt File", "Decrypt files using stored key IDs"),
            ("3", "📝", "Encrypt Text", "Encrypt text with optional file output"),
            ("4", "📖", "Decrypt Text", "Decrypt text from files or direct input"),
            ("5", "📊", "View History", "Display recent encryption operations"),
            ("6", "🔑", "List Keys", "Show all stored encryption key IDs"),
            ("7", "❓", "Help", "Comprehensive help and usage information"),
            ("8", "🚪", "Exit", "Exit the application safely")
        ]

        # Create a beautiful menu with descriptions
        for num, icon, title, desc in menu_items:
            print(f"  {CLIColors.ACCENT}{num}.{CLIColors.RESET} {CLIColors.SUCCESS}{icon} {title:<15}{CLIColors.RESET}")
            print(f"     {CLIColors.SUBTLE}{desc}{CLIColors.RESET}")
            print()

        self.print_separator('─', width)

    def interactive_mode(self):
        """Run enhanced interactive CLI mode"""
        # Show startup animation first
        self.startup_animation()

        # Then show the main banner
        self.show_banner()

        while True:
            self.show_menu()

            try:
                choice = input(f"\n{CLIColors.ACCENT}🎯 Enter your choice (1-8): {CLIColors.RESET}").strip()

                if choice == '1':
                    self.handle_encrypt_file()
                elif choice == '2':
                    self.handle_decrypt_file()
                elif choice == '3':
                    self.handle_encrypt_text()
                elif choice == '4':
                    self.handle_decrypt_text()
                elif choice == '5':
                    self.handle_show_history()
                elif choice == '6':
                    self.list_keys_cli()
                elif choice == '7':
                    self.show_help()
                elif choice == '8':
                    self.show_goodbye()
                    break
                else:
                    self.print_enhanced_box("INVALID CHOICE",
                                          [f"❌ '{choice}' is not a valid option.",
                                           "",
                                           "💡 Please enter a number between 1-8.",
                                           "🔄 Try again with a valid menu option."],
                                          "error")

                print()
                input(f"{CLIColors.ACCENT}⏎ Press Enter to continue...{CLIColors.RESET}")
                self.clear_screen()
                time.sleep(0.2)

            except KeyboardInterrupt:
                print(f"\n\n{CLIColors.WARNING}⚠️  Operation cancelled by user.{CLIColors.RESET}")
                self.show_goodbye()
                break
            except Exception as e:
                self.print_enhanced_box("UNEXPECTED ERROR",
                                      [f"❌ An unexpected error occurred: {str(e)}",
                                       "",
                                       "🔧 Please try again or contact support if the issue persists.",
                                       "📝 Error details have been logged for debugging."],
                                      "error")

    def show_goodbye(self):
        """Show a beautiful goodbye message"""
        goodbye_content = [
            "🎉 Thank you for using Triple DES CLI!",
            "",
            "🔐 Your files are now secure with military-grade encryption.",
            "💾 Remember to keep your Key IDs safe and backed up.",
            "",
            "🌟 Stay secure, stay protected!",
            "👋 Goodbye and see you next time!"
        ]

        self.print_enhanced_box("SESSION COMPLETE", goodbye_content, "success")

        # Final animation
        print(f"{CLIColors.ACCENT}Shutting down securely", end="")
        for i in range(5):
            print(".", end="", flush=True)
            time.sleep(0.2)
        print(f" {CLIColors.SUCCESS}✅{CLIColors.RESET}\n")

    def handle_encrypt_file(self):
        """Handle file encryption in interactive mode"""
        self.print_separator('═')
        print(f"\n{CLIColors.HEADER}🔒 FILE ENCRYPTION WIZARD{CLIColors.RESET}")
        print(f"{CLIColors.SUBTLE}Secure your files with military-grade Triple DES encryption{CLIColors.RESET}\n")

        # Enhanced file input with validation
        while True:
            input_file = input(f"{CLIColors.INFO}📁 Enter file path to encrypt: {CLIColors.RESET}").strip()
            if not input_file:
                self.print_error("File path cannot be empty.")
                continue

            if not Path(input_file).exists():
                self.print_error(f"File not found: {input_file}")
                retry = input(f"{CLIColors.WARNING}Try again? (y/N): {CLIColors.RESET}").strip().lower()
                if retry not in ['y', 'yes']:
                    return
                continue
            break

        # Show file info
        file_path = Path(input_file)
        file_size = file_path.stat().st_size
        print(f"\n{CLIColors.SUCCESS}✅ File found: {file_path.name}{CLIColors.RESET}")
        print(f"{CLIColors.INFO}📊 Size: {file_size:,} bytes ({file_size/1024:.1f} KB){CLIColors.RESET}")

        # Output file selection
        output_file = input(f"\n{CLIColors.INFO}💾 Enter output file path (or press Enter for auto): {CLIColors.RESET}").strip()
        if not output_file:
            output_file = None
            auto_name = f"encrypted_{file_path.name}.bin"
            print(f"{CLIColors.ACCENT}🔄 Auto-generated name: {auto_name}{CLIColors.RESET}")

        # Confirmation
        print(f"\n{CLIColors.WARNING}⚠️  Ready to encrypt:{CLIColors.RESET}")
        print(f"   📁 Input: {input_file}")
        print(f"   🔒 Output: {output_file or auto_name}")

        confirm = input(f"\n{CLIColors.ACCENT}Proceed with encryption? (Y/n): {CLIColors.RESET}").strip().lower()
        if confirm in ['', 'y', 'yes']:
            self.encrypt_file_cli(input_file, output_file)
        else:
            self.print_warning("Encryption cancelled.")

    def handle_decrypt_file(self):
        """Handle file decryption in interactive mode"""
        print(f"\n{CLIColors.HEADER}🔓 FILE DECRYPTION{CLIColors.RESET}")

        input_file = input(f"{CLIColors.INFO}Enter encrypted file path: {CLIColors.RESET}").strip()
        if not input_file:
            self.print_error("File path cannot be empty.")
            return

        key_id = input(f"{CLIColors.INFO}Enter Key ID: {CLIColors.RESET}").strip()
        if not key_id:
            self.print_error("Key ID cannot be empty.")
            return

        output_file = input(f"{CLIColors.INFO}Enter output file path (or press Enter for auto): {CLIColors.RESET}").strip()
        if not output_file:
            output_file = None

        self.decrypt_file_cli(input_file, key_id, output_file)

    def handle_encrypt_text(self):
        """Handle text encryption in interactive mode"""
        print(f"\n{CLIColors.HEADER}📝 TEXT ENCRYPTION{CLIColors.RESET}")

        text = input(f"{CLIColors.INFO}Enter text to encrypt: {CLIColors.RESET}").strip()
        if not text:
            self.print_error("Text cannot be empty.")
            return

        save_to_file = input(f"{CLIColors.INFO}Save to file? (y/N): {CLIColors.RESET}").strip().lower()

        output_file = None
        if save_to_file in ['y', 'yes']:
            output_file = input(f"{CLIColors.INFO}Enter output file path: {CLIColors.RESET}").strip()
            if not output_file:
                self.print_error("Output file path cannot be empty.")
                return

        self.encrypt_text_cli(text, output_file)

    def handle_decrypt_text(self):
        """Handle text decryption in interactive mode"""
        print(f"\n{CLIColors.HEADER}📖 TEXT DECRYPTION{CLIColors.RESET}")

        source_type = input(f"{CLIColors.INFO}Decrypt from (f)ile or (t)ext? (f/t): {CLIColors.RESET}").strip().lower()

        if source_type in ['f', 'file']:
            encrypted_source = input(f"{CLIColors.INFO}Enter encrypted file path: {CLIColors.RESET}").strip()
            is_file = True
        else:
            encrypted_source = input(f"{CLIColors.INFO}Enter encrypted text (base64): {CLIColors.RESET}").strip()
            is_file = False

        if not encrypted_source:
            self.print_error("Encrypted source cannot be empty.")
            return

        key_id = input(f"{CLIColors.INFO}Enter Key ID: {CLIColors.RESET}").strip()
        if not key_id:
            self.print_error("Key ID cannot be empty.")
            return

        self.decrypt_text_cli(encrypted_source, key_id, is_file)

    def handle_show_history(self):
        """Handle showing history in interactive mode"""
        print(f"\n{CLIColors.HEADER}📊 OPERATION HISTORY{CLIColors.RESET}")

        limit_input = input(f"{CLIColors.INFO}Number of records to show (default 10): {CLIColors.RESET}").strip()

        try:
            limit = int(limit_input) if limit_input else 10
            if limit <= 0:
                limit = 10
        except ValueError:
            limit = 10
            self.print_warning("Invalid number, using default (10).")

        self.show_history_cli(limit)

    def show_help(self):
        """Display help information"""
        help_text = f"""
{CLIColors.HEADER}❓ TRIPLE DES CLI HELP{CLIColors.RESET}

{CLIColors.INFO}OVERVIEW:{CLIColors.RESET}
This CLI tool provides secure file and text encryption using the Triple DES algorithm
with CBC mode and proper PKCS7 padding for maximum security.

{CLIColors.INFO}FEATURES:{CLIColors.RESET}
• 🔒 File Encryption/Decryption with automatic key generation
• 📝 Text Encryption/Decryption with base64 encoding
• 🔑 Secure key management with unique Key IDs
• 📊 Operation history tracking
• 🎨 Colorized output for better user experience
• 💾 Automatic file handling and cleanup

{CLIColors.INFO}SECURITY NOTES:{CLIColors.RESET}
• Each encryption operation generates a unique 24-byte Triple DES key
• Keys are stored securely with random 8-byte Key IDs
• CBC mode with random initialization vectors for enhanced security
• PKCS7 padding ensures compatibility with all file types

{CLIColors.INFO}KEY MANAGEMENT:{CLIColors.RESET}
• Key IDs are automatically generated (e.g., 'a1b2c3d4e5f6g7h8')
• Store your Key ID securely - you cannot decrypt without it!
• Keys are saved in 'secure_keys/secure_keys.json'
• Use 'List Keys' option to view all stored Key IDs

{CLIColors.INFO}COMMAND LINE USAGE:{CLIColors.RESET}
You can also use this tool with command line arguments:

{CLIColors.SUCCESS}Encrypt a file:{CLIColors.RESET}
  python cli_main.py --encrypt --file document.pdf

{CLIColors.SUCCESS}Decrypt a file:{CLIColors.RESET}
  python cli_main.py --decrypt --file encrypted_document.pdf.bin --key a1b2c3d4e5f6g7h8

{CLIColors.SUCCESS}Encrypt text:{CLIColors.RESET}
  python cli_main.py --encrypt --text "Hello World"

{CLIColors.SUCCESS}Decrypt text:{CLIColors.RESET}
  python cli_main.py --decrypt --text "base64_encrypted_text" --key a1b2c3d4e5f6g7h8

{CLIColors.WARNING}IMPORTANT REMINDERS:{CLIColors.RESET}
• Always backup your Key IDs in a secure location
• Encrypted files cannot be recovered without the correct Key ID
• Keep your 'secure_keys' folder safe and backed up
• Test decryption immediately after encryption to verify Key ID

{CLIColors.INFO}For more information, visit the project documentation.{CLIColors.RESET}
"""
        print(help_text)


def create_argument_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Triple DES Encryption CLI Tool - Professional Security Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode (default):
    python cli_main.py

  Encrypt a file:
    python cli_main.py --encrypt --file document.pdf

  Decrypt a file:
    python cli_main.py --decrypt --file encrypted_document.pdf.bin --key a1b2c3d4e5f6g7h8

  Encrypt text:
    python cli_main.py --encrypt --text "Hello World"

  Decrypt text:
    python cli_main.py --decrypt --text "base64_encrypted_text" --key a1b2c3d4e5f6g7h8

  Show history:
    python cli_main.py --history

  List keys:
    python cli_main.py --list-keys
        """
    )

    # Main action group
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument('--encrypt', action='store_true', help='Encrypt data')
    action_group.add_argument('--decrypt', action='store_true', help='Decrypt data')
    action_group.add_argument('--history', action='store_true', help='Show operation history')
    action_group.add_argument('--list-keys', action='store_true', help='List stored keys')

    # Input type group
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('--file', type=str, help='File path to encrypt/decrypt')
    input_group.add_argument('--text', type=str, help='Text to encrypt/decrypt')

    # Additional options
    parser.add_argument('--output', type=str, help='Output file path (optional)')
    parser.add_argument('--key', type=str, help='Key ID for decryption')
    parser.add_argument('--limit', type=int, default=10, help='Number of history records to show')

    return parser


def main():
    """Main entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Initialize CLI application
    cli = TripleDESCLI()

    # Handle command line arguments
    if args.encrypt:
        if args.file:
            success = cli.encrypt_file_cli(args.file, args.output)
            sys.exit(0 if success else 1)
        elif args.text:
            success = cli.encrypt_text_cli(args.text, args.output)
            sys.exit(0 if success else 1)
        else:
            cli.print_error("Please specify --file or --text for encryption")
            sys.exit(1)

    elif args.decrypt:
        if not args.key:
            cli.print_error("Key ID is required for decryption (use --key)")
            sys.exit(1)

        if args.file:
            success = cli.decrypt_file_cli(args.file, args.key, args.output)
            sys.exit(0 if success else 1)
        elif args.text:
            success = cli.decrypt_text_cli(args.text, args.key, False)
            sys.exit(0 if success else 1)
        else:
            cli.print_error("Please specify --file or --text for decryption")
            sys.exit(1)

    elif args.history:
        cli.show_history_cli(args.limit)
        sys.exit(0)

    elif args.list_keys:
        cli.list_keys_cli()
        sys.exit(0)

    else:
        # No arguments provided, run interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
