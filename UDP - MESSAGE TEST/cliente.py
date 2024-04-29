import socket

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

# Cria um socket UDP no lado do cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Envia para o servidor usando o socket UDP criado
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# Recebe a resposta do servidor
msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
print(f"Mensagem do Servidor: {msgFromServer.decode()}")

# Permite que o cliente faça tentativas infinitas até digitar "sair"
while True:
    user_input = input("Digite uma mensagem ('sair' para encerrar): ")
    if user_input.lower() == "sair":
        break
    UDPClientSocket.sendto(str.encode(user_input), serverAddressPort)
    msgFromServer, _ = UDPClientSocket.recvfrom(bufferSize)
    print(f"Mensagem do Servidor: {msgFromServer.decode()}")

# Fecha o socket do cliente
UDPClientSocket.close()
