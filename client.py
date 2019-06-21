import socket
import time
from Crypto.Cipher import AES


#socket.AF_INET refers to IPv4 and socket.SOCK_STREAM refers to TCP
#defines our socket
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVERPORT = 9500
CA_PORT = 8080

#Connect to the Server
def serverConnect(portNumber, serverMessage):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #to make our connection to the server
    s.connect((socket.gethostname(), portNumber))

    full_msg = ''
    while True:
        s.sendall(bytes(serverMessage, "utf-8"))
        msg = s.recv(48)
        if len(msg) <= 0:
            break
        #prints our decoded message
        #print(msg.decode("utf-8"))
        full_msg += msg.decode("utf-8")

    s.close()
    return full_msg
    
    
#connect to the Certificate Authority
def CAConnect(portNumber, serverMessage):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #to make our connection to the server
    s.connect((socket.gethostname(), portNumber))

    full_msg = ''
    while True:
        s.sendall(bytes(serverMessage, "utf-8"))
        msg = s.recv(48)
        if len(msg) <= 0:
            break
        #prints our decoded message
        #print(msg.decode("utf-8"))
        full_msg += msg.decode("utf-8")

    s.close()
    return(full_msg)

#method to encrypt message using public key (PyCrypto)
def encrypt(publicKey, data):
    IV = b'1234567890ZYXWVU'
    cipher = AES.new(publicKey, AES.MODE_CFB, IV)
    msg = IV + cipher.encrypt(data)

    return msg

def decrypt(publicKey, encrypted):
    IV = b'1234567890ZYXWVU'
    cipher = AES.new(publicKey, AES.MODE_CFB, IV)
    msg = cipher.decrypt(encrypted)

    return msg
    

def main():
    while True:

        #connects us to our server initially to retrieve the server name
        serverName = serverConnect(SERVERPORT, "Hello")
        if len(serverName) != 0:
            print("Server Name retrieved: {0}".format(serverName))
            time.sleep(1)
            print("Checking name with Certificate Authority")
            time.sleep(.5)
            print('...')

            #connects to the certificate authority to check to see if name(which is the certificate) is legit
            #if so, returns with the server's public key
            publicKey = CAConnect(CA_PORT, serverName)
            if len(publicKey) != 0:
                time.sleep(1)
                print("Public Key retrieved: {0}".format(publicKey))
                time.sleep(1)
                print('...')

                #we then use the public key to encrypt message (session cipher key) and send
                #back to server for a response
                encryptedMessage = encrypt(publicKey, 'session cipher key')
                acknowledgement = serverConnect(SERVERPORT, str(encryptedMessage))    #sends in string format
                time.sleep(.5)
                print("Encrypted Message Sent.")
                time.sleep(1)
                print('...')

                
                #checks to see if returned encrypted acknowledgement matches what is expected
                if acknowledgement != 0:
                    print(str(acknowledgement))
                    time.sleep(.5)
                    print('Begin Data Transfer.')
                    break

                else:
                    print('No acknowledgement recieved.')
                    break
    
            
            else: 
                print("Could not retrieve the Public Key.")
                break

        else:
            print("Server name not received.")
            break

main()
