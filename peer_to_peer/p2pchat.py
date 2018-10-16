from networks import *
import time


def chat(n, ip):
    print("Start chatting!")
    ui = input("\n")
    while not ui == "q":
        n.broadcast(("{ " + ip + " } " + ui).encode())
        ui = input()

    n.disconnect()


your_ip = get_ip()

n = Node()

n.listen()

print("Your address: %s:%d" % (your_ip, n.port))

while not n.integrated.is_set():
    addr = input("Peer ip:port: ")
    if ":" not in addr or addr == "c" or not addr:
        break
    addr = addr.replace(" ", "").split(":")
    n.connect_to_peer((addr[0], int(addr[1])))
    time.sleep(0.5)

input_thread = threading.Thread(target=chat, name="Chat", args=(n, your_ip))
input_thread.start()
