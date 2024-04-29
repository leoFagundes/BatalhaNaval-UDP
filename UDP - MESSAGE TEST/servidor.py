import socket

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Cria um socket datagrama
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Vincula ao endereço e IP
UDPServerSocket.bind((localIP, localPort))
print("Servidor UDP ativo e ouvindo...")

# Escuta por datagramas de entrada
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = f"Mensagem do Cliente: {message.decode()}"
    clientIP = f"Endereço IP do Cliente: {address}"
    print(clientMsg)
    print(clientIP)

    # Verifica se a mensagem é igual a "AA"
    if message.decode() == "AA":
        response = "Resposta correta!"
    else:
        response = "Resposta incorreta!"

    # Envia uma resposta de volta para o cliente
    UDPServerSocket.sendto(str.encode(response), address)
