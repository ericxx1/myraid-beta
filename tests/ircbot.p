//Myraid Irc Bot//
var channel = "#PyPy"
New Socket("irc"):
    irc.connect("irc.freenode.net", 6667)
    irc.send("NICK Myraidbot\r\n")
    irc.send("USER Myraid Myraid Myraid : Myraid\r\n")
    while(0 < 1):
        data = irc.recv(4096)
        if(" 396 " in data):
            irc.send("JOIN " + channel + "\r\n")
        end   
          
        else if("PING" in data):
            irc.send("PONG ")
        end
    end
end
