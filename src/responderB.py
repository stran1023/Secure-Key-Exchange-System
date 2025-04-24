import socket
from cryptography.fernet import Fernet
import secrets
import hashlib

def f_nonce(nonce):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    
    # Update the hash object with the string
    nonce = nonce.decode('latin-1')
    hash_object.update(nonce.encode('utf-8'))
    
    # Get the hexadecimal representation of the hash digest
    hash_value = hash_object.hexdigest()

    return hash_value

# B has master key of B
keyB = b'u_ewiQtRQacaFm2ywSstStOLrZGjkWlwEm9Emy_jhys='

# Start client and connect to the initiator A
initiator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
initiator_address = ('127.0.0.1', 1234)
initiator_socket.connect(initiator_address)
print("Connected to initiator:", initiator_address,"\n")

# Receive the encrypted session key from the KDC
message = initiator_socket.recv(1024)

# Decrypt the message using the shared master key
fernet = Fernet(keyB)
m2 = fernet.decrypt(message)

# Get the session key and id of initiator
m2_decoded = m2.decode("latin-1")
session_key = m2_decoded.split("||")[0].encode("latin-1")

print("Getting the session key ... Done!!!")

#Authentication steps

fernet_sskey = Fernet(session_key)

# Generate a 16-byte (128-bit) nonce
nonce_send = secrets.token_bytes(16) 

# E(Ks, N2)
message = fernet_sskey.encrypt(nonce_send)

initiator_socket.send(message)

message = initiator_socket.recv(1024)

if message == f_nonce(nonce_send).encode('latin-1'):
    print("Authentication initiator done !!!\n")
    print("Connection is established !!!")

initiator_socket.close()
