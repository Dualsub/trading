import json
import requests

if __name__ == "__main__":
    symbols = open("../yahoo_stocks.txt", mode="r", encoding="utf8").read().splitlines()
    for sym in symbols:
        with open(f"{sym}.json", "w") as fp:
            data = requests.get(f"https://sandbox.iexapis.com/stable/stock/{sym}/chart/5y?token=Tsk_e96ea420419b450882b6f19a545e7c0a").json()
            json.dump(data, fp)