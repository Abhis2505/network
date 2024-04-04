import socket

def server_program():
    host = '127.0.0.1'
    port = 55555
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        client_socket.send("Welcome to the server!".encode())
        client_socket.close()

if __name__ == '__main__':
    server_program()


# 1 ....

import socket

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 55555))
    server_socket.listen(2)
    client, address = server_socket.accept()
    print(f"Connection from {address} is established...")
    welcome = 'You are connected'
    client.send(welcome.encode())
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        print(f"From Client {address} : {data}")
        if data.lower().strip() == 'bye':
            print('\nClosing Connection ...')
            break
        data = input('-> ')
        client.send(data.encode())
    client.close()
    server_socket.close()

server_program()


# 2 ....      TCP
import socket

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 55555))
    server_socket.listen(2)
    print("Waiting for connection...")
    try:
        while True:
            client, address = server_socket.accept()
            print(f"Connection from {address} is established...")
            while True:
                data = client.recv(1024).decode()
                if not data:
                    break
                print(f"From Client {address}: {data}")  
                if data.strip().lower() == 'bye':
                    print("Closing connection...")
                    break
                data = input('-> ')
                client.send(data.encode())
            client.close()
           
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

server_program()


#################   UDP   ###################
import socket

server_ip = '127.0.0.1'
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

while True:
    data, client_address = server_socket.recvfrom(1024)
    msg = data.decode()
    if msg == 'exit':
        print(f"Closing Connection...")
        break
    print(f"Message from {client_address} : {msg}")
    server_socket.sendto(msg.encode(), client_address)

server_socket.close()



########################   chatroom   ##########################
import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345
count = 0
client_sockets = {}

server_socket.bind((host, port))
server_socket.listen(5)

def broadcast(msg, sender_socket):
    sender_address = client_sockets[sender_socket]
    for client in client_sockets:
        if client != sender_socket:
            client.send(f"{sender_address} : {msg}".encode())

def exit_broadcast(msg, sender_socket):
    for client in client_sockets:
        if client != sender_socket:
            client.send(f"{msg}".encode())

def handle_client(client_socket, client_address):
    client_sockets[client_socket] = client_address
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Data received from {client_address} : {data.decode()}")
        if data.decode() != 'exit':
            broadcast(data.decode(), client_socket)
        else:
            exit_msg = f"{client_address} has left the chatroom"
            print(exit_msg)
            exit_broadcast(exit_msg, client_socket)
            break
    client_socket.close()
    del client_sockets[client_socket]
    global count
    count -= 1
    print(f"Number of active clients : {count}")

max_clients = 5
while count < max_clients:
    client_socket, client_address = server_socket.accept()
    x = threading.Thread(target = handle_client, args = (client_socket, client_address))
    x.start()
    count += 1
    print(f"Number of active clients : {count}")

server_socket.close()


#################  TCP + UDP #################
import socket 
import select  
 
tcp_port = 12345 
udp_port = 12356

def tcp_client(client_socket): 
    data = client_socket.recv(1024) 
    if data.decode() != 'exit': 
        print(f"Received TCP data from {client_socket.getpeername()} : {data.decode('utf-8')}") 
        message = input("Server : ") 
        client_socket.send(message.encode('utf-8')) 
    elif data.decode() == 'exit': 
        print(f"TCP connection closed.") 
        client_socket.close() 

def udp_client(udp_socket): 
    data, addr = udp_socket.recvfrom(1024) 
    if data: 
        print(f"Received UDP data from {addr} : {data.decode('utf-8')}") 
        # udp_socket.sendto(b"Server received your UDP message", addr) 
        message = input("Server : ") 
        udp_socket.sendto(message.encode('utf-8'), addr) 

def start_server(): 
    tcp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) 
    tcp_socket.bind(('127.0.0.1', tcp_port)) 
    tcp_socket.listen(5) 
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
    udp_socket.bind(('127.0.0.1', udp_port)) 
    inputs = [tcp_socket, udp_socket] 
    print(f"Server listening on {'127.0.0.1'}...") 
    while True: 
        readable, _, _ = select.select(inputs, [], inputs) 
        for ready_socket in readable: 
            if ready_socket == tcp_socket: 
                client_socket, addr = tcp_socket.accept() 
                inputs.append(client_socket) 
                print(f"New TCP connection from {addr}") 
            elif ready_socket == udp_socket: 
                udp_client(udp_socket) 
            else: 
                tcp_client(ready_socket) 

start_server()


################## TIC-TAC-TOE ###################
import socket 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname(socket.gethostname())
port = 12345

server_socket.bind((host, port))

players = []

server_socket.listen(2)

print("Waiting for players...")
for i in range(2):
    player, addr = server_socket.accept()
    print('Connected with Player', i + 1, 'at', addr)
    players.append(player)
print("Both players have joined the game")
print("Player 1 - Symbol 'X' , Player 2 - Symbol 'O'")
print("Zero-based indexing is used for the board cells\n")
print("-------------------Game Start-------------------\n")

def display_board(board):
    return (
        board[0] + " | " + board[1] + " | " + board[2] + "\n" +
        "--+---+--\n" +
        board[3] + " | " + board[4] + " | " + board[5] + "\n" +
        "--+---+--\n" +
        board[6] + " | " + board[7] + " | " + board[8] + "\n\n"
    )

def check_win(board, mark):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]              
    ]
    for condition in win_conditions:
        if all(board[i] == mark for i in condition):
            return True
    return False

def play_game():
    board = [' ']*9
    turn = 0
    marks = ['X', 'O']
    first_move = True
    while True:
        player_index = turn % 2
        player = players[player_index]
        mark = marks[player_index]

        if first_move:
            for p in players:
                p.sendall(str.encode(display_board(board)))
                if p == player:    
                    p.sendall(str.encode("You are player {}\nYour symbol is {}\n".format(player_index + 1, mark)))
                else:
                    p.sendall(str.encode("You are player {}\nYour symbol is {}\n\n".format((player_index + 1) % 2 + 1, marks[(player_index + 1) % 2])))
            first_move = False
        
        for p in players:
            if p == player:
                p.sendall(str.encode("\n" + "-"*30 + "\nYour turn ({}): ".format(mark)))
            else:
                p.sendall(str.encode("-"*34 + "\nWaiting for the opponent's move...\n"))

        move = int(player.recv(1024).decode())
        if move < 0 or move > 8:
            player.sendall(str.encode("Invalid move! Try again.\n"))
            continue

        if board[move] == ' ':
            board[move] = mark
            for p in players:
                p.sendall(str.encode(display_board(board)))
            print("Player {} played move in cell {}\n".format(player_index + 1, move))
            print(display_board(board))
            print("=============================================")
            if check_win(board, mark):
                winner_index = player_index
                loser_index = (player_index + 1) % 2
                winner_mark = marks[winner_index]
                players[winner_index].sendall(str.encode("\n" + "="*25 + "\nCongratulations! You win!\n" + "="*25 + "\n"))
                players[loser_index].sendall(str.encode("\n" + "="*34 + "\nYou lose! Better luck next time...\n" + "="*34 + "\n"))
                print("     !!! Player {} wins".format(winner_index + 1) + " with symbol {} !!!".format(winner_mark))
                print("=============================================")
                break

            elif ' ' not in board:
                for p in players:
                    p.sendall(str.encode("It's a draw!\n"))
                break
            turn += 1
        else:
            player.sendall(str.encode("Invalid move! This cell is already occupied. Try a different move.\n"))

play_game()

for player in players:
    player.close()

print("\nGame Over, Server is closing...\n")
server_socket.close()