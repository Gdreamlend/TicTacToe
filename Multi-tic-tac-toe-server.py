import selectors
import socket
import types
from Tictactoe import Tictactoe
sel = selectors.DefaultSelector()
tic = Tictactoe()

tic.showBoard()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print(recv_data)
            data.outb += recv_data
            #data.outb += "helllo"
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            board = tic.board.encode()
            #sent = sock.send(board)
            sent = sock.send(board)  # Should be ready to write
            data.outb = data.outb[sent:]
            
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('10.55.49.150', 65432))
socket.listen()
conn, host = socket.accept()
print("listening on", (host,65432))
socket.setblocking(False)
sel.register(socket, selectors.EVENT_READ, data=None)
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
            