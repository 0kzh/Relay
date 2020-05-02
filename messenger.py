from fbchat import Client
from fbchat.models import *
from datetime import datetime
import getpass

print("Please enter your password:")

class RelayBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        #self.markAsRead(thread_id)
        # TODO: store in dict for faster lookup
        user = client.fetchUserInfo(author_id)[author_id]
        time = datetime.fromtimestamp(message_object.timestamp / 1000) # convert time in millis to datetime obj
        print("[{}] {}: {}".format(str(time), user.name, message_object.text)) 

client = RelayBot('kelvin.zhang@uwaterloo.ca', getpass.getpass())
client.listen()
print("Logged with id: {}".format(client.uid))

cmds = {
        "getfriends": "",
        "msg {name} {msg}": "send message to friend",
        "getactivechats": "print a list of active chats"
    }
print("Please enter a command. Type help for list of commands")
prompt = "Enter a command: "
cmd = str(raw_input(prompt)) 

ids = dict()

while cmd: 
    if cmd == "help":
        print("----- HELP ------")
        for key, val in cmds.items():
            print("{}: {}".format(key, val))
        print("-----------------")
    elif cmd == "getactivechats":
        users = client.fetchAllUsers()
        for user in users:
            print("{}: {}".format(user.name, user.uid))
    elif cmd.startswith("msg"):
        args = cmd.split(" ")
        if len(args) < 3:
            print("Invalid arguments")
            continue
        name = args[1]
        message = ''.join(args[2:])
        user = client.searchForUsers(name)[0]
        userId = user.uid
        targetType = ThreadType.USER
        
        client.send(Message(text=message), thread_id=userId, thread_type=targetType)
    cmd = str(raw_input(prompt))

client.logout()