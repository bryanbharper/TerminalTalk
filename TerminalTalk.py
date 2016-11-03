#!/usr/bin/python
import socket, select, sys

def eavesdrop():
    sys.stdout.write("Talk: ")
    sys.stdout.flush()

# Main
if __name__ == "__main__":

    if( len(sys.argv) < 2 ):
        username = "Anonymous"
    else:
        username = sys.argv[1]

    # Setup
    buffer_size = 2 ** 12
    server_port = 7777
    server_ip = socket.gethostname()
    server_address = ( server_ip, server_port )

    # Create socket
    megaphone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Establish connection with server
    try:
        megaphone.connect(server_address)

        # Wait for server to request username
        #request = megaphone.recv(buffer_size)
        #if request == "username":
        #    megaphone.send(username)

    except:
        print('Could not connect to TerminalTalk servers. Please try again later.')
        sys.exit()

    # From here on out, we only want to briefly listen to the megaphone socket
    # rather than waiting for data to be recieved. Thus, set a timeout
    megaphone.settimeout(2)

    # Create a list to keep track of connections (terminal input and megaphone)
    connections = [megaphone, sys.stdin]

    eavesdrop()
    while True:
        # Get a list of readable sockets / inputs
        readables, writables, errors = select.select(connections, [], [])

        for socket_i in readables:
            # See if a message has been sent from server
            if socket_i == megaphone:
                missive = socket_i.recv(buffer_size)
                if missive:
                    sys.stdout.write(missive)
                    eavesdrop()
                else:
                    # If misssive returns False, the connection is broken.
                    print("\n The connection has been lost... please reconnect.")
                    sys.exit()
            else:
                # See if the user has entered a message
                verbiage = sys.stdin.readline()
                megaphone.send(verbiage)
                eavesdrop()
