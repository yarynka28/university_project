import os,hashlib
folder_path=input("Enter a path of a folder:")
print("Choose what would you like to do:")
print(f"1.Run an integrity check of a folder 1 time;\n2.Exit;")
decision='1'
hash_folder_path="D:/hash_folder/"
while decision != '2':
    decision=input("Enter your choice:")
    if decision=='1':
        not_changed=True
        for root,dirs,files in os.walk(folder_path):
            for a_file in files:
                if root==folder_path:
                    a_hasher=hashlib.new('ripemd160')
                    full_path_of_a_file=f"{root}{a_file}"
                    f=open(full_path_of_a_file,"rb")
                    content=f.read()
                    a_hasher.update(content)
                    file_hash=a_hasher.hexdigest()
                    f.close()
                    try:
                        f=open(f"{hash_folder_path}check_{a_file}","r")
                        file_hash_r=f.read()
                        if file_hash_r != file_hash:
                            print(f"Warning!File {full_path_of_a_file} has been changed.")
                            not_changed=False
                        f.close()
                    except:
                        f=open(f"{hash_folder_path}check_{a_file}","w+")
                        f.write(file_hash)
                        f.close()
                        file_names.append(f"check_{a_file}")
        if not_changed == True:
            print("Update: no files have been changed.")
    elif decision=='2':
        for root,dirs,files in os.walk(hash_folder_path):
            for a_file in files:
                if root==hash_folder_path:
                    for file_name in file_names:
                        if a_file == file_name:
                            try:
                                os.remove(f"{root}{a_file}")
                            except:
                                pass