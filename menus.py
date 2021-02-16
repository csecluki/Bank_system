from tkinter import *
import connector
from user_data import UserData


class MainMenu(Frame):

    def __init__(self, window, controller):
        Frame.__init__(self, window)
        self.controller = controller

        self.welcome_label = Label(self, text="Welcome to bank!")
        self.welcome_label.pack()

        self.log_in_button = Button(self, text="Log in", command=self.sign_in,
                                    activebackground="grey", activeforeground="black")
        self.log_in_button.pack()

        self.deposit_button = Button(self, text="Deposit money", command=self.deposit_menu,
                                     activebackground="grey", activeforeground="black")
        self.deposit_button.pack()

        self.new_account_button = Button(self, text="Create new account", command=self.new_account,
                                         activebackground="grey", activeforeground="black")
        self.new_account_button.pack()

        self.quit_button = Button(self, text="Quit", command=self.exit,
                                  activebackground="grey", activeforeground="black")
        self.quit_button.pack()

    def open(self):
        self.pack()

    def sign_in(self):
        self.pack_forget()
        self.controller.switch_to("sign_in")

    def deposit_menu(self):
        self.pack_forget()
        self.controller.switch_to("deposit_menu")

    def new_account(self):
        self.pack_forget()
        self.controller.switch_to("new_account")

    def exit(self):
        self.pack_forget()
        self.controller.switch_to("exit")


class SignIn(Frame):

    def __init__(self, window, controller):
        Frame.__init__(self, window)
        self.controller = controller

        self.id_label = Label(self, text="Your id:")
        self.id_label.pack()

        self.id_field = Entry(self)
        self.id_field.pack()

        self.pswd_label = Label(self, text="Your pasword:")
        self.pswd_label.pack()

        self.password_field = Entry(self, show="*")
        self.password_field.pack()

        self.submit_button = Button(self, text="Log in", command=self.log_in,
                                    activebackground="grey", activeforeground="black")
        self.submit_button.pack()

        self.back_button = Button(self, text="Back", command=self.back,
                                  activebackground="grey", activeforeground="black")
        self.back_button.pack()

        self.error_label = Label(self, text="Invalid id number or password")

    def open(self):
        self.pack()

    def back(self):
        self.clear_entries()
        self.error_label.pack_forget()
        self.pack_forget()
        self.controller.switch_to("back")

    def clear_entries(self):
        self.id_field.delete(0, "end")
        self.password_field.delete(0, "end")

    def log_in(self):
        try:
            number = int(self.id_field.get())
            pswd = self.password_field.get()
            if connector.log_in(number, pswd):
                self.clear_entries()
                self.error_label.pack_forget()
                self.pack_forget()
                self.controller.switch_to("user_menu", number)
        except (ValueError, TypeError):
            self.show_label()

    def show_label(self):
        self.error_label.pack()


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


class TransferMenu(Frame):

    def __init__(self, window, controller):
        Frame.__init__(self, window)
        self.controller = controller

        self.id_label = Label(self, text="Receiver id:")
        self.id_label.pack()

        self.id_field = Entry(self)
        self.id_field.pack()

        self.money_label = Label(self, text="Transfer amount:")
        self.money_label.pack()

        self.money_field = Entry(self)
        self.money_field.pack()

        self.message_label = Label(self, text="Message to receiver:")
        self.message_label.pack()

        self.message_field = Text(self, height=4, width=30, xscrollcommand=True)
        self.message_field.pack()

        self.confirm_button = Button(self, text="Transfer", command=self.transfer,
                                     activebackground="grey", activeforeground="black")
        self.confirm_button.pack()

        self.back_button = Button(self, text="Back", command=self.back,
                                  activebackground="grey", activeforeground="black")
        self.back_button.pack()

    def open(self):
        self.pack()

    def transfer(self):
        if self.controller.active_user != int(self.id_field.get()):
            connector.transfer(self.controller.active_user, int(self.id_field.get()),
                               int(self.money_field.get()), self.message_field.get("1.0", "end"))
        self.pack_forget()
        self.controller.switch_to("back")

    def back(self):
        self.pack_forget()
        self.controller.switch_to("back")


