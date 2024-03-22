import sys
import subprocess
import requests
from importlib.metadata import distributions

# List of required packages
required_packages = {'requests'}


# Function to check and install missing packages
def check_and_install_packages():
    installed_packages = {pkg.metadata['Name'] for pkg in distributions()}
    missing_packages = required_packages - installed_packages
    if missing_packages:
        print("Installing missing packages:", ", ".join(missing_packages))
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing_packages], stdout=subprocess.DEVNULL)


# Function to get weather data
def get_weather_data(api_key, area_code):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?zip={area_code},us&appid={api_key}&units=imperial"
    response = requests.get(complete_url)
    return response.json()


# Function to display weather data
def display_weather(data):
    if data["cod"] != 200:
        print("Failed to get weather data:", data.get("message", ""))
        return

    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    print(f"Weather: {weather}")
    print(f"Temperature: {temperature}°F")

    # ASCII art representations for different weather conditions
    ascii_art = {
        'clear sky': """
          \   /    
           .-.
       ― (   ) ―
           `-’     
          /   |
        """,
        'few clouds': """
           .--.
        .-(    ).-
       (___.__)__)
        """,
        'scattered clouds': """
             .-~~~-.
      .- ~ ~-(       )_ _
     /                    ~ -.
    |                          ',
     \                         .'
       ~- ._ ,. ,.,.,., ,.. -~
        """,
        'broken clouds': """
        \  / 
      .- /~~~\ -.
     ,-(     )-,'
       \    / 
        \  /
        """,
        'shower rain': """
         .-.
       (   ).
      (___(__)
       ‘ ‘ ‘ ‘
      ‘ ‘ ‘ ‘
        """,
        'rain': """
         .-.
       (   ).
      (___(__)
       ‘ ‘ ‘ ‘
      ‘ ‘ ‘ ‘
        """,
        'thunderstorm': """
        .-.      .-.
       (   ).   (   ).
      (___(__) (___(__)
       ‘ ‘ ‘ ‘  ‘ ‘ ‘ ‘
      ‘ ‘ ‘ ‘  ‘ ‘ ‘ ‘
        """,
        'snow': """
         .-.
       (   ).
      (___(__)
      *  *  * 
     *  *  * 
        """,
        'mist': """
        - - - - - - - - - - - - -
      - - - - - - - - - - - - - 
        - - - - - - - - - - - - -
      """,
    }

    # Find and print the ASCII art that matches the current weather condition
    for condition, art in ascii_art.items():
        if condition in weather:
            print(art)
            break
    else:
        print("No ASCII art for this weather condition.")


def main():
    check_and_install_packages()

    # Your OpenWeatherMap API key
    api_key = "f5fcbf104b8da6c79d9a4fda01e90c17"

    # User input for area code
    area_code = input("Enter your area code (ZIP code): ")

    # Fetch and display weather data
    weather_data = get_weather_data(api_key, area_code)
    display_weather(weather_data)


if __name__ == "__main__":
    main()
