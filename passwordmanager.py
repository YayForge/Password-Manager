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


def send_email(admin_mail):
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
        email_password = "PASSWORDS"
        if email_password is None:
            raise ValueError("Email password not set in environment variables.")
        server.login("SENDER_MAIL", email_password)
        server.sendmail("SENDER_MAIL", admin_mail, message.as_string())
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
    finally:
        server.quit()
    return code


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


def show():
    if not os.path.exists('Passwords.bin'):
        print(Fore.RED + "No passwords stored yet." + Style.RESET_ALL)
        return

    with open('Passwords.bin', 'r') as file:
        data = file.readlines()

    for line in data:
        decode_data = base64.b64decode(line.strip()).decode('utf-8')
        print(decode_data)


def new(password, note):
    with open("Passwords.bin", "a") as file:
        index = sum(1 for _ in open('Passwords.bin', 'r'))
        new_data = f"{index + 1}-  {password}  <=>  {note}\n"
        file.write(base64.b64encode(new_data.encode('utf-8')).decode('utf-8') + '\n')


def remove():
    if not os.path.exists("Passwords.bin"):
        print(Fore.RED + "\nFile is empty!" + Style.RESET_ALL)
        time.sleep(3)
        return

    with open("Passwords.bin", "r") as file:
        lines = file.readlines()

    clear_screen()
    show()
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

    with open("Passwords.bin", "w") as file:
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


def create_or_load_admin_password():
    if os.path.exists("User_Data.bin"):
        with open("User_Data.bin", "r") as file:
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
                with open("User_Data.bin", "w") as file:
                    file.write(hashed_password + "\n" + hash_mail)
                print("Your password has been created successfully.")
                time.sleep(3)
                return hashed_password, admin_mail


def main():
    admin_password_hash, admin_mail = create_or_load_admin_password()
    verification_code = send_email(admin_mail)
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

                            print(Fore.RED + "1. Show passwords\n2. New password\n3. Remove password\n4. Reset key\n5. Quit" + Style.RESET_ALL)
                            mod = int(input(Fore.RED + "=> " + Style.RESET_ALL))
                            if mod == 1:
                                clear_screen()
                                show()
                                input("Press Enter to continue...")
                            elif mod == 2:
                                clear_screen()
                                enter_password = getpass.getpass("Enter the password you want to add: ")
                                enter_note = input("Enter a note regarding the password: ")
                                new(enter_password, enter_note)
                            elif mod == 3:
                                clear_screen()
                                remove()
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
                                            with open("User_Data.bin", "w") as file:
                                                file.write(admin_password_hash + "\n" + base64.b64encode(admin_mail.encode('utf-8')).decode('utf-8'))
                                            print("Your password has been updated.")
                                            time.sleep(3)
                                            break
                            elif mod == 5:
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
