# TAKEN AND MODIFIED FROM SimpleOSC


try :
    from OSC import OSCServer, ThreadingOSCServer, ForkingOSCServer, OSCClient, OSCMessage, OSCBundle, getUrlStr
except :
    print "Warning!!! you must have pyOSC installed -> https://trac.v2.nl/wiki/pyOSC"
    
import threading


client = 0
server = 0
st = 0


def printing_handler(addr, tags, data, source):
    print "---"
    print "received new osc msg from %s" % getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags :%s" % tags
    print "the actual data is : %s" % data
    print "---"



def initOSCClient(ip='127.0.0.1', port=9000) :
    global client
    client = OSCClient()
    client.connect( (ip,port) )
    
def initOSCServer(ip='127.0.0.1', port=9000, mode=0) :
    """ mode 0 for basic server, 1 for threading server, 2 for forking server
    """
    global server, st

    if mode == 0 :
        server = OSCServer( (ip ,port) ) # basic
    elif mode == 1 : 
        server = ThreadingOSCServer( (ip ,port) ) # threading
    elif mode == 2 :
        server = ForkingOSCServer( (ip ,port) ) # forking

    server.addDefaultHandlers()

def startOSCServer() :
    print "Registered Callback-functions are :"
    for addr in server.getOSCAddressSpace():
        print addr
    st = threading.Thread( target = server.serve_forever )
    st.start()

def setOSCHandler(address="/print", hd=printing_handler) :
    server.addMsgHandler(address, hd) # adding our function

def closeOSC() :
    if client is not 0 : client.close()
    if server is not 0: server.close() 
    if st is not 0: st.join()

def reportOSCHandlers() :
    print "Registered Callback-functions are :"
    for addr in server.getOSCAddressSpace():
        print addr
    
def sendOSCMsg( address='/print', data=[] ) :
    m = OSCMessage()
    m.setAddress(address)
    for d in data :
        m.append(d)
    client.send(m)

def createOSCBundle(address) : # just for api consistency
    return OSCBundle(address)
    
def sendOSCBundle(b):
    client.send(b)

def createOSCMsg(address='/print', data=[]) :
    m = OSCMessage()
    m.setAddress(address)
    for d in data :
        m.append(d)
    return m



