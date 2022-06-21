# from Crypto.Cipher import DES3
# from Crypto import Random
# key = b'Sixteen byte key'
# iv = Random.new().read(DES3.block_size) #DES3.block_size==8
# cipher_encrypt = DES3.new(key, DES3.MODE_CBC, iv)
# plaintext = b'Gorodietska Yaryna Tarasivna    ' #padded with spaces so than len(plaintext) is multiple of 8
# encrypted_text = cipher_encrypt.encrypt(plaintext)
# print(encrypted_text)
# cipher_decrypt = DES3.new(key, DES3.MODE_CBC, iv) #you can't reuse an object for encrypting or decrypting other data with the same key.
# decrypted_text=cipher_decrypt.decrypt(encrypted_text)
# print(decrypted_text)




#
# from tkinter import *
# from tkinter import messagebox
# from twilio.rest import Client
#
# import hashlib
# import time
# import os
#
# root = Tk()
# width_of_window = 200
# height_of_window = 100
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
#
# x = (screen_width / 2) - (width_of_window / 2)
# y = (screen_height / 2) - (height_of_window / 2)
# root.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x, y))
#
#
# def hash(filename, list_hash):
#     with open(filename, "rb") as f:
#         bytes = f.read()  # read entire file as bytes
#         a_hasher = hashlib.new('ripemd160')
#         readable_hash = a_hasher.hexdigest()
#     list_hash.append(readable_hash)
#
#
# def reverse_hash(list_hash):
#     global path
#     path_list = []
#     for (dirpath, _, filenames) in os.walk(path):
#         for f in filenames:
#             abs_file_path = os.path.join(dirpath, f)
#             path_list += [abs_file_path]
#             hash(abs_file_path, list_hash)
#     return path_list
#
#
# def mainloop():
#     root.title("Path")
#
#     Label(root, text="Enter path of directory:").grid(row=0, column=0, sticky="w")
#     Entry(root, textvariable=path_input).grid(row=1, padx=5, pady=5)
#
#     Button(root, text="Start", command=main).grid(row=2, sticky="n")
#
#
# def message_window():
#     global path, list1
#     message_box = Toplevel(root)
#     message_box.title("Information")
#     message_box.geometry('350x300+600+300')
#     message_text = Text(message_box, wrap='word')
#
#     scrollbar = Scrollbar(message_text)
#     message_text.configure(yscrollcommand=scrollbar.set)
#     message_text.pack(side=LEFT, expand='yes', fill='both')
#     scrollbar.config(command=message_text.yview)
#     scrollbar.pack(side=RIGHT, fill=Y)
#
#     def message_info():
#         global path, list1
#         list2 = []
#         path_list = reverse_hash(list2)
#         for i in range(len(path_list)):
#             if list1[i] == list2[i]:
#                 message_text.insert(END, "File {} is integrity\n".format(path_list[i]))
#             else:
#                 message_text.insert(END, "File {} was added,changed or removed\n".format(path_list[i]))
#                 SMS(path_list, i)
#                 list1 = []
#                 reverse_hash(list1)
#         value = 0
#         stop = 1000
#         if value <= stop:
#             root.after(3000, message_info)
#             value += 1
#
#     message_info()
#
#
# def SMS(path_list, i):
#     account_sid = 'AC499887d2611b4e9c03c93624f8879f68'
#     auth_token = '30603030aa1113047ee5594142f31f64'
#     client = Client(account_sid, auth_token)
#
#     message = client.messages \
#         .create(
#         body='File {} was changed or removed'.format(path_list[i]),
#         from_='+380945728186',
#         to='+380996313348'
#     )
#
#     print(message.sid)
#
#
# def main():
#     global path, list1
#     path = path_input.get()
#     reverse_hash(list1)
#     message_window()
#
#
# path_input = StringVar()
# list1 = []
# path = ""
# mainloop()
# root.mainloop()



import PySimpleGUI as sg
import hashlib
import os
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

password_to_authenfification = "Control_work"





