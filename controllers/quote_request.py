import json, urllib

#(url) -> Python object
#receive URL then sed request to get JSON data
#conver JSON to return Python objects
def request_data(url):
    response = urllib.request.urlopen(url)
    return json.loads(response.read())
#To-do: fix bug "Unknown symbol"

#Receive quote symbol
#return symbol
#       name
#       price
def get_quote_info(symbol):
    if not symbol:
        return None
    else:
        url = "https://sandbox.iexapis.com/stable/stock/"+symbol+"/quote?token=Tsk_f8cd285ba22642d18133f27bd86c9671"
        data = request_data(url)
        return {
                "symbol" : data["symbol"],
                "name" : data["companyName"],
                "price" : data["latestPrice"]
                }


def get_quote_list_info(userQuoteList):
    quote_list = []
    for userQuote in userQuoteList:
        company_quote = get_quote_info(userQuote["symbol"])
        company_quote["share"] = userQuote["share"]
        company_quote["total"] = round(userQuote["share"] * company_quote["price"], 2)
        quote_list.append(company_quote)
        print(company_quote)
    return quote_list

def get_quote_list(chart):
    url = get_url_for_list(chart)
    data = request_data(url)
    quote_list = []
    for quote in data:
        reduced_quote = {}
        reduced_quote["symbol"] = quote["symbol"]
        reduced_quote["name"] = quote["companyName"]
        reduced_quote["price"] = quote["latestPrice"]

        quote_list.append(reduced_quote)
    return quote_list

def get_url_for_list(chart):
    return "https://sandbox.iexapis.com/stable/stock/market/list/"+chart+"?token=Tsk_f8cd285ba22642d18133f27bd86c9671"
