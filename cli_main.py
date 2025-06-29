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
    """Color constants for CLI output"""
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    INFO = Fore.CYAN + Style.BRIGHT
    HEADER = Fore.MAGENTA + Style.BRIGHT
    RESET = Style.RESET_ALL

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
        """Print success message with formatting"""
        print(f"{CLIColors.SUCCESS}✅ {message}{CLIColors.RESET}")
    
    def print_error(self, message):
        """Print error message with formatting"""
        print(f"{CLIColors.ERROR}❌ {message}{CLIColors.RESET}")
    
    def print_warning(self, message):
        """Print warning message with formatting"""
        print(f"{CLIColors.WARNING}⚠️  {message}{CLIColors.RESET}")
    
    def print_info(self, message):
        """Print info message with formatting"""
        print(f"{CLIColors.INFO}ℹ️  {message}{CLIColors.RESET}")
    
    def print_header(self, message):
        """Print header message with formatting"""
        print(f"{CLIColors.HEADER}{message}{CLIColors.RESET}")
    
    def print_box(self, title, content, width=60):
        """Print content in a formatted box"""
        print("\n" + "=" * width)
        print(f"{CLIColors.HEADER}{title.center(width)}{CLIColors.RESET}")
        print("=" * width)
        for line in content:
            print(f"{CLIColors.INFO}{line}{CLIColors.RESET}")
        print("=" * width)
        print()
    
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
