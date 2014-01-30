import time, socket
from ws4py.client.threadedclient import WebSocketClient

class DummyClient(WebSocketClient):
    def opened(self):
        print "Opened."
        def data_provider():
            for i in range(1, 200, 25):
                yield "#" * i

        self.send(data_provider())

        for i in range(0, 200, 25):
            print i
            self.send("*" * i)

    def setup(self, timeout=1):
        try:
            self.__init__(self.url)
            self.connect()
            self.run_forever()
        except KeyboardInterrupt:
            self.close()
        except:
            newTimeout = timeout + 1
            print "Timing out for %i seconds. . ." % newTimeout
            time.sleep(newTimeout)
            print "Attempting reconnect. . ."
            self.setup(newTimeout)

    def closed(self, code, reason=None):
        print "Closed down", code, reason
        print "Timing out for a bit. . ."
        time.sleep(3)
        print "Reconnecting. . ."
        # self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.setup()


    def received_message(self, m):
        print m
        # if len(m) == 175:
        #     self.close(reason='Bye bye')

if __name__ == '__main__':
    ws = DummyClient('ws://localhost:9000/ws')
    ws.setup()
