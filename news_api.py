import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

TWILIO_SID = 'your twilio sid'
TWILIO_AUTH_TOKEN = 'Twilio auth_token'

VIRTUAL_TWILIO_NUMBER = 'your twilio sid'
VERIFIED_NUMBER = 'your twilio number '

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_API_KEY = 'YOUR API_KEY'

parameters = {
    'apikey': 'DOKHYYJ25ZLIJ3G2',
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK_NAME,

}

r = requests.get(STOCK_ENDPOINT, params=parameters)
stock = r.json()
data = stock['Time Series (Daily)']

data_list = [value for (key, value) in data.items()]
yesterday_stock = data_list[2]['4. close']
print(yesterday_stock)

day_before_yesterday_close_price = data_list[3]['4. close']
print(day_before_yesterday_close_price)

difference = float(yesterday_stock) - float(day_before_yesterday_close_price)

print(abs(difference))
diff_percent = (difference / float(yesterday_stock)) * 100  
print(f'{abs(diff_percent)} %')
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if diff_percent > 1:

    new_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(STOCK_ENDPOINT, params=new_params)

    json_news_response = news_response.json()['articles']

    three_articles = json_news_response[:3]

    new_list_of_response = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in three_articles]

    # Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in new_list_of_response:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
