import os
import sys
import requests
from dotenv import load_dotenv
holdings = {
}
cost_prices = {
}
load_dotenv()
api_key = os.environ.get("COINCAP_API_KEY")
payload={'apiKey':api_key}
if api_key is None:
    sys.exit("set up the COINCAP_API_KEY environment variable first")

def retrieve():
    try:
        symbols = ",".join(holdings)
        url = (f'https://rest.coincap.io/v3/price/bysymbol/{symbols}')
        api = requests.get(url, params = payload)
        api.raise_for_status()
        data = api.json()
        return data
    except requests.exceptions.RequestException:
        sys.exit("unable to retrieve api")

def user_input():
    while True:
        try:
            symbol = input("shortname of coin: ").upper()
            coin_amt = float(input("amount of coin: "))
            cost_price = float(input("price paid per coin: "))
            holdings[symbol] = (coin_amt)
            cost_prices[symbol] = (cost_price)
        except TypeError:
            sys.exit("please input your number correctly")
        exit_loop = input("any more coins to add? Y/N")
        if exit_loop.upper() == "N":
             break

def calculate_cost():
    total = 0
    for coin in cost_prices:
        cost = cost_prices[coin] * holdings[coin]
        total += cost
    return total

def calculate_value(prices):
    total = 0
    i = 0
    for coin in holdings:
        value = holdings[coin] * float(prices["data"][i])
        i += 1
        total += value
    return total

def main():
    user_input()
    prices = retrieve()
    total_cost = calculate_cost()
    total_value = calculate_value(prices)
    print(f"total cost is {total_cost}")
    print(f"total value is {total_value}")

if __name__ == "__main__":
    main()