from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import requests, json

TOKEN: Final = 'enter_your_bot_token'
API: Final = "enter_your_weather_api_token"
BOT_USERNAME: Final = '@weather_bot_is_online_bot'

# -------------------------------------------------------- code


weather_icons = {
    "01d": "☀️",  # clear sky (day)
    "01n": "🌙",  # clear sky (night)
    "02d": "⛅️",  # few clouds (day)
    "02n": "⛅️",  # few clouds (night)
    "03d": "☁️",  # scattered clouds (day)
    "03n": "☁️",  # scattered clouds (night)
    "04d": "☁️",  # broken clouds (day)
    "04n": "☁️",  # broken clouds (night)
    "09d": "🌧",  # shower rain (day)
    "09n": "🌧",  # shower rain (night)
    "10d": "🌦",  # rain (day)
    "10n": "🌦",  # rain (night)
    "11d": "⛈",  # thunderstorm (day)
    "11n": "⛈",  # thunderstorm (night)
    "13d": "❄️",  # snow (day)
    "13n": "❄️",  # snow (night)
    "50d": "🌫",  # mist (day)
    "50n": "🌫",  # mist (night)
}

weather_image = {
    "01d": "https://img.freepik.com/premium-photo/vertical-image-white-clouds-blue-sky-morning_35782-208.jpg",  # clear sky (day)
    "01n": "https://wallpapers.com/images/hd/night-clear-sky-at-alps-6f53weasubiksxfb.jpg",  # clear sky (night)
    "02d": "https://img.freepik.com/premium-photo/blue-cloudy-sky-sunny-day-clouds-sunny-sky_666008-498.jpg",  # few clouds (day)
    "02n": "https://static.vecteezy.com/system/resources/thumbnails/011/504/901/small/lightning-in-the-night-sky-flashes-on-the-cloudscape-in-the-darkness-thunderbolt-effect-variations-fx-isolated-storm-with-lightning-bolt-lightning-strikes-in-the-clouds-in-the-dark-thunderstorm-video.jpg",  # few clouds (night)
    "03d": "https://pixabay.com/photos/sky-clouds-dark-clouds-sunbeams-1494656/",  # scattered clouds (day)
    "03n": "https://pixabay.com/illustrations/darling-star-night-space-light-1695067/",  # scattered clouds (night)
    "04d": "https://live.staticflickr.com/65535/50026176147_f70671b807_b.jpg",  # broken clouds (day)
    "04n": "https://live.staticflickr.com/5758/22448249491_e3e9ddcddf_b.jpg",  # broken clouds (night)
    "09d": "https://ewscripps.brightspotcdn.com/dims4/default/614d72d/2147483647/strip/true/crop/3021x1699+326+121/resize/1280x720!/quality/90/?url=http%3A%2F%2Fewscripps-brightspot.s3.amazonaws.com%2Fb1%2F2e%2F2e386b204320b99187b980ed2dbe%2Fscreen-shot-2020-11-08-at-9.25.06%20PM.png",  # shower rain (day)
    "09n": "https://www.thoughtco.com/thmb/beiCvc1QcvpjjJPXI6g0wG18MxI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/drops-of-rain-on-glass-838815210-5a823cc0a18d9e0036e325e2.jpg",  # shower rain (night)
    "10d": "https://w0.peakpx.com/wallpaper/390/367/HD-wallpaper-rainy-day-rainy-day.jpg",  # rain (day)
    "10n": "https://pixabay.com/illustrations/oil-rain-christmas-s%C3%A3o-paulo-art-4657212/",  # rain (night)
    "11d": "https://pixabay.com/illustrations/ai-generated-artistic-artwork-7640159/",  # thunderstorm (day)
    "11n": "https://pixabay.com/illustrations/storm-thunderstorm-lightnings-7974474/",  # thunderstorm (night)
    "13d": "https://th-i.thgim.com/public/incoming/jwawgl/article66487130.ece/alternates/FREE_1200/20230131043L.jpg",  # snow (day)
    "13n": "https://m.media-amazon.com/images/I/71C2R0mjx+L.jpg",  # snow (night)
    "50d": "https://images.freeimages.com/images/large-previews/11e/foggy-day-1335348.jpg",  # mist (day)
    "50n": "https://mir-s3-cdn-cf.behance.net/project_modules/disp/a3f9aa15334031.5628f9d28783d.jpg",  # mist (night)
}

