#!/usr/bin/env python3
"""
Test script to verify all functionality works correctly after fixes
"""

import os
import sys
import tempfile
from src.triple_des_example import TripleDESCipher
import sqlite3

def test_triple_des():
    """Test Triple DES encryption/decryption"""
    print("Testing Triple DES functionality...")
    
    cipher = TripleDESCipher()
    
    # Test text encryption/decryption
    test_text = "Hello, this is a test message for Triple DES encryption!"
    
    # Generate key
    cipher.generate_key()
    
    # Encrypt
    encrypted = cipher.encrypt_data(test_text)
    print(f"✅ Text encrypted successfully")
    
    # Decrypt
    decrypted = cipher.decrypt_data(encrypted)
    decrypted_text = decrypted.decode()
    
    if decrypted_text == test_text:
        print(f"✅ Text decryption successful: {decrypted_text}")
    else:
        print(f"❌ Text decryption failed")
        return False
    
    # Test file encryption/decryption
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(test_text)
        test_file = f.name
    
    encrypted_file = test_file + '.encrypted'
    decrypted_file = test_file + '.decrypted'
    
    try:
        # Encrypt file
        cipher.encrypt_file(test_file, encrypted_file)
        print(f"✅ File encrypted successfully")
        
        # Decrypt file
        cipher.decrypt_file(encrypted_file, decrypted_file)
        print(f"✅ File decrypted successfully")
        
        # Verify content
        with open(decrypted_file, 'r') as f:
            decrypted_content = f.read()
        
        if decrypted_content == test_text:
            print(f"✅ File content matches original")
        else:
            print(f"❌ File content doesn't match")
            return False
            
    finally:
        # Cleanup
        for file_path in [test_file, encrypted_file, decrypted_file]:
            if os.path.exists(file_path):
                os.unlink(file_path)
    
    return True

def test_key_management():
    """Test key saving and loading"""
    print("\nTesting key management...")
    
    cipher = TripleDESCipher()
    
    # Generate and save key
    cipher.generate_key()
    test_key_id = "test_key_123"
    cipher.save_key(test_key_id)
    print(f"✅ Key saved with ID: {test_key_id}")
    
    # Create new cipher instance and load key
    cipher2 = TripleDESCipher()
    if cipher2.load_key(test_key_id):
        print(f"✅ Key loaded successfully")
    else:
        print(f"❌ Key loading failed")
        return False
    
    # Test encryption/decryption with loaded key
    test_data = "Test data for key loading"
    encrypted = cipher.encrypt_data(test_data)
    decrypted = cipher2.decrypt_data(encrypted).decode()
    
    if decrypted == test_data:
        print(f"✅ Encryption/decryption with loaded key successful")
    else:
        print(f"❌ Encryption/decryption with loaded key failed")
        return False
    
    return True

def test_database():
    """Test database functionality"""
    print("\nTesting database functionality...")
    
    db_path = os.path.join('database', 'encryption_history.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Test insert
        c.execute('''
            INSERT INTO encryption_history (filename, key_id, operation_type)
            VALUES (?, ?, ?)
        ''', ('test_file.txt', 'test_key_123', 'Test'))
        
        # Test select
        c.execute('SELECT * FROM encryption_history WHERE operation_type = ?', ('Test',))
        result = c.fetchone()
        
        if result:
            print(f"✅ Database insert/select successful")
            # Cleanup test record
            c.execute('DELETE FROM encryption_history WHERE operation_type = ?', ('Test',))
        else:
            print(f"❌ Database insert/select failed")
            return False
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🔧 Running functionality tests after fixes...\n")
    
    tests = [
        ("Triple DES Encryption/Decryption", test_triple_des),
        ("Key Management", test_key_management),
        ("Database Operations", test_database)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED\n")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED\n")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
