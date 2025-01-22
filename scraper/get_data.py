import requests
import csv
from datetime import datetime

def get_lat_lon_from_zip(zip_code):
    # Using OpenCage Geocoder API for zip code to latitude/longitude conversion
    api_key = 'KEY GOES HERE'  # Get a free key from https://opencagedata.com/
    url = f'https://api.opencagedata.com/geocode/v1/json?q={zip_code}&key={api_key}'
    response = requests.get(url)
    print(response.status_code)
    print(response.text)  # This prints the raw response text

    # Parse the response to JSON
    data = response.json()  # Convert the response to a Python dictionary

    if data['results']:  # Accessing 'results' key in the parsed JSON data
        lat = data['results'][0]['geometry']['lat']
        lon = data['results'][0]['geometry']['lng']
        return lat, lon
    else:
        raise ValueError("Invalid zip code or location not found.")

def get_historical_weather_data(lat, lon, start_date, end_date):
    # Format the start and end date to match the API request
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Fetch the historical data from Visual Crossing Weather API
    api_key = 'KEY GOES HERE'  # Use your own Visual Crossing API key
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{start_date.date()}/{end_date.date()}?key={api_key}'
    
    print("Requesting weather data...")
    response = requests.get(url)
    
    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        try:
            data = response.json()
            
            if 'error' in data:
                raise ValueError("Error fetching historical data. Please check the dates and location.")
            
            weather_records = []
            for day in data['days']:
                # Extract date and weather details, including additional data points
                date = day['datetime']
                temperature = day.get('temp', 'N/A')
                humidity = day.get('humidity', 'N/A')
                wind_speed = day.get('windspeed', 'N/A')
                precipitation = day.get('precip', 'N/A')
                pressure = day.get('pressure', 'N/A')
                
                weather_records.append({
                    'Date': date,
                    'Temperature (F)': temperature,
                    'Humidity': humidity,
                    'Wind Speed (mph)': wind_speed,
                    'Precipitation (inches)': precipitation,
                    'Pressure (mb)': pressure
                })
            
            return weather_records
        except ValueError as e:
            print(f"Error processing the weather data: {e}")
            return []
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        print(f"Response: {response.text}")  # Print the raw response for debugging
        return []

def write_to_csv(weather_data, filename='weather_data.csv'):
    keys = weather_data[0].keys()
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(weather_data)

def main():
    zip_code = input("Enter the ZIP code: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    try:
        lat, lon = get_lat_lon_from_zip(zip_code)
        weather_data = get_historical_weather_data(lat, lon, start_date, end_date)
        
        if weather_data:
            write_to_csv(weather_data, filename=f"weather_data({zip_code}_{start_date}_{end_date}).csv")
            print(f"Weather data successfully saved to 'weather_data.csv'.")
        else:
            print("No data available for the given date range.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
