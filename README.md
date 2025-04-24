# Secure Key Exchange System

This project implements a **secure symmetric key exchange system** based on the **Needham-Schroeder Symmetric Key Protocol** using **Python socket programming** and **Fernet symmetric encryption**. The system includes an **Initiator (A)**, **Responder (B)**, and a **Key Distribution Center (KDC)** to securely distribute session keys and authenticate communication between two parties.

## 🚀 **Features**

- Implements **Needham-Schroeder Symmetric Key Protocol**.  
- Uses **Fernet encryption** for secure key distribution.  
- **Mutual authentication** via **nonce validation** and **SHA-256 hashing**.  
- Built with **Python socket programming** for network communication.

## 🛠 **Tech Stack**

- **Python 3**  
- **cryptography (Fernet)**  
- **hashlib (SHA-256)**  
- **socket programming (TCP/IP)**

## 📂 **File Structure**

| **File**           | **Description**                                      |
|--------------------|------------------------------------------------------|
| `initiatorA.py`    | Represents **A (Initiator)**. Requests session key from KDC, starts the connection with B. |
| `responderB.py`    | Represents **B (Responder)**. Connects to A, receives session key, and performs mutual authentication. |
| `KDC.py`           | **Key Distribution Center**. Generates session keys and securely distributes them to A and B. |

## 🔒 **Protocol Workflow**

1. **A requests a session key** from KDC for communication with B.  
2. **KDC generates a session key (Ks)** and securely distributes it to A and B using their respective **master keys (KA, KB)**.  
3. **A forwards the encrypted session key to B**.  
4. **B initiates mutual authentication** using a **nonce (N2)** encrypted with the session key.  
5. **A responds by hashing N2** and sending it back, completing authentication.

## 🔧 **How to Run**

1. Install required libraries:

```bash
pip install cryptography
```

2. Run the **KDC** server:

```bash
python KDC.py
```

3. In a separate terminal, run **initiatorA**:

```bash
python initiatorA.py
```

4. In another terminal, run **responderB**:

```bash
python responderB.py
```

## 📜 **License**

This project is for **educational purposes only**.

