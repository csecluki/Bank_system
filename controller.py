from window import Window
from user_data import UserData
from menus import *


class Controller:

    def __init__(self):
        self.window = Window()

        self.user_data = UserData()
        self.active_user = None

        self.main_menu = MainMenu(self.window, self)
        self.sign_in = SignIn(self.window, self)
        self.deposit_menu = DepositMenu(self.window, self)
        self.new_account = NewAccount(self.window, self)
        self.user_menu = UserMenu(self.window, self)
        self.transfer_menu = TransferMenu(self.window, self)

        self.stack = []
        self.switch_to("main_menu")

        self.window.mainloop()

    def switch_to(self, action, *args):
        if action == "back":
            self.stack.pop()
        else:
            self.stack.append(action)

        if self.stack[-1] == "main_menu":
            self.main_menu.open()
        elif self.stack[-1] == "sign_in":
            self.active_user = None
            self.sign_in.open()
        elif self.stack[-1] == "deposit_menu":
            self.deposit_menu.open()
        elif self.stack[-1] == "new_account":
            self.new_account.open()
        elif self.stack[-1] == "user_menu":
            if len(args) > 0:
                self.active_user = args[0]
            self.user_menu.open(self.active_user)
        elif self.stack[-1] == "transfer_menu":
            self.transfer_menu.open()
        else:
            self.window.destroy()
            quit()
