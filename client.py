from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import tkinter.simpledialog


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Real Time Messaging Application!!!")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, width=50, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


# Sockets part
class MyDialog(tkinter.simpledialog.Dialog):

    def body(self, master):
        tkinter.Label(master, text="Enter HOST Address:").grid(row=0)
        tkinter.Label(master, text="Enter PORT Address:").grid(row=1)

        self.e1 = tkinter.Entry(master)
        self.e2 = tkinter.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e1 # initial focus

        self.apply()

    def apply(self):
        self.HOST = self.e1.get()
        self.PORT = self.e2.get()
        return [self.HOST, self.PORT]

HP_val = MyDialog(top)
# print(f"***************{HP_val.HOST}***************")
# print(f"***************{HP_val.PORT}***************")

if not HP_val.PORT:
    HP_val.PORT = 1234
else:
    HP_val.PORT = int(HP_val.PORT)

BUFSIZ = 1024
ADDR = (HP_val.HOST, HP_val.PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
receive_thread = Thread(target=receive)
receive_thread.start()
top.mainloop()  # Starts GUI execution.