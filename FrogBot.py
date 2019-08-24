import socket

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net" 
channel = "#froggington"
botnick = "FrogBot" 
adminname = "tomdoherty" 
exitcode = "bye " + botnick 

def sendraw(msg): 
  ircsock.send(msg + "\n")

def joinchan(chan): 
  sendraw("JOIN "+ chan)
  ircmsg = ""
  while ircmsg.find("End of /NAMES list.") == -1: 
    ircmsg = ircsock.recv(2048).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    print(ircmsg)

def ping(): 
  sendraw("PONG :pingis")

def sendmsg(msg, target=channel): 
  sendraw("PRIVMSG "+ target +" :"+ msg)

def main():
  ircsock.connect((server, 6667)) 

  sendraw("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick)
  sendraw("NICK "+ botnick)

  joinchan(channel)
  
  while 1:
    ircmsg = ircsock.recv(2048).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    
    print(ircmsg)

    if ircmsg.find("KICK") != -1:
      kick_channel = ircmsg.split(' ')[2]
      sendraw("JOIN "+ kick_channel)
      sendraw("PRIVMSG "+ kick_channel+ " :Runt!")
    
    if ircmsg.find("PRIVMSG") != -1:
      name = ircmsg.split('!',1)[0][1:]
      
      message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
      if len(name) < 17:
        if message.find('Hi ' + botnick) != -1:
          sendmsg("Hello " + name + "!")

        if message.find('Fuck you ' + botnick) != -1:
          sendmsg("Fuck you too " + name + " you bitch!")
        
        if message.find('Dance ' + botnick) != -1:
          sendmsg("I am dancing " + name)

        if message[:5].find('.tell') != -1:
          target = message.split(' ', 1)[1]
          
          if target.find(' ') != -1:
              message = target.split(' ', 1)[1]
              target = target.split(' ')[0]
          
          else:
            target = name
            message = "Could not parse"
          
          sendmsg(message, target)
        
        if name.lower() == adminname.lower() and message.rstrip() == exitcode:
          sendmsg("oh...okay. :'(")
          sendraw("QUIT")
          return
    
    else:
      if ircmsg.find("PING :") != -1:
        ping()

main()
