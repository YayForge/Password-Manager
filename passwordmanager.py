from colorama import Fore, Style
import os
import getpass
import time
import hashlib
import base64
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import threading
import sys

def send_email(admin_mail):
    global verification_code

    code = str(random.randint(100000, 999999))

    message = MIMEMultipart()
    message["From"] = "SENDER_MAIL"
    message["To"] = admin_mail
    message["Subject"] = "Account Verification Code"
    message.attach(MIMEText(f"""This email has been sent to you in response to your two-step verification request. Please use the following 6-digit code to verify your account:

    Verification Code: {code}

    This code is crucial for the security of your account and is valid for 10 minutes. If you did not make this request, please contact us immediately.

    Thank you,
    Byyay Support Team""", "plain"))

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        email_password = "PASSWORD"
        if email_password is None:
            raise ValueError("Email password not set in environment variables.")
        server.login("SENDER_MAIL", email_password)
        server.sendmail("SENDER_MAIL", admin_mail, message.as_string())
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
    finally:
        if 'server' in locals():
            server.quit()
    
    verification_code = code

def signature():
    signature = """
    ██████╗ ██╗   ██╗    ██╗   ██╗ █████╗ ██╗   ██╗
    ██╔══██╗╚██╗ ██╔╝    ╚██╗ ██╔╝██╔══██╗╚██╗ ██╔╝
    ██████╔╝ ╚████╔╝      ╚████╔╝ ███████║ ╚████╔╝ 
    ██╔══██╗  ╚██╔╝        ╚██╔╝  ██╔══██║  ╚██╔╝  
    ██████╔╝   ██║          ██║   ██║  ██║   ██║   
    ╚═════╝    ╚═╝          ╚═╝   ╚═╝  ╚═╝   ╚═╝  

    """
    print(signature)

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def show(path):
    if not os.path.exists(path):
        print(Fore.RED + "No passwords stored yet." + Style.RESET_ALL)
        return

    with open(path, 'r') as file:
        data = file.readlines()

    for line in data:
        decode_data = base64.b64decode(line.strip()).decode('utf-8')
        print(decode_data)

def new(password, note, path):
    if not os.path.exists(path):
        index = 0
    else:
        index = sum(1 for _ in open(path, 'r'))

    with open(path, "a") as file:
        new_data = f"{index + 1}-  {password}  <=>  {note}\n"
        file.write(base64.b64encode(new_data.encode('utf-8')).decode('utf-8') + '\n')

def remove(path):
    if not os.path.exists(path):
        print(Fore.RED + "\nFile is empty!" + Style.RESET_ALL)
        time.sleep(3)
        return

    with open(path, "r") as file:
        lines = file.readlines()

    clear_screen()
    show(path)
    lines_length = len(lines)

    while True:
        try:
            selected_line = int(input(Fore.RED + "\n\nSelect line to remove: " + Style.RESET_ALL))
            if selected_line > lines_length or selected_line <= 0:
                print(Fore.RED + "\nInvalid line number!" + Style.RESET_ALL)
            else:
                del lines[selected_line - 1]
                break
        except ValueError:
            print(Fore.RED + "\nInvalid input! Please enter a number." + Style.RESET_ALL)

    with open(path, "w") as file:
        for line in lines:
            file.write(line)

    print(Fore.GREEN + "\nLine removed successfully!" + Style.RESET_ALL)
    time.sleep(3)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def resetkey(current_password_hash):
    temp = 2
    while True:
        password = getpass.getpass("Password: ")
        if temp == 0:
            print("You have made too many wrong attempts.\nExiting...")
            time.sleep(3)
            return False
        if hash_password(password) != current_password_hash:
            temp -= 1
            print(Fore.RED + "Wrong Password!" + Style.RESET_ALL)
        else:
            print("Redirecting...")
            time.sleep(3)
            return True

def create_or_load_admin_password(user_path):
    if os.path.exists(user_path):
        with open(user_path, "r") as file:
            password = file.readline().strip()
            mail = base64.b64decode(file.readline().strip()).decode('utf-8')
        return password, mail
    else:
        while True:
            create_admin_password = getpass.getpass("Enter your new password: ")
            c_again_admin_password = getpass.getpass("Please re-enter: ")
            admin_mail = input("Enter your email: ")
            if create_admin_password != c_again_admin_password:
                print(Fore.RED + "Passwords do not match" + Style.RESET_ALL)
            else:
                hashed_password = hash_password(create_admin_password)
                hash_mail = base64.b64encode(admin_mail.encode('utf-8')).decode('utf-8')
                with open(user_path, "w") as file:
                    file.write(hashed_password + "\n" + hash_mail)
                print("Your password has been created successfully.")
                time.sleep(3)
                return hashed_password, admin_mail

