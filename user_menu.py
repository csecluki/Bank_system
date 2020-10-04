from tkinter import *
from user_data import UserData
import connector


class UserMenu(Frame):

    def __init__(self, window, controller):
        Frame.__init__(self, window)
        self.controller = controller

    def data(self, client_id, name, pswd, balance):

        self.greetings_label = Label(self, text=f"Hello, {name}!")
        self.greetings_label.pack()

        self.money_label = Label(self, text=f"Your current balance is: {balance}")
        self.money_label.pack()

        self.question_label = Label(self, text="How can I help you?")
        self.question_label.pack()

        self.make_a_transfer_button = Button(self, text="Make a transfer", command=self.make_transfer,
                                             activebackground="grey", activeforeground="black")
        self.make_a_transfer_button.pack()

        self.logout_button = Button(self, text="Log out", command=self.log_out,
                                    activebackground="grey", activeforeground="black")
        self.logout_button.pack()

    def open(self, client_id):
        data = connector.get_info(client_id)
        self.data(*data)
        self.pack()

    def make_transfer(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.pack_forget()
        self.controller.switch_to("transfer_menu")

    def log_out(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.pack_forget()
        self.controller.switch_to("back")
