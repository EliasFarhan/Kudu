import socket
from threading import Lock, Thread
from engine.vector import Vector2


class SharedData():
    def __init__(self,data):
        self.data = data
        self.lock = Lock()

    def access_data(self):
        """Always free the shared data after being used"""
        if not self.lock.locked():
            self.lock.acquire()
            return self.data
        else:
            return None
    def free_data(self):
        self.lock.release()

players_list = SharedData({})


class PlayersListUpdate(Thread):
    def run(self):
        self.finish = False
        while not self.finish:
            sock = shared_socket.access_data()
            if sock:
                players_data = sock.recv(1024)
                shared_socket.free_data()
                sock = None
                parsed_data = players_data.split(";")
                if parsed_data[0] != "NEW_ID":
                    """Position"""
                    parsed_data[1] = parsed_data[1].split(',')
                    parsed_data[1] = Vector2(int(float(parsed_data[1][0])),int(float(parsed_data[1][1])))
                    """Frame"""
                    parsed_data[3] = int(parsed_data[3])

                    """update players position"""
                    players = players_list.access_data()
                    players[parsed_data[0]] = parsed_data[1:]
                    players_list.free_data()

    def finish(self):
        self.finish = True

HOST, PORT = "92.222.15.13", 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
shared_socket = SharedData(client_socket)
update_thread = None
self_id = 0


def get_self_id():
    global self_id
    return self_id


def init():
    global update_thread,self_id
    data = "ID_REQUEST;"
    new_id_request = None
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect(("92.222.15.13", 10000))
        sock.sendall(data)
        # Receive data from the server and shut down
        new_id_request = sock.recv(1024)
    finally:
        sock.close()
    self_id = new_id_request.split(";")[1]
    '''
    run thread getting new players position
    '''
    update_thread = PlayersListUpdate()
    update_thread.daemon = True
    update_thread.start()


def set_request(pos, state, frame):
    """Change the position of the player on the server"""

    """Set correct pos, state, frame"""
    sock = shared_socket.access_data()
    if sock:
        sock.sendto("SET_REQUEST;"+str(self_id)+";"+pos.get_string() +";"+state+";"+str(frame)+";", (HOST, PORT))
        shared_socket.free_data()
        sock = None


def exit_network():
    global update_thread
    update_thread.finish()


def get_players_request():
    sock = shared_socket.access_data()
    if sock:
        sock.sendto("GET_REQUEST;", (HOST, PORT))
        shared_socket.free_data()
        sock = None


