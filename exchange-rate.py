import sys
import csv
import json
import time
import requests

# Fetch available currencies
print("Looking for available currencies...")
querystring = {"format": "json"}
headers = {
    'x-rapidapi-host': "currency-converter5.p.rapidapi.com",
    'x-rapidapi-key': "81c29f4051msh1004bb8307e4948p17f135jsn8ffa2e7c4bb0"
}
currencyData = requests.request(
    "GET",
    "https://currency-converter5.p.rapidapi.com/currency/list",
    headers=headers,
    params=querystring
)
currencyData = json.loads(currencyData.text)
currencyData = currencyData.get("currencies")
userCurrency = sys.argv[1].upper()
print("Initiate process for " + userCurrency)
timestamp = str(round(time.time()))
filename = "exchange-rate-" + timestamp + ".csv"
print("Fetching exchange rate for " + userCurrency + " and preparing csv...")
with open(filename, 'w', newline='') as file:
    filePointer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filePointer.writerow([
        'Base Currency Code',
        'Base Currency',
        'Target Currency',
        'Rate',
        'Updated at'
    ])

    for code in currencyData:
        querystring = {"format": "json", "from": code, "to": userCurrency, "amount": "1"}
        exchangeData = requests.request(
            "GET",
            "https://currency-converter5.p.rapidapi.com/currency/convert",
            headers=headers,
            params=querystring
        )
        exchangeData = json.loads(exchangeData.text)
        if exchangeData.get("status") == "success":
            filePointer.writerow([
                exchangeData.get("base_currency_code"),
                exchangeData.get("base_currency_name"),
                exchangeData.get("rates").get(userCurrency).get("currency_name"),
                exchangeData.get("rates").get(userCurrency).get("rate"),
                exchangeData.get("updated_date"),
            ])
print("Exchange rate csv - " + filename + " ready to use.")