import socket
import sys
import traceback
from threading import Thread
import pickle



users = []


usersConnections = []


status = [] #if busy the number will be 0 and if not the number will be 1



def main():
    start_server()


def start_server():
    port = 8888         # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind(("192.168.88.245", port))

    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        print("form up there")

        ip, port = str(address[0]), str(address[1])

        users.append(address)
        usersConnections.append(connection)
        status.append(1)
        print("Connected with " + ip + ":" + port)

        try:

            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
            break

    soc.close()


def client_thread(connection, ip, port ,max_buffer_size = 5120 ):
    connection.sendall("Hello There ..... Welcome to our Server ..... ".encode("utf8"))

    busy = 1
    while busy == 1:
        print(status)
        client_input = receive_input(connection, max_buffer_size )

        if "--quit--" in client_input and busy ==1:
            print("Client is requesting to quit")
            connection.close()
            counter = 0
            for user in users:
                print(str(user[0]))
                print(f"( {ip} , {port})")
                if (str(user[1]) == str(port) and str(user[0]) == str(ip)):
                    users.pop(counter)
                    usersConnections.pop(counter)
                    status.pop(counter)
                    print(users)
                    break
                counter = counter + 1

            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        elif str(client_input).isnumeric() and busy ==1:
            if int(client_input) == 0 :
                sendUsers(connection)


            elif int(client_input) == 200 :
                theBusyList()

            else:
                index = int(client_input)-1
                connectionfound = usersConnections.__getitem__(index)
                print("connecting to " + str(users.__getitem__(index)))
                print(connectionfound)

                connectWithOtherClients(connectionfound , connection , max_buffer_size)



        elif busy ==1:
            print(client_input + " no not numeric")
        counter = 0
        for conn in usersConnections:
            if connection == conn :
                busy = int(status.__getitem__(counter))
                break
            counter = counter + 1



def sendUsers(connection):
    print(users[0][0])
    counter = 0
    list=""
    for user in  users:
        counter = counter+1
        list = list +  "\n "+str(counter)+"    |   "+str(user[0])+"  | "+str(user[1])

    msg = pickle.dumps(list)
    print(f"sending ...{list}")
    msg = bytes(f"{len(msg):<{10}}", 'utf-8') + msg
    connection.sendall(msg)


def receive_input(connection, max_buffer_size):



    result = ""

    choose = connection.recv(max_buffer_size).decode("utf-8").rstrip()
    result = choose

    return result



def connectWithOtherClients(connection1 , connection2 , max_buffer_size):

    message = "\nthis IP " + connection2.getsockname()[0] + " needs to contact with you do you want to accept this connection Y/N\n"

    msg = pickle.dumps(message)
    print(f"sending ...{message}")
    msg = bytes(f"{len(msg):<{10}}", 'utf-8') + msg
    connection1.sendall(msg)
    answer = connection1.recv(max_buffer_size).decode("utf-8").rstrip()
    if "yes" in answer :
        message = " \nthe ip has accepted the connection you can start the conversation with it ..\n"
        msg = pickle.dumps(message)
        print(f"sending ...{message}")
        msg = bytes(f"{len(msg):<{10}}", 'utf-8') + msg
        connection2.sendall(msg)

        index = 0
        for conn in usersConnections:
            if conn is connection1:
                break
            index = index + 1
        status.__setitem__(index,0)


        index2 = 0
        for conn in usersConnections:
            if conn is connection2:
                break
            index2 = index2 + 1
        status.__setitem__(index2,0)


        massegingtopeer(connection1, connection2, max_buffer_size)
        return 0

    if "no" in answer :
        message = " the ip has not accepted the connection"
        msg = pickle.dumps(message)
        print(f"sending ...{message}")
        msg = bytes(f"{len(msg):<{10}}", 'utf-8') + msg
        connection2.sendall(msg)
        return 0
    else:
        print("\nTry again error input")
        connectWithOtherClients(connection1, connection2, max_buffer_size) #recursive function
        return 0

def massegingpeer(connection1,connection2,max_buffer_size):
    try :

        while True :
            text = connection1.recv(max_buffer_size).decode("utf-8").rstrip()

            msg = pickle.dumps(text)
            print(f"sending ...{text}")
            msg = bytes(f"{len(msg):<{10}}", 'utf-8') + msg
            connection2.sendall(msg)
    except Exception as e :
            print(e)

def massegingtopeer(connection1,connection2,max_buffer_size):
    Thread(target=massegingpeer, args=(connection1, connection2, max_buffer_size)).start()
    try :
        while True:
            text = connection2.recv(max_buffer_size).decode("utf-8").rstrip()

            msg = pickle.dumps(text)
            print(f"sending ...{text}")
            msg = bytes(f"{len(msg):<{10}}", 'utf-8') + msg
            connection1.sendall(msg)
    except Exception as e:
        print(e)



def theBusyList() :
    counter = 0 
    for user in users :
        print(user[0])
        print(status[counter])
        counter = counter +1



if __name__ == "__main__":
    main()