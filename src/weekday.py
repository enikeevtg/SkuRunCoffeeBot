from datetime import datetime


def get_weekday():
    weekdays = 'Mon Tue Wed Thu Fri Sat Sun'.split()
    return weekdays[datetime.today().weekday()]


if __name__ == '__main__':
    print(get_weekday())
