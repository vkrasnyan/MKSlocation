import json
import urllib.request
import turtle
import time

from typing import List, Dict, Any
from http.client import HTTPResponse


def main():
    url: str = 'http://api.open-notify.org/astros.json'
    res: HTTPResponse = urllib.request.urlopen(url)
    result: Dict[str, Any] = json.loads(res.read())
    with open('iss.txt', 'w') as file:
        file.write(f'Now there are {str(result["number"])} astronauts:\n\n')
        print('В настоящий момент на МКС ' + str(result["number"]) + ' космонавтов:\n')
        people: List[Dict[str, str]] = result['people']
        for person in people:
            file.write(person['name'] + '\n')
            print(person['name'])

        screen: turtle.Screen = turtle.Screen()
        screen.setup(1280, 720)
        screen.setworldcoordinates(-180, -90, 180, 90)

        # загружааем изображение карты мира из файла
        screen.bgpic('map.gif')
        # загружаем изображение станции из файла
        screen.register_shape('iss.gif')
        # присваиваем переменной iss значение объекта Turtle
        iss = turtle.Turtle()
        # придаём переменной вид изображения станции из файла
        iss.shape('iss.gif')
        # выключаем функцию рисования следа от объекта Turtle()
        iss.penup()

        while True:

            url: str = 'http://api.open-notify.org/iss-now.json'
            res: HTTPResponse = urllib.request.urlopen(url)
            result: Dict[str, Dict[str, str]] = json.loads(res.read())

            # извлекаем локацию станции
            location: Dict[str, str] = result['iss_position']
            # извлекаем только широту станции
            lat: float = float(location['latitude'])
            # извлекаем только долготу станции
            lon: float = float(location['longitude'])

            # Получение текущего времени
            current_time: str = time.strftime("%Y-%m-%d %H:%M:%S")
            print("\nДата и время:", current_time)
            print(f'Широта: {lat}')
            print(f'Долгота: {lon}')

            # обновляем локация станции на карте
            iss.goto(lon, lat)

            # обновляем каждые 5 секунд
            time.sleep(5)

if __name__ == '__main__':
    main()