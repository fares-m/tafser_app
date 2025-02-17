import os
import datetime

with open("pid.txt" , 'r') as file :
    pid = int(file.read())
try :
    os.system('del pid.txt')
    os.kill(pid , 15)
    with open("log.txt" , 'a') as file :file.write(f"[+] {datetime.datetime.now()} | Server is shut down.\n")
except Exception as e :
    with open("Error_log.txt" , 'a') as file :file.write(f"[+] {datetime.datetime.now()} | Could not shut down the Server.\n")

