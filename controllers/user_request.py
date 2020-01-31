#TO-DO: need to update security

#Request information of user
def request_user_quote(user_id):
    return {
            "cash" : 100000,
            "quote" : (
                ("symbol1", "name1","10","10","total1"),
                ("symbol2", "name2","20","20","total2")
                ),
            "total" : 102031,
            }

def request_user_name():
    return "aws"

def request_password(username, cursor):
    #get password
    if not cursor:
        if username == "aws":
            return "123"
        else:
            return None
    else:
        cursor.execute("SELECT password FROM user_info WHERE username = '"+username+"'")
        response = cursor.fetchone()
        if not response:
            return None
        else:
            return response[0]

def request_user_id(username, password, cursor):
    if not cursor:
        if username == "aws" and password == "123":
            return "R3T2N4"
        else:
            return None
    else:
        cursor.execute("SELECT user_id FROM user_info WHERE username = '"+username+"' AND password = '"+password+"'")
        response = cursor.fetchone()
        if not response:
            return None
        else:
            return response[0]

def request_cash(user_id, cursor):
    user_id = str(user_id)
    cursor.execute("SELECT cash FROM user_porperty WHERE user_id = '"+user_id+"'")
    row = cursor.fetchone()
    if row == None:
        return 0
    else:
        return row[0]

def request_available_share(user_id, quoteSymbol, cursor):
    cursor.execute("SELECT share FROM user_stock WHERE user_id = "+str(user_id)+" AND symbol = '"+quoteSymbol+"'")
    row = cursor.fetchone()
    if row == None:
        return 0
    else:
        return row[0]

# (String) -> Tupples of Dictionaries
# Receive user_id
# Search in database to return list of user's quotes symbol and shares
def request_list_quote(user_id, cursor):
    user_id = str(user_id)
    if not cursor:
        return []
    else:
        cursor.execute("SELECT * FROM user_stock WHERE user_id = "+user_id)
        rows = cursor.fetchall()
        list_quote = []
        for row in rows:
            quote = {
                    "symbol": row[1],
                    "share": row[2]
                    }
            list_quote.append(quote)
        return list_quote

#Check username exists
def check_username(username, cursor):
    cursor.execute("SELECT * FROM user_info WHERE username = '"+username+"'")
    row = cursor.fetchone()
    if row == None:
        return False
    else: 
        return True


def register_user(username, password, cursor):
    cursor.execute("INSERT INTO user_info (username,password) VALUES ('"+username+"', '"+password+"')")
    cursor.execute("SELECT user_id FROM user_info WHERE username = '"+username+"'")
    row = cursor.fetchone()
    user_id = row[0]
    cursor.execute("INSERT INTO user_porperty (user_id, cash) VALUES ("+str(user_id)+", 100000)")
    
