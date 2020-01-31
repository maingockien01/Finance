buy = 1;
sell = -1;
def commitBuy(user_id, symbol, share, price, cash, cursor):
    changeStock(user_id,symbol,share,buy,cursor)
    changeCash(user_id = user_id,cash=cash,change_total = (share * price),actionValue = buy, cursor=cursor)

def changeStock(user_id, symbol, share, actionValue, cursor):
    user_id = str(user_id)
    cursor.execute("SELECT share FROM user_stock WHERE user_id = "+user_id+" AND symbol = '"+symbol+"'")
    row = cursor.fetchone()
    if row == None:
        cursor.execute("INSERT INTO user_stock (user_id, symbol, share) VALUES ("+user_id+", '"+symbol+"', "+str(share)+")")
    else:
        newShare = int(row[0]) + int(share) * actionValue
        cursor.execute("UPDATE user_stock SET share = " + str(newShare) + " WHERE user_id = " + user_id + " AND symbol = '" + symbol + "'")

def changeCash(user_id, cash, change_total, actionValue, cursor):
    cash = float(cash)
    change_total = float(change_total)
    user_id = str(user_id)
    cash = round(cash,2)
    change_total = round(change_total, 2)
    actionValue = actionValue * (-1)
    newCash = cash + change_total * actionValue;

    cursor.execute("UPDATE user_porperty SET cash = " +str(newCash)+" WHERE user_id = " + user_id)

def commitSell(user_id, symbol, share, price, cash, cursor):
    changeStock(user_id,symbol,share,sell,cursor)
    changeCash(user_id = user_id,cash=cash,change_total = (share * price),actionValue = sell, cursor=cursor)
