from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os
import json
import argparse

class TripleDESCipher:
    def __init__(self):
        self.key = None
        self.iv = None
        # Use relative path for key file
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.key_file = os.path.join(project_root, 'secure_keys', 'secure_keys.json')

    def generate_key(self):
        """Generate a secure Triple DES key with proper parity"""
        self.key = DES3.adjust_key_parity(get_random_bytes(24))
        self.iv = get_random_bytes(8)  # Initialization vector for CBC mode
        return self.key, self.iv

    def encrypt_data(self, data):
        """Encrypt data using Triple DES in CBC mode"""
        try:
            if not isinstance(data, bytes):
                data = data.encode()
            
            if not self.key or not self.iv:
                raise ValueError("Key and IV must be generated first")

            cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
            padded_data = pad(data, DES3.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            
            # Combine IV and encrypted data for storage/transmission
            return base64.b64encode(self.iv + encrypted_data)
        
        except Exception as e:
            raise Exception(f"Encryption error: {str(e)}")

    def decrypt_data(self, encrypted_data):
        """Decrypt data using Triple DES in CBC mode"""
        try:
            if not self.key:
                raise ValueError("Key must be provided or generated first")

            # Decode and extract IV and ciphertext
            raw_data = base64.b64decode(encrypted_data)
            use_iv = raw_data[:8]
            ciphertext = raw_data[8:]

            cipher = DES3.new(self.key, DES3.MODE_CBC, use_iv)
            decrypted_data = cipher.decrypt(ciphertext)
            return unpad(decrypted_data, DES3.block_size)

        except Exception as e:
            raise Exception(f"Decryption error: {str(e)}")

    def encrypt_file(self, input_file, output_file):
        """Encrypt a file using Triple DES"""
        try:
            with open(input_file, 'rb') as f:
                file_data = f.read()
            
            encrypted_data = self.encrypt_data(file_data)
            
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        except Exception as e:
            raise Exception(f"File encryption error: {str(e)}")

    def decrypt_file(self, input_file, output_file):
        """Decrypt a file using Triple DES"""
        try:
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.decrypt_data(encrypted_data)
            
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            return True
        except Exception as e:
            raise Exception(f"File decryption error: {str(e)}")

    def save_key(self, key_name):
        """Save key and IV to a secure file"""
        if not self.key or not self.iv:
            raise ValueError("Key and IV must be generated first")
        
        key_data = {
            key_name: {
                "key": base64.b64encode(self.key).decode(),
                "iv": base64.b64encode(self.iv).decode()
            }
        }
        
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'r') as f:
                    existing_data = json.load(f)
                existing_data.update(key_data)
            else:
                existing_data = key_data

            with open(self.key_file, 'w') as f:
                json.dump(existing_data, f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving key: {str(e)}")

    def load_key(self, key_name):
        """Load key and IV from secure storage"""
        try:
            with open(self.key_file, 'r') as f:
                key_data = json.load(f)
                if key_name in key_data:
                    self.key = base64.b64decode(key_data[key_name]["key"])
                    self.iv = base64.b64decode(key_data[key_name]["iv"])
                    return True
                return False
        except FileNotFoundError:
            return False
        except Exception as e:
            raise Exception(f"Error loading key: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Triple DES Encryption/Decryption Tool - Professional CLI Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encrypt a file:
    python triple_des_example.py --action encrypt --input document.pdf

  Decrypt a file:
    python triple_des_example.py --action decrypt --input encrypted_doc.bin --key-name a1b2c3d4e5f6g7h8

  Encrypt text:
    python triple_des_example.py --action encrypt --input "Hello World" --text

  Decrypt text:
    python triple_des_example.py --action decrypt --input "base64_text" --text --key-name a1b2c3d4e5f6g7h8

Note: The Key ID is automatically generated during encryption and displayed in the output.
      Save this Key ID securely - you'll need it for decryption!
        """)

    parser.add_argument('--action', choices=['encrypt', 'decrypt'], required=True,
                      help='Action to perform: encrypt or decrypt')
    parser.add_argument('--input', required=True,
                      help='Input file path or text to process')
    parser.add_argument('--output',
                      help='Output file path (optional, auto-generated if not specified)')
    parser.add_argument('--text', action='store_true',
                      help='Treat input as text instead of file')
    parser.add_argument('--key-name',
                      help='16-character Key ID for decryption (generated automatically for encryption)')

    args = parser.parse_args()
    cipher = TripleDESCipher()

    try:
        if args.action == 'encrypt':
            # Generate new key and save with unique key ID
            cipher.generate_key()

            # Generate unique key ID (16 characters)
            key_id = os.urandom(8).hex()
            cipher.save_key(key_id)

            if args.text:
                # Encrypt text
                encrypted = cipher.encrypt_data(args.input)
                if args.output:
                    with open(args.output, 'wb') as f:
                        f.write(encrypted)
                    print("=" * 60)
                    print("SUCCESS: TEXT ENCRYPTION COMPLETED!")
                    print("=" * 60)
                    print(f"Output file: {args.output}")
                    print(f"Key ID: {key_id}")
                    print("=" * 60)
                    print("IMPORTANT: Save this Key ID to decrypt your file later!")
                    print("=" * 60)
                else:
                    print("=" * 60)
                    print("SUCCESS: TEXT ENCRYPTION COMPLETED!")
                    print("=" * 60)
                    print(f"Encrypted text (base64): {encrypted.decode()}")
                    print(f"Key ID: {key_id}")
                    print("=" * 60)
                    print("IMPORTANT: Save this Key ID to decrypt your text later!")
                    print("=" * 60)
            else:
                # Encrypt file
                output_file = args.output or f"{args.input}.encrypted"
                cipher.encrypt_file(args.input, output_file)

                # Display success message with key
                print("=" * 60)
                print("SUCCESS: FILE ENCRYPTION COMPLETED!")
                print("=" * 60)
                print(f"Original file: {args.input}")
                print(f"Encrypted file: {output_file}")
                print(f"Key ID: {key_id}")
                print("=" * 60)
                print("IMPORTANT: Save this Key ID to decrypt your file later!")
                print("Store it securely - you cannot decrypt without it!")
                print("=" * 60)

        else:  # decrypt
            if not args.key_name:
                print("=" * 60)
                print("ERROR: DECRYPTION FAILED!")
                print("=" * 60)
                print("Error: Key ID is required for decryption")
                print("Usage: --key-name YOUR_16_CHARACTER_KEY_ID")
                print("=" * 60)
                return

            if not cipher.load_key(args.key_name):
                print("=" * 60)
                print("ERROR: DECRYPTION FAILED!")
                print("=" * 60)
                print(f"Error: Key ID '{args.key_name}' not found")
                print("Make sure you have the correct 16-character Key ID")
                print("Check your saved keys or operation history")
                print("=" * 60)
                return

            try:
                if args.text:
                    # Decrypt text
                    decrypted = cipher.decrypt_data(args.input.encode())
                    if args.output:
                        with open(args.output, 'wb') as f:
                            f.write(decrypted)
                        print("=" * 60)
                        print("SUCCESS: TEXT DECRYPTION COMPLETED!")
                        print("=" * 60)
                        print(f"Decrypted file: {args.output}")
                        print(f"Key ID used: {args.key_name}")
                        print("=" * 60)
                    else:
                        print("=" * 60)
                        print("SUCCESS: TEXT DECRYPTION COMPLETED!")
                        print("=" * 60)
                        print(f"Decrypted text: {decrypted.decode()}")
                        print(f"Key ID used: {args.key_name}")
                        print("=" * 60)
                else:
                    # Decrypt file
                    if args.output:
                        output_file = args.output
                    else:
                        # Auto-generate output filename based on input with decrypted_ prefix
                        input_name = os.path.basename(args.input)
                        if input_name.startswith('encrypted_') and input_name.endswith('.bin'):
                            # Web app format: encrypted_filename.ext.bin -> decrypted_filename.ext
                            original_name = input_name[10:-4]  # Remove 'encrypted_' and '.bin'
                            output_file = f"decrypted_{original_name}"
                        else:
                            # CLI format: filename.encrypted or filename.bin -> decrypted_filename
                            clean_name = input_name.replace('.encrypted', '').replace('.bin', '')
                            output_file = f"decrypted_{clean_name}"

                        # Use the directory of the input file for output
                        output_file = os.path.join(os.path.dirname(args.input), output_file)

                    cipher.decrypt_file(args.input, output_file)

                    print("=" * 60)
                    print("SUCCESS: FILE DECRYPTION COMPLETED!")
                    print("=" * 60)
                    print(f"Encrypted file: {args.input}")
                    print(f"Decrypted file: {output_file}")
                    print(f"Key ID used: {args.key_name}")
                    print("=" * 60)
                    print("Your file has been successfully decrypted!")
                    print("=" * 60)
            except Exception as e:
                print("=" * 60)
                print("ERROR: DECRYPTION FAILED!")
                print("=" * 60)
                print(f"Error: {e}")
                print("Check if the file path and Key ID are correct")
                print("Ensure the file was encrypted with this system")
                print("=" * 60)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()