def cord(location,apikey):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={apikey}"
    response = requests.get(url)
    data = response.json()
    # print(data)
    if data == []:
        return -1, -1
    elif data[0]['name'] .lower() == location.lower() or data[0]['name']:
        return data[0]['lat'] , data[0]['lon']
    else:
        return None, None

def ktoc(kelvin):
    return round(kelvin - 273.15)

def send_photo(chat_id, photo_url, caption):
    bot_token = TOKEN
    api_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    params = {
        'chat_id': chat_id,
        'photo': photo_url,
        'caption': caption,
        'width': 50,
        'height': 50
    }
    # print(params)
    response = requests.post(api_url, params=params)
    return response.json()
def main(api_key, loc):
    lat , lon  = cord(loc, api_key)
    # print(lat , lon)
    if lat is not None and lon is not None:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:

            location = loc
            weather_station = data['name']
            weather = data['weather'][0]['main']
            weather_desc = data['weather'][0]['description']

            weather_icon = data['weather'][0]['icon']
            weather_img = weather_image[weather_icon]
            weather_icon = weather_icons[weather_icon]

            current_temp = ktoc( data['main']['temp'] )
            feels_like = ktoc( data['main']['feels_like'] )
            min_temp = ktoc( data['main']['temp_min'] )
            max_temp = ktoc( data['main']['temp_max'] )

            return location, weather_station, weather, weather_desc, weather_icon, weather_img, current_temp, feels_like, min_temp, max_temp
        else:
            return 0, 0, 0, 0, 0, 0, 0, 0
    else:
        return 0, 0, 0, 0, 0, 0, 0, 0



# ------------------------------------------ Commands
async def start_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the WeatherBot! I can provide you with the current weather information of any city. Just use the '/weather city_name' command, and I'll fetch the weather details for you. Stay informed about the weather conditions and plan your day accordingly")

async def help_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here are the commands available on this bot:\n\n/start: Get a warm greeting from the bot.\n/weather city_name: Get the current weather information of a specific village, city, state, country.\n/help: Display the help page with a list of available commands.\n/custom: Explore custom commands and their functionalities.")

async def custom_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is the custom command section')

async def weather_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text
    chat_id = update.message.chat_id
    city = command.split(' ', 1)
    # print(city)
    # print("fffffffffffffffffff",city)
    if len(city)>1:
        # print(" hello ")
        api_key = API
        location, weather_station, weather, weather_desc, weather_icon, weather_img, current_temp, feels_like, min_temp, max_temp = main(api_key, city[1])
        # print(location, weather_station, weather, weather_desc, weather_icon, weather_img, current_temp, feels_like, min_temp, max_temp)
        if weather_station != "":
            caption = f"\nCurrent Weather Condition:   {weather}  {weather_icon}\n\nCurrent Temperature 🌡️: {current_temp}°c .\nMinimum Temperature 🌡️: {min_temp}°c .\nMaximum Temperature 🌡️: {max_temp}°c .\n\nWeather Location 🌍:   {location}\nWeather Station 🏢 is at {weather_station}\nWeather Description: {weather_desc}"
            send_photo(chat_id,weather_img, caption)
        else:
            await update.message.reply_text('Please Enter a valid Village, City, State, Country name')
    else:
        await update.message.reply_text('Please Enter a valid city name by < /weather city_name >')

# ===================================================== Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()

    # if 'hello' in text:
    #     return 'Hey there.'

    if 'hello' in processed:
        return 'Hey there.'

    if 'how are you' in processed:
        return 'Iam good.'

    if 'i love python' in processed:
        return 'I Love It too.'

    return 'I do not Understand it'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User({update.message.chat.id} in {message_type}: '{text}'')")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print("bot", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update{update} cause error {context.error}")

if __name__ == "__main__":
    print('Starting..........')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('weather', weather_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling.....')
    app.run_polling(poll_interval = 3)