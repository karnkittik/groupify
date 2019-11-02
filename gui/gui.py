from tkinter import *

window = Tk()
window.title("Groupify")
window.geometry("820x600")

info = Frame(window)
info.pack()
chat = Frame(window)
chat.pack(side="right")
g_chat = Frame(chat)
g_chat.pack()
p_chat = Frame(chat)
p_chat.pack()

#Function
#Submit Button
def update():
    first_name = e1.get()
    last_name = e2.get()
    nickname = e3.get()
    year = e4.get()
    faculty = e5.get()

    # user_info = first_name+"    "+last_name+"    "+nickname+"    "+year+"    "+faculty
    Label(info,text = "Updated").grid(row=0, column=1)

#Send message
def sent(chat,msg_box,var):
    chat.config(state="normal")
    msg = msg_box.get()
    chat.insert(INSERT, msg+"\n")
    chat.config(state="disabled")
    var.set("")

#Text Header
Label(info, text="Information:").grid(row=0, column=0)

#Form
#FirstName
Label(info, text="First Name").grid(row=1,column=0)
e1 = Entry(info)
e1.grid(row=1,column=1)

#LastName
Label(info, text="Last Name").grid(row=1,column=2)
e2 = Entry(info)
e2.grid(row=1,column=3)

#Nickname
Label(info, text="Nickname").grid(row=1,column=4)
e3 = Entry(info, width=10)
e3.grid(row=1,column=5)

#Year
Label(info, text="Year").grid(row=1,column=6)
e4 = Entry(info, width=7)
e4.grid(row=1,column=7)

#Faculty
Label(info, text="Faculty").grid(row=1,column=8)
e5 = Entry(info)
e5.grid(row=1,column=9)

#Update Button
Button(info, text="Update", command=update).grid(row=1,column=10,padx=10)


#Global Chat
Label(g_chat, text="Global Chat").grid(row=0)
text1 = Text(g_chat, state="disabled", width=25, height=10)
text1.grid(row=1, column=0,  pady=10)

Scrollbar(g_chat).grid(row=1, column=1, ipady=60)

var1 = StringVar()
e6 = Entry(g_chat, textvariable=var1, width=30)
e6.grid(row=2, column=0, pady=5)

Button(g_chat, text="send", command= lambda: sent(text1,e6,var1)).grid(row=2, column=2, padx=10)

#Personal Chat
Label(p_chat, text="Personal Chat").grid(row=0)
text2 = Text(p_chat, state="disabled", width=25, height=10)
text2.grid(row=1, column=0,  pady=10)

var2 = StringVar()
e7 = Entry(p_chat, textvariable=var2, width=30)
e7.grid(row=2, column=0)

Button(p_chat, text="send", command= lambda: sent(text2,e7,var2)).grid(row=2, column=1, padx=10)

window.mainloop()