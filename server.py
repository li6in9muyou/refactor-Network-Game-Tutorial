import socket
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("waiting for a connection")

currentId = 0
pos = ["0:50,50", "1:100,100"]


def threaded_client(conn):
    global currentId, pos
    conn.send(str(currentId).encode())
    print(f'assigned id {currentId}')
    currentId += 1
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                conn.send(str.encode("goodbye"))
                break
            else:
                this_state = data.decode('utf-8')
                print("received: " + this_state)
                arr = this_state.split(":")
                this_id = int(arr[0])

                is_fetching_init_pos = arr[1] == ''
                if is_fetching_init_pos:
                    reply = pos[this_id]
                else:
                    pos[this_id] = this_state
                    another_id = 1 if this_id == 0 else 0
                    reply = pos[another_id][:]

                print("sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("connection closed")
    currentId -= 1
    conn.close()


if __name__ == '__main__':
    while True:
        conn, addr = s.accept()
        print("connected to: ", addr)
        start_new_thread(threaded_client, (conn,))
