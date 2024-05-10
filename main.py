import requests
import csv
from datetime import datetime, timedelta


def fetch_weather_data(api_key, location, date):
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&dt={date}&aqi=no"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Date','Minimum Temperature (°C)', 'Maximum Temperature (°C)','Average Temperature (°C)', 'Condition', 'Chance of Rain (%)', 'Chance of Snow (%)',
                      'Total Snow (cm)', 'Average Visibility (km)', 'Sunrise', 'Sunset', 'Moonrise', 'Moonset']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    # Replace 'your_api_key_here' and 'London' with your actual API key and location
    api_key = '893e642c01654fb3a52221644240504'
    location = 'Montreal'

    # Find the date for tomorrow
    tomorrow = datetime.now() + timedelta(days=1)

    # Fetch weather data for each day from tomorrow up to the 10th day
    weather_data_list = []
    for i in range(0, 10):
        date = tomorrow + timedelta(days=i)
        weather_data = fetch_weather_data(api_key, location, date.strftime("%Y-%m-%d"))
        if weather_data:
            weather_data_dict = {
                'Date': date.strftime('%Y-%m-%d'),
                'Minimum Temperature (°C)': weather_data['forecast']['forecastday'][0]['day']['mintemp_c'],
                'Maximum Temperature (°C)': weather_data['forecast']['forecastday'][0]['day']['maxtemp_c'],
                'Average Temperature (°C)': weather_data['forecast']['forecastday'][0]['day']['avgtemp_c'],
                'Condition': weather_data['forecast']['forecastday'][0]['day']['condition']['text'],
                'Chance of Rain (%)': weather_data['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
                'Chance of Snow (%)': weather_data['forecast']['forecastday'][0]['day']['daily_chance_of_snow'],
                'Total Snow (cm)': weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm'],
                'Average Visibility (km)': weather_data['forecast']['forecastday'][0]['day']['avgvis_km'],
                'Sunrise': weather_data['forecast']['forecastday'][0]['astro']['sunrise'],
                'Sunset': weather_data['forecast']['forecastday'][0]['astro']['sunset'],
                'Moonrise': weather_data['forecast']['forecastday'][0]['astro']['moonrise'],
                'Moonset': weather_data['forecast']['forecastday'][0]['astro']['moonset']
            }
            weather_data_list.append(weather_data_dict)
        else:
            print(f"Failed to fetch weather data for {date.strftime('%Y-%m-%d')}")

    # Write weather data to CSV file
    print(weather_data_list)
    write_to_csv('weather_data.csv', weather_data_list)
    print("Weather data has been written to weather_data.csv")


if __name__ == "__main__":
    main()
