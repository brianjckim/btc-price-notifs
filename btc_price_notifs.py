import requests
from datetime import datetime
import time

BTC_API_URL = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
IFTTT_WEBHOOKS_URL = (
    "https://maker.ifttt.com/trigger/{}/with/key/bBodYdtkX91z69Nfxywj_4"
)
BTC_PRICE_FLOOR = 6000
BTC_PRICE_CEILING = 7000


def get_btc_price():
    response = requests.get(BTC_API_URL)
    response_json = response.json()
    return round(float(response_json[0]["price_usd"]), 2)


def post_ifttt_webhook(event, value):
    data = {"value1": value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)


def format_btc_history(btc_history):
    rows = []

    for btc_price in btc_history:
        date = btc_price["date"].strftime("%m.%d.%Y %H:%M")
        price = btc_price["price"]
        row = "{}: ${}".format(date, price)
        rows.append(row)

    return "\n".join(rows)


def main():
    btc_history = []

    while True:
        price = get_btc_price()
        date = datetime.now()
        btc_history.append({"date": date, "price": price})

        if price < BTC_PRICE_FLOOR or price > BTC_PRICE_CEILING:
            post_ifttt_webhook("btc_price_alert", price)

        if len(btc_history) == 3:
            post_ifttt_webhook("btc_price_update", format_btc_history(btc_history))
            btc_history = []

        time.sleep(19 * 60)


if __name__ == "__main__":
    main()
