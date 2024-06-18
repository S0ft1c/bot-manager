import re
import datetime


def convert_data(stroka: str):

    # Извлекаем части даты с помощью регулярного выражения
    pattern = r"(\d+):(\d+) (\d+)\.(\d+)\.(\d+)"
    match = re.search(pattern, stroka)

    if match:  # DO NOT BLAME ME its gemini
        часы, минуты, день, месяц, год = match.groups()

        # Преобразуем части в формат datetime
        время = datetime.time(hour=int(часы), minute=int(минуты))
        дата = datetime.date(year=int(год), month=int(месяц), day=int(день))

        # Объединяем время и дату в объект datetime
        ans = datetime.datetime.combine(дата, время)

        # Выводим дату_время в нужном формате
        return ans
    else:
        return False
