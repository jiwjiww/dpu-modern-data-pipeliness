import requests


API_KEY = "7b404f9d1cb348024471868595e0d5ee"
payload = {
    "q": "bangkok",
    "appid": API_KEY,
    "units": "metric"
}
url = "https://api.openweathermap.org/data/2.5/weather"
response = requests.get(url, params=payload)
print(response.url)

data = response.json()
print(data)