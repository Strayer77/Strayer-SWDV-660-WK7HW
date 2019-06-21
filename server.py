import socket
from Crypto.Cipher import AES

#socket.AF_INET refers to IPv4 and socket.SOCK_STREAM refers to TCP
#defines our socket
PORT = 9500
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binds socket, sets port to 
s.bind(( socket.gethostname(), PORT ))

s.listen(5)

serverData = {
    "name" : "MyServer",
    "publicKey" : "publicKey1234567"
}

def DataEncryptionCheck(publicKey, data):
    IV = b'1234567890ZYXWVU'
 
    cipher = AES.new(publicKey, AES.MODE_CFB, IV)
    msg = IV + cipher.encrypt(data)

    return msg

#going to listen to connections in while loop
while True:
    clientsocket, address = s.accept()
    print("Connection from ", address  ," has been established!")


    #what we use to check against encrypted data sent from client 
    #that was encrypted with public key info
    publicKey = serverData['publicKey']
    encryptedDataCheck = DataEncryptionCheck(publicKey, 'session cipher key')


    #our acknowledgement that is encrypted and sent back to client for final time
    encryptedReturnMessage = DataEncryptionCheck(publicKey, 'Session cipher acknowledged.')
    print(encryptedReturnMessage)

    data = clientsocket.recv(1024)
    decoded_data = data.decode("utf-8")



    #if the message from client is 'Hello' the server sends
    #message saying "Hi", if not - server says "Goodbye"
    if decoded_data == 'Hello':
        clientsocket.send(bytes("MyServer", "utf-8"))
    
    #if the encrypted data matches the data output by our own 
    #encryption function, this will send an acknowledgment
    elif decoded_data == str(encryptedDataCheck):
        clientsocket.send(bytes('Session Cipher Acknowledged', "utf-8"))

    else: 
        clientsocket.send(bytes("Goodbye", "utf-8"))

    clientsocket.close()

 