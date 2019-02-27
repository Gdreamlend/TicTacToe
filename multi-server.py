import socket
import select
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('10.55.76.78', 65432))
sock.listen(2)

# lists of sockets to watch for input and output events
ins = [sock]
ous = []
# mapping socket -> data to send on that socket when feasible
data = {}
# mapping socket -> (host, port) on which the client is running
adrs = {}

try:
    while True:
        i, o, e = select.select(ins, ous, [])  # no excepts nor timeout
        for x in i:
            if x is sock:
                # input event on sock means client trying to connect
                newSocket, address = sock.accept(  )
                print( "Connected from", address)
                ins.append(newSocket)
                adrs[newSocket] = address
            else:
                # other input events mean data arrived, or disconnections
                newdata = x.recv(8192)
                if newdata:
                    # data arrived, prepare and queue the response to it
                    print(len(newdata), " bytes from " ,  adrs[x])
                    data[x] = data.get(x, '') + newdata.decode()
                    if x not in ous: ous.append(x)
                else:
                    # a disconnect, give a message and clean up
                    print ("disconnected from", adrs[x])
                    del adrs[x]
                    try: ous.remove(x)
                    except ValueError: pass
                    x.close(  )
        for x in o:
            # output events always mean we can send some data
            tosend = data.get(x).encode()
            if tosend:
                nsent = x.send(tosend)
                print(nsent, " bytes to" , adrs[x])
                # remember data still to be sent, if any
                tosend = tosend[nsent:]
            if tosend:
                data[x] = tosend
            else:
                try: del data[x]
                except KeyError: pass
                ous.remove(x)
                print("No data currently remain for", adrs[x])
finally:
    sock.close(  )