def hash(directory, path):
    for file in directory:
        hash = hashlib.sha256()
        full_path = ''
        full_path = path + '/' + file
        list_hash = list()
        with open(full_path, 'rb') as hash_file:  # opening the file one line at a time for memory considerations

            while True:
                data = hash_file.read(8192)

                if not data:
                    break
                hash.update(data)
            list_hash.append(hash.hexdigest())
            hash = None
    return list_hash


def create_main_vindow():
    layout = [
        [sg.Text('Виберіть директорію'), sg.InputText(), sg.FolderBrowse('Пошук')],
        [sg.Output(size=(88, 20))],
        [ sg.Cancel('Вийти', key='Cancel'), sg.Button('Розпочати монітор', key='Start')]
    ]

    window = sg.Window('Перевірка хеш сум', layout)
    directory_path = None
    directory = None
    start_list = None
    current_list = None
    start_track = False

    # The Event Loop
    while True:
        event, values = window.read(timeout=1800, timeout_key='TIMEOUT_KEY')
        # print(event, values) #debug
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Start':
            print(values[0])

            directory_path = values[0]
            directory = os.listdir(values[0])

            start_list = hash(directory, directory_path)

        if event == 'Start':
            start_track = True

        if event == 'TIMEOUT_KEY':
            if start_track:
                current_list = hash(directory, directory_path)
                print('have been checked')
                if not (current_list == start_list):
                    print('Alert')
                    start_track = False

    window.close()


layout_AUT = [
    [sg.Text('Введіть пароль:'), sg.InputText()],
    [sg.Submit('Авторизуватися', key='Submit'), sg.Cancel('Вийти', key='Cancel')]
]

window_AUT = sg.Window('Авторизація', layout_AUT)

# The Event Loop
while True:
    event, values = window_AUT.read()

    if event in (None, 'Exit', 'Cancel'):
        break

    if event == 'Submit':
        pass_inp = values[0]

        if pass_inp == password_to_authenfification:
            window_AUT.close()
            create_main_vindow()
        else:
            window_AUT.close()






import os, hashlib
import PySimpleGUI as sg
from twilio.rest import Client


def create_layout_for_authentification():
    password_to_authentification = "Control_work"
    layout_authentification = [
        [sg.Text('Введіть пароль'), sg.InputText()],
        [sg.Submit('Увійти', key='Submit'), sg.Cancel('Вийти', key='Exit')]
    ]
    window_authentification = sg.Window('Авторизація', layout_authentification)
    while True:
        event, values = window_authentification.read()

        if event in (None, 'Exit'):
            break

        if event == 'Submit':
            pass_inp = values[0]

            if pass_inp == password_to_authentification:
                window_authentification.close()
                main_window()
            else:
                window_authentification.close()


def check_file(directory, path):
    for file in directory:
        hash = hashlib.new('ripemd160')
        full_path_to_file = path + '/' + file
        hash_l = list()
        with open(full_path_to_file, 'rb') as hash_file:

            while True:
                data = hash_file.read()

                if not data:
                    break
                hash.update(data)
            hash_l.append(hash.hexdigest())
    return hash_l


def main_window():
    layout = [
        [sg.Text('Ввeдіть шлях до папки:'), sg.InputText()],
        [sg.Output(size=(65, 20))],
        [ sg.Button('Розпочати сканування', key='Start'), sg.Cancel('Вийти', key='Exit')]
    ]

    window = sg.Window('Перевірка цілісності', layout)
    # directory = None
    # directory_path = None
    # start_list = []
    # start_of_scanning = False
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        if event == 'Start':
            print(values[0])
            directory_path = values[0]
            directory = os.listdir(values[0])
            start_list = check_file(directory, directory_path)
            current_list = check_file(directory, directory_path)
            if (current_list == start_list):
                print('Файли є цілісними')
            else :
                print('Увага.Файли були змінені!')
                send_SMS(directory_path)
    window.close()


def send_SMS(file_path):
    account_sid = 'AC499887d2611b4e9c03c93624f8879f68'
    auth_token = '30603030aa1113047ee5594142f31f64'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='File {} was changed or removed'.format(file_path),
        from_='+13862040179',
        to='+380996313348'
    )
    print(message.sid)

create_layout_for_authentification()