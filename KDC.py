import socket
from cryptography.fernet import Fernet

# KDC has master key of A and B
keyA = b'BqTboPeUOaTaRXMfuBB9NtdCqGoDv7-2tkrH4BMZETg='
keyB = b'u_ewiQtRQacaFm2ywSstStOLrZGjkWlwEm9Emy_jhys='

# Start KDC and wait for a client connection - initiator A
kdc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kdc_socket.bind(('0.0.0.0', 1234))
kdc_socket.listen(1)
print("KDC started. Waiting for client connection...\n")

client_socket, client_address = kdc_socket.accept()
print("Client connected:", client_address,"\n")

# -------- KDC receive a message from initiator A --------
print("Receiving message from initiator\n")
message = client_socket.recv(1024) #IDA || IDB || N
print(message)

# -------- Data processing --------
decoded_string = message.decode("latin-1")

# Generate a session key for A-B communication
session_key = Fernet.generate_key()

# Create message
m1 = session_key + b'||' + message                                              #[Ks || IDA || IDB || N1])
m2 = session_key + b'||' + decoded_string.split("||")[0].encode("latin-1")      #[Ks || IDA])

# Encrypt message
fernetA = Fernet(keyA)
fernetB = Fernet(keyB)

m1_enc = fernetA.encrypt(m1) #E(Ka, [Ks || IDA || IDB || N1])
m2_enc = fernetB.encrypt(m2) #E(Kb, [Ks || IDA])

print("\nMessage sending to initiator\n")
message = m1_enc + b'||' + m2_enc
print(message)

# -------- KDC respond to initiator A --------
print("\nResponding to initiator... \n")
client_socket.send(message)

print("Sending message...\n")
total_bytes_sent = client_socket.send(message)

if total_bytes_sent == len(message):
    print("Message sent successfully.\n")
else:
    print("Failed to send message\n")

client_socket.close()
kdc_socket.close()