def loading(duration=5):  
    start_time = time.time()  
    loading_text = "loading"
    
    while time.time() - start_time < duration:  
        for dots in range(4): 
            if time.time() - start_time >= duration:  
                break
            sys.stdout.write("\r" + loading_text + "." * dots + " " * (3 - dots))  
            sys.stdout.flush()  
            time.sleep(0.5)
    clear_screen()        

def path():
    appdata_path = os.getenv('LOCALAPPDATA')
    my_app_data_path = os.path.join(appdata_path, 'PasswordManager')

    if not os.path.exists(my_app_data_path):
        os.makedirs(my_app_data_path)

    user_data_path = os.path.join(my_app_data_path, 'User_Data.bin')
    password_data_path = os.path.join(my_app_data_path, 'Passwords.bin')

    return user_data_path, password_data_path, my_app_data_path

def reset_PM(user_path, passwords_path):
    os.system(f"powershell rm {user_path}")
    os.system(f"powershell rm {passwords_path}")
    os.system("cls")
    print(Fore.GREEN + "Resetting successful. Exiting the program..." + Style.RESET_ALL)
    time.sleep(3)
    sys.exit()

def open_directory(path):
    os.startfile(path)

def main():
    global verification_code
    verification_code = None
    user_data_path , passwords_path , directory_path= path()
    admin_password_hash, admin_mail = create_or_load_admin_password(user_data_path)
    send_email_background = threading.Thread(target=send_email, args=(admin_mail,))
    loading_background = threading.Thread(target=loading)
    loading_background.start()
    send_email_background.start()
    send_email_background.join()
    loading_background.join()
    temp = 3
    temp2 = 3
    while temp > 0:
        password = getpass.getpass("Password: ")
        if hash_password(password) == admin_password_hash:
            while temp2 > 0:
                input_code = input(f"Enter the 6-digit code sent to {admin_mail} :")
                if input_code == verification_code:
                    while True:
                        try:
                            clear_screen()
                            print("\u226f━" * 20 + "ྼ١ By YAY ١ྼ" + "\u2501≯" * 20)
                            signature()
                            print("\u226f━" * 20 + "ྼ١ By YAY ١ྼ" + "\u2501≯" * 20)
                            print(Fore.RED + "\nWELCOME TO PASSWORD MANAGER by YAY\n\n" + Style.RESET_ALL)

                            print(Fore.RED + "1. Show passwords\n2. New password\n3. Remove password\n4. Reset key\n5. Reset Program\n6. Open File Location\n7. Quit" + Style.RESET_ALL)
                            mod = int(input(Fore.RED + "=> " + Style.RESET_ALL))
                            if mod == 1:
                                clear_screen()
                                show(passwords_path)
                                input("Press Enter to continue...")
                            elif mod == 2:
                                clear_screen()
                                enter_password = getpass.getpass("Enter the password you want to add: ")
                                enter_note = input("Enter a note regarding the password: ")
                                new(enter_password, enter_note, passwords_path)
                            elif mod == 3:
                                clear_screen()
                                remove(passwords_path)
                            elif mod == 4:
                                clear_screen()
                                if resetkey(admin_password_hash):
                                    while True:
                                        new_admin_password = getpass.getpass("Enter your new password: ")
                                        again_admin_password = getpass.getpass("Please re-enter: ")

                                        if new_admin_password != again_admin_password:
                                            print(Fore.RED + "Passwords do not match" + Style.RESET_ALL)
                                        else:
                                            admin_password_hash = hash_password(new_admin_password)
                                            with open(user_data_path, "w") as file:
                                                file.write(admin_password_hash + "\n" + base64.b64encode(admin_mail.encode('utf-8')).decode('utf-8'))
                                            print("Your password has been updated.")
                                            time.sleep(3)
                                            break
                            elif mod == 5:
                                os.system("cls")
                                reset_PM(user_data_path, passwords_path)
                            elif mod == 6:
                                os.system("cls")
                                open_directory(directory_path)
                            elif mod == 7:
                                print("bye")
                                return
                            else:
                                print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
                                time.sleep(2)
                        except ValueError:
                            print(Fore.RED + "Invalid character" + Style.RESET_ALL)
                            time.sleep(2)
                else:
                    temp2 -= 1
                    print(Fore.RED + "Wrong Code!" + Style.RESET_ALL)
            temp = 0
        else:
            temp -= 1
            print(Fore.RED + "Wrong Password!" + Style.RESET_ALL)
    print("You have made too many wrong attempts.\nExiting...")
    time.sleep(3)


if __name__ == "__main__":
    main()
