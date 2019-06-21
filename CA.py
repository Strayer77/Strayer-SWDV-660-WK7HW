import socket

PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.bind(( socket.gethostname(), PORT ))

s.listen(5)

serverData = {
    "name" : "MyServer",
    "publicKey" : "publicKey1234567"
}
#serverName = serverData["name"]
#publicKey = serverData["publicKey"]

#going to listen to connections in while loop
while True:
    clientsocket, address = s.accept()
    print("Connection from ", address  ," has been established!")

    data = clientsocket.recv(1024)
    decoded_data = data.decode("utf-8")

    #if the message from client is the server name the server sends
    #message with the public key, if not - server says "Goodbye"
    if decoded_data == serverData["name"]:
        clientsocket.send(bytes(serverData["publicKey"], "utf-8"))
    else: 
        clientsocket.send(bytes("Goodbye", "utf-8"))

    clientsocket.close()
