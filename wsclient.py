import time, sys, socket
from ws4py.client.threadedclient import WebSocketClient

def printHard(*args):
    print(*args)
    sys.stdout.flush()

class DummyClient(WebSocketClient):
    def opened(self):
        printHard("Opened.")

        while True:
            stuffToSend = "*" * 20
            printHard(stuffToSend)
            self.send(stuffToSend)
            time.sleep(2)

    def setup(self, timeout=1):
        try:
            self.__init__(self.url)
            self.connect()
            self.run_forever()
        except KeyboardInterrupt:
            self.close()
        except:
            newTimeout = timeout + 1
            printHard("Timing out for %i seconds. . ." % newTimeout)
            time.sleep(newTimeout)
            printHard("Attempting reconnect. . .")
            self.setup(newTimeout)

    def closed(self, code, reason=None):
        printHard("Closed down", code, reason)
        printHard("Timing out for a bit. . .")
        time.sleep(3)
        printHard("Reconnecting. . .")
        # self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.setup()


    def received_message(self, m):
        printHard(m)
        # if len(m) == 175:
        #     self.close(reason='Bye bye')

if __name__ == '__main__':
    ws = DummyClient('ws://localhost:9000/ws')
    ws.setup()
