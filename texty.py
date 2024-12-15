import speech_recognition as sr
from pyttsx3 import speak
import pywhatkit
import webbrowser
from datetime import datetime
import time
import requests
import pyjokes
from bs4 import BeautifulSoup


API_KEY = "ed90488c7c793f2a1a6e52a02fd51538"
base_url = "https://api.openweathermap.org/data/2.5/weather/"

listener = sr.Recognizer()


def get_sound():
    try:
        print('listening...')
        speak('listening...')

        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
    except:
        pass
    return command


def codechef_ratings(a):
    usernames = ['dhanush_30',
                 'sidhu4641', 'siddu2355', 'hellfire2004', 'gkey_akhilsaik']
    key=a
    for username in usernames:
        html = requests.get(f"https://codechef.com/users/{key}").text
        soup = BeautifulSoup(html, 'lxml')
        name = soup.find('h1', class_='h2-style').text
        rating_div = soup.find('div', class_='rating-number')
        if rating_div is not None:
            rating = int(rating_div.text[0:4].replace(
                "?", "").replace("i", ''))
        else:
            rating = 0
        print(f'''[
        username: {username},
        name: {name},
        rating: {rating}
],''')


def codeforces_ratings():
    speak("Enter your codeforces username: ")
    username = input("Enter your codeforces username: ")
    html = requests.get(f"https://codeforces.com/profile/{username}").text
    soup = BeautifulSoup(html, 'lxml')
    tag_div = soup.find('div', class_="user-rank")
    nop_div = soup.find('div', class_="_UserActivityFrame_counterValue")
    if tag_div is None:
        tag = "Invalid Username."
    else:
        tag = tag_div.span.text
    if nop_div is None:
        nop = "Invalid Username."
    else:
        nop = nop_div.text.replace(" problems","")

    if nop == "Invalid Username.":
        print("Invalid Username.")
        speak("Invalid Username.")
    else:
        print(f'''[
        username: {username},
        tag: {tag},
        number of problems solved: {nop}
],''')


def open_yT(comman):
    song = comman.replace('play', '')
    speak('playing ' + song)
    print('playing ' + song)
    pywhatkit.playonyt(song)


def get_curtime():
    time = datetime.now().strftime('%I:%M %p')
    print('Current time is ' + time)
    speak('Current time is ' + time)


def google_command():
    speak("what do you what to search")
    search_key = input("What do you want to search: ")
    print(f"Searching {search_key}")
    speak(f"Searching {search_key}")
    url = f"https://www.google.com/search?q={search_key}"
    webbrowser.get().open(url)


def location():
    speak("which place you want to search")
    searchLo = input("Which place do you want to Locate: ")
    print(f"Searching {searchLo}")
    speak(f"Searching {searchLo}")
    url = f"https://www.google.com/maps?q={searchLo}"
    webbrowser.get().open(url)


def get_a_joke():
    jok = pyjokes.get_joke()
    print(jok)
    speak(jok)


def whatsapp_message():
    contacts = {
        "bro": "+919391198374",
        "pranav": "+919347349353",
        "player": "+917989267277",
        "grand player": "+918333931019",
    }
    time = datetime.now().strftime('%I:%M %p')
    min = int(time[3:5])
    hour = int(time[0:2])
    ap = time[6:8]
    if hour != 00 and hour != 12:
        hour += 12
        speak("To whom you want to send message to: ")
        name = input("To whom you want to send a message: ")
        x = 0
        for i in contacts:
            if i == name:
                x = 1
                speak(f"what is your message to {i}")
                messa = input(f"What is your message to {i}: ")
                print(f"your message to {i} is \'{messa}\'")
                pywhatkit.sendwhatmsg(contacts[i], messa, hour, min+2)
        if x == 0:
            print(f"{name} is not in your contacts. ")
            speak(f"{name} is not in your contacts. ")


def weather_report():
    speak("weather report of which city you want to look at? ")
    city = input("weather report of which city you want to look at: ")
    print(f"please wait fetching the weather report of {city}")
    speak(f"please wait fetching the weather report of {city}")

    response = requests.get(f"{base_url}?appid={API_KEY}&q={city}")
    if response.status_code == 200:
        data = response.json()
        result = {
            'lon': data['coord']['lon'],
            'lat': data['coord']['lat'],
            'temp': round(data["main"]['temp'] - 273, 2),
            'wind_speed': data['wind']['speed'],
            'pressure': data["main"]['pressure'],
            'humidity': data["main"]['humidity'],
        }
        print(f"""[
            city: {city}
            longitude: {result['lon']}
            latitude: {result['lat']}
            temperature: {result['temp']}
]""")
        speak(
            f"The current temperature in {city} is {str(result['temp'])} degrees centigrade.")
    elif response.status_code == 404:
        print(f"The city {city} does not Exist.")
        speak(f"The city {city} does not Exist.")


def wikipedia_info(wik):
    wiki = wik.replace("wikipedia ", "")
    inf = pywhatkit.info(wik)


def open_website(cmd):
    res = cmd.replace("open ", "")
    if res == "whatsapp":
        res = "web.whatsapp"
        print(f"opening whatspp.....")
        speak(f"opening whatsapp")
    else:
        print(f"opening {res}.....")
        speak(f"opening {res}")
    webbrowser.get().open(f"https://{res}.com")


def run_code():
    cmd = input("Enter a command: ")
    command = cmd.lower()
    if 'play' in command:
        open_yT(command)
    elif "wikipedia" in command:
        wikipedia_info(command)
    elif "name" in command:
        print("I am John.")
        speak("I am John.")
    elif "open" in command:
        open_website(command)
    elif "hello" in command:
        print("Hi There, how can i help you?")
        speak("Hi There, how can i help you?")
    elif 'time' in command:
        get_curtime()
    elif "codeforces" in command:
        codeforces_ratings()
    elif 'google' in command:
        google_command()
    elif 'locate' in command:
        location()
    elif 'joke' in command:
        get_a_joke()
    elif 'whatsapp' in command:
        whatsapp_message()
    elif "weather" in command:
        weather_report()
    elif "codechef" in command:
        a = input()
        codechef_ratings(a)
    elif 'exit' in command:
        return False
    else:
        print('Please say the command again.')
        speak('Please say the command again.')


print("Hello I'm Your personal Assistant.")
speak("Hello I'm Your personal Assistant.")


while True:
    time.sleep(1)
    if run_code() == False:
        break
    else:
        run_code()
