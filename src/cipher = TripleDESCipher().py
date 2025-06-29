cipher = TripleDESCipher()
key, iv = cipher.generate_key()
cipher.save_key("my_secure_key")