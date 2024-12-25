import requests
import datetime

yr = datetime.date.today().year


# API Производственный календарь
def calendar():
    rq = requests.get(f"https://xmlcalendar.ru/data/ru/{yr}/calendar.json")
    return rq


# Количество часов в году
def year_hours():
    year_hours = calendar().json().get("statistic").get("hours40")
    return year_hours


# Количество дней в месяце
def days_count(num):
    months = calendar().json().get("months")
    num = months[num - 1]["month"]
    days_31 = [1, 3, 5, 7, 8, 10, 12]
    days_30 = [4, 6, 9, 11]
    days_f = [2]
    if num in days_31:
        return 31
    elif num in days_30:
        return 30
    elif num in days_f:
        if yr % 4 != 0:
            return 28

        elif yr % 100 == 0:
            if yr % 400 == 0:
                return 29
            else:
                return 28
        else:
            return 29
    else:
        return 0


# Количество часов в месяце
def month_hours(month_num):
    months = calendar().json().get("months")
    month = months[month_num - 1]["days"].split(',')
    len_month = len(month)
    cnt = 0

    for i in month:
        if '*' in i:
            cnt += 1

    result = ((days_count(month_num) - len_month + cnt) * 8) - cnt

    return result


# ЗП за месяц по СУРВ
def money(num, month_num):
    result = num * 12 / year_hours() * month_hours(month_num)
    result_real = result - result / 100 * 13
    return round(result, 2), round(result_real, 2)
