import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 55555))
    message = client_socket.recv(1024)
    client_socket.close()
    print(message.decode())

if __name__ == '__main__':
    client_program()


# 1 ....
import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 55555))
    #print(client_socket.recv(1024).decode())
    message = input('-> ')
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        print(f"From Server : {data}")
        message = input('-> ')
        client_socket.send(message.encode())
    client_socket.close()

client_program()


################### UDP ####################
import socket

server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input('-> ')
    client_socket.sendto(msg.encode(), (server_ip, server_port))
    if msg == 'exit':
        print(f"Closing Client...")
        break
    response, server_address = client_socket.recvfrom(1024)
    print(f"Received Response : {response.decode()}")

client_socket.close()


###############  CHATROOM #################
import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345
client_socket.connect((host, port))

def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received from Server : {data.decode()}")
        except ConnectionAbortedError:
            break

x = threading.Thread(target = receive_messages)
x.start()

try:
    while True:
        message = input()
        client_socket.send(message.encode())
        if(message == 'exit'):
            break
except KeyboardInterrupt:
    pass

client_socket.close()



###################### TCP + UDP ######################

############   TCP   #############
import socket 
 
def tcp_client(): 
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) 
    client.connect(('127.0.0.1', 12345)) 
    while True: 
        message = input('TCP Client : ') 
        if message.lower()=='exit': 
            break 
        client.sendall(message.encode('utf-8')) 
        response = client.recv(1024) 
        print(f"Server : {response.decode('utf-8')}") 
 
    client.close() 
 
tcp_client()

########### UDP #############
import socket 
 
def udp_client(): 
    global client 
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 

    while True: 
        message = input("UDP Client : ") 
        if message.lower() == "exit": 
            break  
        client.sendto(message.encode('utf-8'), ("127.0.0.1", 12356)) 
        data, server_address = client.recvfrom(1024) 
        print(f"Server {server_address} : {data.decode('utf-8')}") 
    client.close() 
 
udp_client() 


####################### TIC-TAC-TOE ########################
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
client_socket.connect((host, port))

def display_board(board):
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")
    print(board[6] + " | " + board[7] + " | " + board[8])

def get_move():
    while True:
        try:
            move = int(input("Enter your move (0-8) : "))
            print("\n")
            if move < 0 or move > 8:
                print("Invalid move! Please enter a number between 0 and 8.")
            else:
                return move
        except ValueError:
            print("Invalid input! Please enter a number.")

def receive_message():
    while True:
        message = client_socket.recv(1024).decode()
        print(message)
        if "Your turn" in message:
            return
        elif "win" in message or "lose" in message:
            return True

game_over = False
while not game_over:
    game_over = receive_message()
    if game_over:
        break
    move = get_move()
    client_socket.sendall(str.encode(str(move)))

client_socket.close()