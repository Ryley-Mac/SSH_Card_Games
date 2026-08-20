import os
import socket
import threading
import paramiko
from ssh_blackjack import BlackJack

HOST_KEY = paramiko.RSAKey(filename="/home/froo/.ssh/server_host_key")

class LobbyServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def get_allowed_auths(self, username):
        #print(f"get_allowed_auths username={username}")
        return "password,publickey"

    def check_auth_password(self, username, password):
        #print("check_auth_password")
        return paramiko.AUTH_SUCCESSFUL
    
    def check_channel_request(self, kind, chanid):
        #print("check_channel_request")
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        #print("check_channel_pty_request")
        return True
    
    def check_auth_publickey(self, username, key):
        #print("Check_auth_publickey")
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        #print("get_allowed_auths")
        self.event.set()
        return True


class User:
    def __init__(self, client_sock, addr, name, password):
        self.sock = client_sock
        self.addr = addr
        self.name = name
        self.password = password

def handle_connection(client_sock, addr):
    transport = paramiko.Transport(client_sock)
    transport.add_server_key(HOST_KEY)

    server = LobbyServer()

    transport.start_server(server=server)
    
    channel = transport.accept(20)
    if channel is None:
        print("No channel opened.")
        return

    server.event.wait(10)

    channel.send("Welcome to the Card Games lobby!\r\n")

    buffer = b""

    try:
        loop = True
        while loop:
            data = channel.recv(1024)
            if not data:
                print("no data")
                loop = False

            elif b"\x03" in data: # Close on Ctrl + C
                print("ctrl+c")
                channel.send(f"\r\nGoodbye!\r\n")
                channel.send(data)
                loop = False

            elif b"\r" in data or b"\n" in data: # When user press enter/return
                line = buffer.strip().decode(errors="ignore")
                if line.lower() in ("exit", "quit", "stop"): # Initiate exit
                    print(f"exited: {line}")
                    channel.send(f"\r\nGoodbye!\r\n")
                    loop = False
                else: # While client inputs characters
                    print(f"{addr} Buffer: {buffer}")
                    buffer = b""
                    channel.send(b"\r\n")
            else:
                for byte in data:
                    ch = bytes([byte])

                    if buffer and ch in (b"\x7f", b"\x08", b"\x1b[3~"):
                        buffer = buffer[:-1]
                        channel.send(b"\b \b")
                    else:
                        buffer += data
                        channel.send(data)
               

    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        channel.close()
        transport.close()
        print(f"Connection with {addr} closed.")


def console_loop():
    loop = True
    while loop:
        try:
            cmd = input()
            if cmd.lower() in ("quit", "exit", "stop"):
                loop = False
                os._exit(0)
        except EOFError:
            loop = False
        

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 2222))
    sock.listen(100)
    print("Listening on port 2222...")

    threading.Thread(target=console_loop, daemon=True).start()
    loop = True
    while loop:
        client_sock, addr, name, password = sock.accept()
        threading.Thread(target=handle_connection, args=(client_sock, addr), daemon=True).start()

if __name__ == "__main__":
    main()
