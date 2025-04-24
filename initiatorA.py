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

# A has master key of A
keyA = b'BqTboPeUOaTaRXMfuBB9NtdCqGoDv7-2tkrH4BMZETg='

# Start client and connect to the KDC
kdc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kdc_address = ('127.0.0.1', 1234)
kdc_socket.connect(kdc_address)
print("Connected to KDC:", kdc_address,"\n")

# send IDA || IDB || N1 to KDC

idA = b'initiatorA'
idB = b'responderB'

# Generate a 16-byte (128-bit) nonce
nonce_send = secrets.token_bytes(16) 

# Create message
message = idA + b'||' + idB + b'||' + nonce_send
print("Message sending to KDC\n")
print(message)

# Send message to KDC
print("\nSending message to KDC\n")
total_bytes_sent = kdc_socket.send(message)

if total_bytes_sent == len(message):
    print("Message sent successfully.\n")
else:
    print("Failed to send message\n")
    
message = kdc_socket.recv(1024)
print("Receiving message from KDC\n")
print(message)

# Data processing
# Message = E(Ka, [Ks || IDA || IDB || N1]) || E(Kb, [Ks || IDA])
decoded_string = message.decode("latin-1")
m1_enc = decoded_string.split("||")[0]
m2_enc = decoded_string.split("||")[1]

# Decrypt the message KDC send to A
fernet = Fernet(keyA)

m1 = fernet.decrypt(m1_enc)

# Get the session key and nonce
m1 = m1.decode("latin-1").split("||")

session_key = m1[0].encode("latin-1")

# Verifying message from KDC - by nonce??
print("\nVerifying message from KDC ?\n")
nonce_recv = m1[3].encode("latin-1") 

if nonce_send == nonce_recv:
    print("The message is from KDC - Authentic !!!\n")
else:
    print("The message is fake!!!\n")
    
print(session_key)

kdc_socket.close()

print("\nA forwarding message from KDC to responder B\n")

# Start initiator and wait for a responder connection
initiator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
initiator_socket.bind(('0.0.0.0', 1234))
initiator_socket.listen(1)
print("Initiator started. Waiting for responder connection...\n")

responder_socket, responder_address = initiator_socket.accept()
print("Responder connected:", responder_address,"\n")

m2_enc = m2_enc.encode("latin-1")

responder_socket.send(m2_enc)

# Authentication steps
fernet_sskey = Fernet(session_key)

message = responder_socket.recv(1024)

message = fernet_sskey.decrypt(message)

message = f_nonce(message)

responder_socket.send(message.encode('latin-1'))

responder_socket.close()
initiator_socket.close()


