'''
Code plan:

Нейросеть для видеонаблюдения (сторонняя утилита) и видеонаблюдение В СЛЕДУЮЩЕЙ ЖИЗНИ
Сайт для просмотра камер В СЛЕДУЮЩЕЙ ЖИЗНИ
Поиск URL остановки по координатам
Поиск улицы по координатам
Прокси 
Погода GOTOVO
TG Api Audio +GOTOVO
Получение видео через реквесты готово
Монтаж гифок 
Обновление получения данных
Completed (fix timer) - Обновление интерфейса GOTOVO


Mirage
tg - @aio2139
'''


#Импорт сторонних утилит

#Утилиты системы
import util #Адаптация названия файлов + Работа над анимациями
#import get_location #Получение локации

#Графический фреймворк
import kivy
import kivymd
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivymd.app import MDApp 
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.metrics import sp

import requests #Библиотека запросов
from fake_useragent import UserAgent #Библиотека ложных заголовков
from bs4 import BeautifulSoup #Библиотека чтения html файлов

#Библиотека системы
import os 
import os.path

import socket

from gtts import gTTS #озвучка

#Библиотеки для работы таймера
import schedule 
import time
import threading

#Глобальные переменные
get_location = False
#videoget = requests.get("https://rasa-test.surdo24.ru/dict/signs?search=&page=1")
current_temperature_2m, current_relative_humidity_2m, current_weather, current_wind_speed_10m = 0,0,0,0
REMOTE_SERVER = "18.192.94.96"

def is_connected(hostname):
  try:
    host = socket.gethostbyname(hostname)
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except Exception:
      pass
  return False



#Проверка надобности получения координат остановки
if get_location == False:
    street = "Малая Морская улица, 7, Санкт-Петербург" #Улица, отображаемая на карте в интерфейсе
    parse_url = "https://yandex.ru/maps/2/saint-petersburg/stops/stop__10075076/?indoorLevel=1&ll=30.316053%2C59.935873&tab=overview&z=17.26" #URL остановки в Y.Maps
#else:
#    get_location.main()
    
# Генерируем случайный заголовок
ua = UserAgent()
randomheaders = ua.random
print("Fake headers: ", randomheaders)
headers = {'User-Agent': randomheaders}

#Основной код

# Работа с графикой
Window.fullscreen = 'auto'

# Функция для получения координат остановвки   
def get_coordinates(location):
    print("Getting coordinates in process")
    global latitude, longtitude
    api_key = "5873c1b5-35c9-4048-9850-0d1e38ee9cd3"
    #api_key = "65ec9a88621c6118463610tfqbc81f3"

    url_api = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={location}&format=json"
    # https://geocode.maps.co/search?q={location}&api_key={api_key}
    # https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={location}&format=json
    
    try:
        response = requests.get(url_api, headers=headers).json()
        coordinates = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        longitude, latitude = map(float, coordinates.split())
        print(latitude,"\n",longitude)
        return latitude, longitude
    except Exception as e:
        # Обработка ошибки при запросе к API или при извлечении координат
        print(f"Произошла ошибка: {e}")

# Функция для парсинга данных

def parse_bus(url):
    try:
        print("Parsing pub transport")
        req = requests.get(url, headers=headers)
        html_content = req.text

        with open("info\Content.html", "w", encoding="utf-8") as file:
            file.write(html_content)
            file.close()
    except Exception as e:
        print(e)
#Функция для получения информации из файла

def get_info():
    global tram_list, bus_list, minibus_list, trollbus_list, bus_time, first_bus, stop_name, buses, trollbuses, trams
    try:
        print("Trying to get info")
        with open("info\Content.html", "r", encoding="utf-8") as file:
            bs = BeautifulSoup(file, "lxml")
            stop_name = bs.find("h1", class_="card-title-view__title").text
            bus_list = bs.find_all("div", class_="masstransit-transport-list-view__type-transport _type_bus _highlighted")
            minibus_list = bs.find_all("div", class_="masstransit-transport-list-view__type-transport _type_minibus _highlighted")
            trollbus_list = bs.find_all("div", class_="masstransit-transport-list-view__type-transport _type_trolleybus _highlighted")
            tram_list = bs.find_all("div", class_="masstransit-transport-list-view__type-transport _type_tramway _highlighted")
            first_bus = bs.find("span", class_="masstransit-vehicle-snippet-view__main-text")
            bus_time = bs.find("span", class_="masstransit-prognoses-view__title-text")
            file.close()
        buses, trollbuses, trams = [],[],[]  #Списки ТС  
        for bus in bus_list:
            buses.append(bus.text + "\n")
        for bus in minibus_list:
            buses.append(bus.text + '\n')
        print(buses)
        for trollbus in trollbus_list:
            trollbuses.append(trollbus.text + '\n')
        print(trollbuses)
        for tram in tram_list:
            trams.append(tram.text + '\n')
        print(trams)
    except Exception as e:
        print(e)


