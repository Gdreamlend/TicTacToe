import socket
import selectors
import types
sel = selectors.DefaultSelector()

HOST = '10.55.49.150'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


messages = [b'0', b'00']
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print(recv_data.decode())
            #print('received', repr(recv_data.decode()), 'from connection', data.connid)
            data.recv_total += len(recv_data)
            data.messages[0] = input("Please choose the number where you will move to:").encode()
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.messages[0] = input("Please choose the number where you will move to:").encode()
            data.outb = data.messages[0]
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
#
def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print('starting connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(m) for m in messages),
                                     recv_total=0,
                                     messages=list(messages),
                                     outb=b'')
        sel.register(sock, events, data=data)
start_connections(HOST,PORT,2)


while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        service_connection(key, mask)
