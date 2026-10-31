
import os
import getpass
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# Configuration
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
ITERATIONS = 600_000

MAGIC = b"AESFILE1"


def derive_key(password, salt):
    """Derive a 256-bit encryption key from the password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))



def encrypt_file(file_path, password):
    """Encrypt a file and save it with the .aes extension."""
    source = Path(file_path)

    if not source.is_file():
        raise FileNotFoundError("The selected file does not exist.")

    if source.suffix.lower() == ".aes":
        raise ValueError("This file already has the .aes extension.")

    output_path = Path(str(source) + ".aes")

    if output_path.exists():
        raise FileExistsError(
            f"{output_path} already exists. Rename it before encrypting."
        )

    plaintext = source.read_bytes()

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, MAGIC)

    encrypted_data = MAGIC + salt + nonce + ciphertext

    # Create a new file without overwriting an existing file.
    with output_path.open("xb") as output_file:
        output_file.write(encrypted_data)

    print("\nEncryption successful!")
    print(f"Encrypted file: {output_path}")

    return output_path




def decrypt_file(file_path, password):
    """Decrypt a file created by this program."""
    source = Path(file_path)

    if not source.is_file():
        raise FileNotFoundError(
            "The selected encrypted file does not exist."
        )

    encrypted_data = source.read_bytes()
    header_size = len(MAGIC) + SALT_SIZE + NONCE_SIZE

    if len(encrypted_data) < header_size + 16:
        raise ValueError("The encrypted file is incomplete or invalid.")

    if not encrypted_data.startswith(MAGIC):
        raise ValueError("This file was not created by this program.")

    position = len(MAGIC)
    salt = encrypted_data[position:position + SALT_SIZE]
    position += SALT_SIZE

    nonce = encrypted_data[position:position + NONCE_SIZE]
    position += NONCE_SIZE

    ciphertext = encrypted_data[position:]
    key = derive_key(password, salt)

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, MAGIC)

    if source.suffix.lower() == ".aes":
        output_path = source.with_suffix("")
    else:
        output_path = Path(str(source) + ".decrypted")

    if output_path.exists():
        raise FileExistsError(
            f"{output_path} already exists. Rename it before decrypting."
        )

    # Create a new file without overwriting an existing file.
    with output_path.open("xb") as output_file:
        output_file.write(plaintext)

    print("\nDecryption successful!")
    print(f"Decrypted file: {output_path}")

    return output_path




def main():
    print("\n=== AES-256 File Encryption System ===")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Exit")

    choice = input("\nChoose an option (1-3): ").strip()

    if choice == "3":
        print("Exiting program.")
        return

    if choice not in ("1", "2"):
        print("Invalid choice. Please select 1, 2, or 3.")
        return

    file_path = input("Enter the full path of the file: ").strip()
    file_path = file_path.strip('"')

    password = getpass.getpass("Enter your password: ")

    if not password:
        print("Password cannot be empty.")
        return

    try:
        if choice == "1":
            encrypt_file(file_path, password)
        else:
            decrypt_file(file_path, password)

    except InvalidTag:
        print(
            "\nDecryption failed: Incorrect password "
            "or the encrypted file has been modified."
        )

    except FileNotFoundError:
        print("\nError: The selected file was not found.")

    except FileExistsError as error:
        print(f"\nError: {error}")

    except (ValueError, OSError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()

   