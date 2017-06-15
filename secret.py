import socket, threading, time,  atexit,  random


sock = None;

class Client(threading.Thread):
    def __init__(self, c, name):
        threading.Thread.__init__(self)
        self.this = c;
        self.name = name;
        self.pendingMessages = []
        self.stop = False;
        self.winner = False;
        self.score = 0;

    def run(self):
        while not self.stop:
            message = self.this.recv(1024).decode()
            if(not message == "" and not message == None):
                print(message)
                self.pendingMessages.append(message)

    def send(self, message):
        self.this.sendall(message)

    def receive(self):
        if(len(self.pendingMessages) == 0):
            return None
        out = self.pendingMessages;
        self.pendingMessages = []
        return out

        
class Host(threading.Thread):
    def __init__(self, players):
        threading.Thread.__init__(self);
        self.clients = [];
        self.stop = False;
        self.players = players;

    def run(self):
        global sock
        #init
        host = socket.gethostname()
        port = 1111
        sock = socket.socket()
        sock.bind((host, port))
        print("[SERVER] Server hosted on " + host + ":" + str(port))
        sock.listen(1)
        #Joining
        while len(self.clients) < self.players and not self.stop:
            print("[SERVER] Awaiting Connection")
            data = sock.accept()
            addr = str(data[1])
            c = data[0]
            print("[SERVER] Connection from: "+addr)
            name = c.recv(1024).decode()
            c = Client(c,name)
            c.start()
            c.setName(c.name)
            self.clients.append(c)
            for c in self.clients:
                c.send(("Server: "+name+" Connected").encode())
        #Main loop
        while not self.stop:
            #Setup
            print("[SERVER] Generating code")
            length = random.randint(8,10)
            code = [];
            guessed = False
            characters = list("1234567890ABCDEF")
            for i in range(length):
                code.append(random.choice(characters))
            print("[SERVER] " + str(code))
            for c in self.clients:
                c.send("Server: You have to be the first to decrypt the hexidescimal code.\n\tThe code is "+str(length)+" characters long.")
                time.sleep(1)
                c.send("START")
            while not guessed and not self.stop:
                results = []
                for c in self.clients:
                    msgs = c.receive()
                    if(not msgs == None):
                        for msg in msgs:
                            m = list(msg.upper())
                            iteration = 0
                            correct = True;
                            for i in m:
                                if((not i in characters) or iteration>=len(code)):
                                    print("[DEBUG] Not in characters")
                                    results.append("X")
                                    correct = False
                                    continue
                                print(str(m)+"\t"+i)
                                char = code[iteration]
                                value = int(char, 16)
                                print("[DEBUG] "+ str(iteration)+ "\t" +i+"\t"+ str(value))
                                if(char == i):
                                    results.append("Y")
                                elif(value > int(i,16)):
                                    results.append("U")
                                    correct = False
                                elif(value < int(i,16)):
                                    results.append("D")
                                    correct = False
                                iteration += 1
                            if(iteration < len(code)):
                                correct = False
                            print("[SERVER] "+"".join(results))
                            c.send("             "+''.join(results))
                            if(correct):
                                c.winner = True
                                guessed = True
            for c in self.clients:
                c.send("STOP")
                time.sleep(0.25)
                if(c.winner):
                    for c2 in self.clients:
                        c2.send(c.name+" gussed the code. The code was "+''.join(code))
                        
                        
if(raw_input("Host a server (Y/N): ").upper() == "Y"):
    print("[SERVER] You are hosting on " + socket.gethostname())
    players = input("[SERVER] Players: ")
    hostThread = Host(players);
    hostThread.start();
    hostThread.setName("Host")
    time.sleep(1);
    while True:
        pass


else:
    class Send(threading.Thread):
        def __init__(self, socket):
            threading.Thread.__init__(self);
            self.s = socket
            self.stop = False
        def run(self):
            while not self.stop:
                s.send(raw_input("Enter Guess: ").encode())
                time.sleep(2)
            

    
    s = socket.socket()
    host = socket.gethostname()#raw_input("Enter host: ")
    port = 1111
    name = raw_input("Enter name: ").replace('"',"").replace("'","").replace("\\","").replace(" ","_")
    print(name)

    print("Connecting to " + host + ":" + str(port))
    s.connect((host, port))
    print("Connected")
    s.sendall(name.encode());
    while not False:
        msg = s.recv(1024).decode()
        if(msg == "START"):
            print("[DEBUG] Starting")
            send = Send(s)
            send.start()
        elif(msg == "STOP"):
            send.stop = True
        else:
            print msg
    s.close()

def kill():
    sock.close()
    for i in hostThread.clients:
        i.stop = True
    hostThread.stop = True

atexit.register(kill)

kill()
