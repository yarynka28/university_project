# import os,hashlib
# folder_path=input("Enter a path of a folder:")
# print("Choose what would you like to do:")
# print(f"1.Run an integrity check of a folder 1 time;\n2.Exit;")
# decision='1'
# hash_folder_path="D:/hash_folder/"
# while decision != '2':
#     decision=input("Enter your choice:")
#     if decision=='1':
#         not_changed=True
#         for root,dirs,files in os.walk(folder_path):
#             for a_file in files:
#                 if root==folder_path:
#                     a_hasher=hashlib.new('ripemd160')
#                     full_path_of_a_file=f"{root}{a_file}"
#                     f=open(full_path_of_a_file,"rb")
#                     content=f.read()
#                     a_hasher.update(content)
#                     file_hash=a_hasher.hexdigest()
#                     f.close()
#                     try:
#                         f=open(f"{hash_folder_path}check_{a_file}","r")
#                         file_hash_r=f.read()
#                         if file_hash_r != file_hash:
#                             print(f"Warning!File {full_path_of_a_file} has been changed.")
#                             not_changed=False
#                         f.close()
#                     except:
#                         f=open(f"{hash_folder_path}check_{a_file}","w+")
#                         f.write(file_hash)
#                         f.close()
#                         file_names.append(f"check_{a_file}")
#         if not_changed == True:
#             print("Update: no files have been changed.")
#     elif decision=='2':
#         for root,dirs,files in os.walk(hash_folder_path):
#             for a_file in files:
#                 if root==hash_folder_path:
#                     for file_name in file_names:
#                         if a_file == file_name:
#                             try:
#                                 os.remove(f"{root}{a_file}")
#                             except:
#                                 pass
import os, hashlib
import PySimpleGUI as sg
from twilio.rest import Client


def create_layout_for_authentification():
    password_to_authentification = "Control_work"
    layout_authentification = [
        [sg.Text('Введіть пароль'), sg.InputText()],
        [sg.Submit('Увійти', key='Submit')]
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
    directory = None
    directory_path = None
    start_list = []
    start_of_scanning = False
    while True:
        event, values = window.read(timeout=5000, timeout_key='timeout_key')
        if event in (None, 'Exit'):
            break
        if event == 'Start':
            print(values[0])
            directory_path = values[0]
            directory = os.listdir(values[0])
            start_list = check_file(directory, directory_path)
            start_of_scanning = True
        if event == 'timeout_key':
            if start_of_scanning:
                current_list = check_file(directory, directory_path)
                if (current_list == start_list):
                    print('Файли є цілісними')
                else:
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