import connector


class UserData:

    def __init__(self):
        self.id = None
        self.name = None
        self.balance = None
        self.pswd = None

    def upload_user_data(self, client_id):
        self.id, self.name, self.balance, self.pswd = connector.get_info(client_id)

    def clear_data(self):
        self.name = None
        self.balance = None
        self.pswd = None
