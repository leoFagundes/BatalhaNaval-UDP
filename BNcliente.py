import socket

ROWS, COLS = 10, 10

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def print_client_board(board):
    print("\n   A B C D E F G H I J")
    for i, row in enumerate(board):
        if i + 1 < 10:
            print(f"0{i + 1} {' '.join(row)}")
        else:
            print(f"{i + 1} {' '.join(row)}")

client_board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def update_board(response, user_input):
    row = int(user_input[1:]) - 1
    col = ord(user_input[0].upper()) - ord('A')
    if "Acerto - Acertou um navio!" in response:
        client_board[row][col] = 'X'
    elif "Erro - Acertou a Água!" in response:
        client_board[row][col] = '~'

while True:
    user_input = input("Digite uma posição (por exemplo, A5) ou 'sair' para encerrar: ")
    if user_input.lower() == "sair":
        break
    UDPClientSocket.sendto(user_input.encode(), serverAddressPort)
    response, _ = UDPClientSocket.recvfrom(bufferSize)
    print(response.decode())
    update_board(response.decode(), user_input)
    print_client_board(client_board)

UDPClientSocket.close()