#Погода

def get_weather():
    global latitude, longitude, current_temperature_2m, current_relative_humidity_2m, current_weather, current_wind_speed_10m
    
    import openmeteo_requests
    import requests_cache
    import pandas as pd
    from retry_requests import retry
    
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)


    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
            "latitude": f'{latitude}',
            "longitude": f'{longitude}',
            "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m"],
            "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_weather_code = current.Variables(2).Value()
    c = current_weather_code
    current_wind_speed_10m = current.Variables(3).Value()

    current_weather = ""

    if c == 1 or c == 2 or c == 3:
        current_weather = "Пасмурно"
    elif c == 0:
        current_weather = "Ясно"
    elif c == 45 or c == 48:
        current_weather = "Туман"
    elif c == 51 or c == 53 or c == 55:
        current_weather = "Небольшой дождь"
    elif c ==56 or c == 57:
        current_weather = "Небольшой дождь с морозом"
    elif c == 61 or c == 63 or c == 65:
        current_weather = "Дождь"
    elif c == 66 or c == 67:
        current_weather = "Дождь с морозом"
    elif c == 71 or c == 73 or c == 75:
        current_weather = "Снегопад"
    elif c == 77:
        current_weather = "Небольшой снег"
    elif c == 80 or c == 81 or c == 82:
        current_weather = "Ливень"
    elif c == 85 or c == 86:
        current_weather = "Сильный снегопад"
    elif c == 95:
        current_weather = "Ливень с грозой"
    elif c == 96 or c == 99:
        current_weather = "Град с грозой"



    print(f"Current time {current.Time()}")
    print(f"Current temperature_2m {current_temperature_2m}")
    print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
    print(f"Current weather_code {current_weather_code}")
    print(f"Current weather {current_weather}")
    print(f"Current wind_speed_10m {current_wind_speed_10m}")


# Функция для получения статического изображения карты
def get_map(location):
    print("Getting a map in process")
    global latitude, longitude
    # Получение координат остановки
    latitude, longitude = get_coordinates(location)
    try:
        # Создание запроса к Yandex Static API для получения статического изображения карты
        url = f"http://static.maps.2gis.com/1.0?center={longitude},{latitude}&zoom=18&size=800,650"
        response = requests.get(url,headers=headers)
    except Exception as e:
        print(e)
    
    # Сохранение изображения карты
    with open("graph\\map.png", "wb") as f:
        f.write(response.content)
    return url, latitude, longitude


#Получение жеста номера автобуса

def get_video(num):
    try:
        data = videoget.json()[2]['signs']
        for i in range(len(data)):
            if data[i]['text']==str(num):
                return data[i]['link']
    except Exception as ex :return("Error -", ex)
        
    
def download_video(num, bus):
    if get_video is not None:
        try:
            response = requests.get(get_video(num))
            if response.status_code == 200:
                folder_path = f'temp_files\\videos'  # Название папки, куда сохранять видео
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, f'{bus}.mp4')
                
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Video saved as {file_path}")
            else:
                print("Failed to download")
        except Exception as ex:
            print("Error - ", ex)
    else: return "uncorrect value"




