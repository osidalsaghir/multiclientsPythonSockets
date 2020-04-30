import socket
import sys
import pickle
from threading import Thread

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8888

def main():


    try:
        connection = soc.connect(('192.168.88.245', port))
        receiveMethode()



    except:
        print("Connection error")
        sys.exit()

   # print("Enter 'quit' to exit")
    #username = input("enter the name that you want to use  : ")
    #soc.sendall(username.encode("utf8"))




def receiveMethode():
    print(soc.recv(5120).decode("utf8").rstrip())
    Thread(target=sendMethode).start()
    while True:

        full_msg = b''
        new_msg = True
        while True:
            try:

                msg = soc.recv(10)
                if new_msg:
                    msglen = int(msg[:10])
                    new_msg = False

                full_msg += msg
                if len(full_msg) - 10 == msglen:
                    heShe = pickle.loads(full_msg[10:])

                    print(f"\nhe/she says : {heShe}\n")

                    new_msg = True
                    full_msg = b""

                    break

            except:
                try:
                    msg = pickle.loads(full_msg[10:])
                    print(f"\n{msg}\n")

                    break
                except:
                    print("an error occurred")
                    sys.exit(0)
                    break



def sendMethode():

    while True:
        theData =input("\nyou : --->>")
        if theData :
            soc.sendall(theData.encode("utf8"))





if __name__ == "__main__":
    main()










'''

the user should only get and send data and so the clients should only print the masseges form thes server and get the data .





'''

''' while True:
     full_msg = b''
     new_msg = True
     print("Main Menu :  \n press 0 to choose and communicate with ip : ")
     choose = input(" ->")
     if choose.isnumeric():
         soc.sendall(choose.encode("utf8"))
         while True:
             try:
                 msg = soc.recv(10)
                 if new_msg:
                     msglen = int(msg[:10])
                     new_msg = False

                 full_msg += msg
                 if len(full_msg) - 10 == msglen:
                     users = pickle.loads(full_msg[10:])
                     counter = 0
                     for user in users:
                         stringUser = str(counter) + " | " + user[0] + " | " + str(user[1])
                         print(stringUser)
                         counter = counter + 1
                     new_msg = True
                     full_msg = b""


                     break

             except:
                 try:
                     msg = pickle.loads(full_msg[10:])
                     print(msg)
                     break
                 except :
                     print("an error occurred")
                     break

     elif choose == "quit":
         soc.send(b'--quit--')
         break


     else:
         print("try again")
'''
