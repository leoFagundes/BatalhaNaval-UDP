import socket
import random

ROWS, COLS = 10, 10
server_board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def can_place_ship(symbol, row, col, direction, size):
    if direction == 'horizontal':
        if col + size > COLS:
            return False
        for c in range(col, col + size):
            if server_board[row][c] != ' ':
                return False
    elif direction == 'vertical':
        if row + size > ROWS:
            return False
        for r in range(row, row + size):
            if server_board[r][col] != ' ':
                return False
    return True

def place_ships():
    ships = [(3, 1, 'S'), (2, 2, 'C'), (1, 3, 'P')]  # Submarino, Cruzador, Porta-aviões
    for qntd, size, symbol in ships:
        for _ in range(qntd):
            while True:
                row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
                direction = random.choice(['horizontal', 'vertical'])
                if can_place_ship(symbol, row, col, direction, size):
                    if direction == 'horizontal':
                        for c in range(col, col + size):
                            server_board[row][c] = symbol
                    elif direction == 'vertical':
                        for r in range(row, row + size):
                            server_board[r][col] = symbol
                    break

def print_board(board):
    print("\n   A B C D E F G H I J")
    for i, row in enumerate(board):
        if i + 1 < 10:
            print(f"0{i + 1} {' '.join(row)}")
        else:
            print(f"{i + 1} {' '.join(row)}")

def check_victory():
    for row in server_board:
        for cell in row:
            if cell not in [' ', '~', 'X']:
                return False
    return True

def restart_game():
    global server_board
    server_board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    place_ships()
    print("\nNovo jogo iniciado!")
    print_board(server_board)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
UDPServerSocket.bind((localIP, localPort))
print("Servidor Batalha Naval ativo e ouvindo...\n")

place_ships()
print_board(server_board)

def update_server_board(response, col, row):
    if "Erro - Acertou a Água!" in response:
        server_board[row][col] = '~'
    elif "Acerto - Acertou um navio!" in response:
        server_board[row][col] = 'X'
    print_board(server_board)

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    client_message = bytesAddressPair[0].decode()
    client_address = bytesAddressPair[1]

    try:
        col, row = ord(client_message[0].upper()) - ord('A'), int(client_message[1:]) - 1
        if 0 <= row < ROWS and 0 <= col < COLS:
            if server_board[row][col] == ' ':
                response = "Erro - Acertou a Água!"
            elif server_board[row][col] == '~':
                response = "Erro - Alvo já foi escolhido!"
            else:
                response = "Acerto - Acertou um navio!"
        else:
            response = "Posição inválida"
    except (ValueError, IndexError):
        response = "Formato inválido. Use uma letra seguida de um número (por exemplo, A5)."

    UDPServerSocket.sendto(response.encode(), client_address)
    if "Acerto" in response or "Erro" in response:
        update_server_board(response, col, row)

    if check_victory():
        response = "Você venceu! Deseja recomeçar o jogo? (sim/não)"
        UDPServerSocket.sendto(response.encode(), client_address)
        client_response, _ = UDPServerSocket.recvfrom(bufferSize)
        if client_response.strip().lower() == "sim":
            restart_game()
        else:
            print("Encerrando o jogo...")
            break
