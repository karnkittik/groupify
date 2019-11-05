from tkinter import *
import setup

from services.user import UserService


class UserInformation(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.label = Label(self, text="Information: ")
        self.label.grid(row=0)

        self.l1 = Label(self, text="First Name: ")
        self.l1.grid(row=1, column=0)

        self.e1 = Entry(self)
        self.e1.grid(row=1, column=1)

        self.l2 = Label(self, text="Last Name: ")
        self.l2.grid(row=1, column=2)

        self.e2 = Entry(self)
        self.e2.grid(row=1, column=3)

        self.l4 = Label(self, text="Year: ")
        self.l4.grid(row=1, column=4)

        self.e4 = Entry(self, width=5)
        self.e4.grid(row=1, column=5)

        self.l5 = Label(self, text="Faculty: ")
        self.l5.grid(row=1, column=6)

        self.e5 = Entry(self)
        self.e5.grid(row=1, column=7)

        self.update_button = Button(self, text="Update", command=self.update)
        self.update_button.grid(row=1, column=8, padx=10)

    def update(self):
        first_name = self.e1.get()
        last_name = self.e2.get()
        year = self.e4.get()
        faculty = self.e5.get()

        setup.current_user.update(first_name, last_name, year, faculty)
        UserService.updateProfile(first_name, last_name, faculty, year)
        print(first_name, last_name, year, faculty)
        print(UserService.getProfile())
