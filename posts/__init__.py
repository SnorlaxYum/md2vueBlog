from datetime import datetime, timedelta


def sortmethod(a, b):
    """sort posts in a descending order according to the date"""
    a_time = datetime.strptime(a['date'], '%Y-%m-%d %H:%M')
    b_time = datetime.strptime(b['date'], '%Y-%m-%d %H:%M')
    com_value = a_time - b_time
    if (com_value > timedelta(0)):
        return -1
    elif (com_value == timedelta(0)):
        return 0
    else:
        return 1


def parseGivenDate(dt):
    return "{dt:%B} {dt.day}, {dt.year}".format(dt=dt)
