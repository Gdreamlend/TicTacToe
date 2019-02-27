import socket
import sys
import time
import select


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('10.55.49.150', 65432)
print('connecting to %s port %s' , server_address)
sock.connect(server_address)


time.sleep(1)

messages = [b'0'
            ]

try:
    # Look for the response
    mysocket.setblocking(0)

    ready = select.select([mysocket], [], [], timeout_in_seconds)
    if ready[0]:
        data = mysocket.recv(4096)
    amount_received = 0
    # Send data
    while amount_received < 10:

        messages[0] = input("Please choose the number where you will move to:").encode()
        print('sending ' , messages[0])
        sock.sendall(messages[0])
        data = sock.recv(1024)
        amount_received += len(data)
        print(data.decode())
        time.sleep(1.5)


finally:
    print("finished")
#     print(sys.stderr, 'closing socket')
#     sock.close()