class DepositMenu(Frame):

    def __init__(self, window, controller):
        Frame.__init__(self, window)
        self.controller = controller

        self.id_label = Label(self, text="Your id:")
        self.id_label.pack()

        self.id_field = Entry(self)
        self.id_field.pack()

        self.money_label = Label(self, text="Deposit amount:")
        self.money_label.pack()

        self.money_field = Entry(self)
        self.money_field.pack()

        self.accept_button = Button(self, text="Transfer", command=self.deposit,
                                    activebackground="grey", activeforeground="black")
        self.accept_button.pack()

        self.back_button = Button(self, text="Back", command=self.back,
                                  activebackground="grey", activeforeground="black")
        self.back_button.pack()

        self.error_label = Label(self, text="Invalid id number or amount")
        self.wrong_data_label = Label(self, text="Given id doesn't exist")

    def open(self):
        self.pack()

    def deposit(self):
        try:
            if connector.exist([int(self.id_field.get())]):
                connector.deposit(int(self.id_field.get()), int(self.money_field.get()))
                self.back()
            else:
                self.show_label("id")
        except (ValueError, TypeError):
            self.show_label("error")

    def show_label(self, kind):
        if kind == "error":
            self.wrong_data_label.pack_forget()
            self.error_label.pack()
        elif kind == "id":
            self.error_label.pack_forget()
            self.wrong_data_label.pack()

    def back(self):
        self.pack_forget()
        self.controller.switch_to("back")


class NewAccount(Frame):

    def __init__(self, window, controller):
        Frame.__init__(self, window)
        self.controller = controller

        self.error_label = Label(self, text="Passwords don't match!")

        self.creation_label = Label(self, text="Hello!")
        self.creation_label.pack()

        self.name_label = Label(self, text="Your name:")
        self.name_label.pack()

        self.name_field = Entry(self)
        self.name_field.pack()

        self.pswd_label = Label(self, text="Your pasword:")
        self.pswd_label.pack()

        self.password_field = Entry(self, show="*")
        self.password_field.pack()

        self.confirm_pswd_label = Label(self, text="Confirm your pasword:")
        self.confirm_pswd_label.pack()

        self.confirm_password_field = Entry(self, show="*")
        self.confirm_password_field.pack()

        self.submit_button = Button(self, text="Create account", command=self.submit,
                                    activebackground="grey", activeforeground="black")
        self.submit_button.pack()

        self.back_button = Button(self, text="Back", command=self.back,
                                  activebackground="grey", activeforeground="black")
        self.back_button.pack()

    def open(self):
        self.pack()

    def submit(self):
        pswd = self.password_field.get()
        if len(pswd) > 0 and pswd == self.confirm_password_field.get():
            user_id = connector.new_client(self.name_field.get(), pswd)
            self.controller.switch_to("account_created", user_id)
            for element in [self.name_field, self.password_field, self.confirm_password_field]:
                element.delete(0, "end")
                element.focus()
            self.pack_forget()
        else:
            self.error_label.pack()

    def back(self):
        for element in [self.name_field, self.password_field, self.confirm_password_field]:
            element.delete(0, "end")
            element.focus()
        self.pack_forget()
        self.controller.switch_to("back")


class AccountCreated(Frame):

    def __init__(self, window, controller):
        Frame.__init__(self, window)
        self.controller = controller

    def data(self, client_id):

        self.confirm_label = Label(self, text=f"Your account was succesfully created!")
        self.confirm_label.pack()

        self.info_label = Label(self, text=f"Your id is: {client_id}.")
        self.info_label.pack()

        self.main_menu_button = Button(self, text="Go to main menu", command=self.main_menu,
                                       activebackground="grey", activeforeground="black")
        self.main_menu_button.pack()

    def open(self, client_id):
        self.data(client_id)
        self.pack()

    def main_menu(self):
        for element in [self.confirm_label, self.info_label, self.main_menu_button]:
            element.destroy()
        self.pack_forget()
        self.controller.switch_to("main_menu")
