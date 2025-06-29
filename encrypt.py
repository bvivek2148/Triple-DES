#!/usr/bin/env python3
"""
Triple DES Encryption CLI - Quick Launcher
Simple launcher script for the Triple DES CLI tool
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from cli_main import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Error: Missing dependencies. Please install requirements:")
    print(f"   pip install -r requirements.txt")
    print(f"\nError details: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