#Код GUI
class Bus_NUmber(MDBoxLayout):
    def update_labels(self, *args):
        layout = self
        global trollbuses,buses,trams,stop_name,first_bus, current_temperature_2m, current_relative_humidity_2m, current_weather, current_wind_speed_10m
        print("Update in process")
        #parse_bus(parse_url)
        #get_weather()
        Label_weather = layout.ids.weather
        Label_weather.text = f"Температура - {int(current_temperature_2m)}С°    Погода - {current_weather}    Ветер - {int(current_wind_speed_10m)}км/ч    Влажность - {int(current_relative_humidity_2m)}г/м3"
        spaces = len(Label_weather.text[14:20])*" "
        lbl_icos = layout.ids.wico
        lbl_icos = f"thermometer{spaces}partly_cloudy_day  air humidity_percentage"
        get_info()
        Label_Bus = layout.ids.list_label
        Label_Bus.text = "\n\n\n\n\n\n\nСписок номеров машин общественного транспорта:\n"
        all_elements = len(buses+trollbuses+trams)
        if buses != []:
           Label_Bus.text += "Автобус №"+"Автобус №".join(buses) # отображение списка автобусов на экран
        if trollbuses != []:
           Label_Bus.text += "Троллейбус №"+"Троллейбус №".join(trollbuses) # отображение списка троллейбусов на экран
        if trams != []:
            Label_Bus.text += "Трамвай №"+"Трамвай №".join(trams) # отображение списка трамваев на экран
        Label_Bus.text += "\n"*(16-all_elements)
        label_street=layout.ids.street_name 
        label_street.text="Остановка общественного транспорта:\n" + stop_name# отображение названия остановки
        firstbus = layout.ids.first_bus
        
        firstbus.text = f"\nТранспортное средство №{first_bus.text}   -   {bus_time.text}" # отображение ближайшего автобуса
        if bus_time.text == "прибывает":
            print("Sound func in process")
            bus = util.change_name(first_bus.text)
            gifka = f"graph\\{bus}.gif"
            if os.path.exists(gifka) == True:
                layout.ids.gif.source = gifka
            else:
                print(f"{int(first_bus.text)}      {bus}")
                download_video(int(first_bus.text),bus)
                util.merge(bus)
                layout.ids.gif.source = gifka
            try:
                if os.path.exists(f"audio\\{bus}.mp3") == False or os.path.exists(f"audio\\{bus}_eng.mp3") == False:
                    tts = gTTS(f"Транспортное средство номер {first_bus.text} прибывает на остановку", lang = "ru")
                    tts.save(f"audio\\{bus}.mp3")
                    tts = gTTS(f"Vehicle number {first_bus.text} is arriving to the bus station", lang = "en")
                    tts.save(f"audio\\{bus}_eng.mp3")
                    sound = SoundLoader.load(f"audio\\{bus}.mp3")
                    sound.play()
                    time.sleep(5)
                    sound = SoundLoader.load(f"audio\\{bus}_eng.mp3")
                    sound.play()
                else:
                    sound = SoundLoader.load(f"audio\\{bus}.mp3")
                    sound.play()
                    time.sleep(5)
                    sound = SoundLoader.load(f"audio\\{bus}_eng.mp3")
                    sound.play()
            except Exception as e:
                print(e)
        elif int(bus_time.text[0]) <= 5:
            print("Sound func in process")
            bus = util.change_name(first_bus.text)
            bt = util.change_name(bus_time.text[0])
            #gifka = f"graph\\{bus}.gif"
            #if os.path.exists(gifka) == True:
            #    layout.ids.gif.source = gifka
            #else:
            #    print(f"{int(first_bus.text)}      {bus}")
            #    download_video(int(first_bus.text),bus)
            #    util.merge(bus)
            #    layout.ids.gif.source = gifka
            try:
                if os.path.exists(f"audio\\{bus}_{bt}.mp3") == False or os.path.exists(f"audio\\{bus}_{bt}_eng.mp3") == False:
                    tts = gTTS(f"Транспортное средство номер {first_bus.text} прибывает на остановку через {bus_time.text}", lang = "ru")
                    tts.save(f"audio\\{bus}_{bt}.mp3")
                    tts = gTTS(f"Vehicle number {first_bus.text} is arriving to the bus station in {bus_time.text}", lang = "en")
                    tts.save(f"audio\\{bus}_{bt}_eng.mp3")
                    sound = SoundLoader.load(f"audio\\{bus}_{bt}.mp3")
                    sound.play()
                    time.sleep(5)
                    sound = SoundLoader.load(f"audio\\{bus}_{bt}_eng.mp3")
                    sound.play()
                else:
                    sound = SoundLoader.load(f"audio\\{bus}_{bt}.mp3")
                    sound.play()
                    time.sleep(5)
                    sound = SoundLoader.load(f"audio\\{bus}_{bt}_eng.mp3")
                    sound.play()
            except Exception as e:
                print(e)    
        else:
            layout.ids.gif.source = ""

KV = '''
MDScreen:
  MDLabel:
    font_size: 250
    text:"wifi_off"
    theme_font_name: "Custom"
    font_name: "MaterialSymbols"
    orientation: 'horizontal'
    padding: (800,0,0,200)
  MDLabel:
    font_size: 50
    text:"Нет подключения к сети"
    orientation: 'horizontal'
    padding: (650,50,0,0)
          '''
class Example(MDApp):
      def build(self):
          self.theme_cls.theme_style = "Dark"
          return Builder.load_string(KV)
    

# В методе build() класса MyApp добавляем вызов Clock.schedule_interval() для обновления данных:    
#  Основной класс программы
class MyApp(MDApp):
    def build(self):
        layout = Bus_NUmber()
        Clock.schedule_interval(layout.update_labels, 10)
        return layout
if __name__=="__main__":
    con_check = is_connected(REMOTE_SERVER)
    if con_check == True:
        #latitude, longitude = get_coordinates(street)
        #parse_bus(parse_url)
        #get_map(street)
        #get_weather()
        get_info()
        MyApp().run()
    '''else:
        while True:
          Example().run()
          con_check = is_connected(REMOTE_SERVER)
          print(con_check)
          if con_check == True:
            Example().stop()
            break
          time.sleep(5)
        #latitude, longitude = get_coordinates(street)
        #parse_bus(parse_url)
        #get_map(street)
        #get_weather()
        get_info()
        MyApp().run()
'''
