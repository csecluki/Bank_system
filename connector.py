import mysql.connector

bank_data_base = mysql.connector.connect(
    host="localhost",
    user="root",
    database="bank"
)

cursor = bank_data_base.cursor()


def new_client(name, pswd, money=0):
    sql_query = "INSERT INTO account (name, pswd, money)" \
                f"VALUES ('{name}', '{pswd}', {money})"
    cursor.execute(sql_query)
    bank_data_base.commit()
    sql_query = "SELECT MAX(client_id) FROM account"
    cursor.execute(sql_query)
    result = cursor.fetchone()[0]
    return result


def log_in(client_id, pswd):
    sql_query = f"SELECT pswd FROM account WHERE client_id={client_id}"
    cursor.execute(sql_query)
    result = cursor.fetchone()[0]
    try:
        if pswd == result:
            return True
    except (ValueError, TypeError):
        return False


def get_info(client_id):
    sql_query = f"SELECT * FROM account WHERE client_id={client_id}"
    cursor.execute(sql_query)
    result = cursor.fetchone()
    return result


def exist(numbers):
    for number in numbers:
        sql_query = f"SELECT (EXISTS (SELECT * FROM account WHERE client_id = {number}))"
        cursor.execute(sql_query)
        result = cursor.fetchone()[0]
        if result == 1:
            continue
        else:
            return False
    return True


def deposit(client_id, amount):
    sql_query = f"UPDATE account SET money = money + {amount} WHERE client_id = {client_id}"
    cursor.execute(sql_query)
    bank_data_base.commit()


def transfer(sender, receiver, amount, msg):
    if get_info(sender)[3] > amount:
        sql_query = f"SELECT EXISTS(SELECT * FROM account WHERE client_id = {receiver})"
        cursor.execute(sql_query)
        result = cursor.fetchone()[0]
        if result == 1:
            for query in [f"UPDATE account SET money = money - {amount} WHERE client_id = {sender}",
                          f"UPDATE account SET money = money + {amount} WHERE client_id = {receiver}",
                          f"INSERT INTO transaction (sender_id, receiver_id, amount, message)"
                          f"VALUES ({sender}, {receiver}, {amount}, '{msg}')"]:
                cursor.execute(query)
            bank_data_base.commit()
            return True
    return False
