import selectors
import socket
import types
from Tictactoe import Tictactoe
sel = selectors.DefaultSelector()
tic = Tictactoe()

tic.showBoard()
address_list = []

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
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        win = False
        if data.outb:
            if data.addr[0] == address_list[0]:
                win = tic.move('X', data.outb.decode())
            else:
                win = tic.move('O', data.outb.decode())

            if win:
                sent = sock.send(b'You win')  # Should be ready to write
                data.outb = data.outb[sent:]
                # addr2 = (address_list[1],65432)
                # data2 = types.SimpleNamespace(addr=addr2, inb=b'', outb=b'')
                # sent = sock.send(b'You Lose')  # Should be ready to write
                # data2.outb = data.outb[sent:]

            else:
                board = tic.showBoard().encode()
                sent = sock.send(board)  # Should be ready to write
                data.outb = data.outb[sent:]
            
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('10.55.76.78', 65432))
socket.listen()
conn, host = socket.accept()
address_list.append(host)
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
            
