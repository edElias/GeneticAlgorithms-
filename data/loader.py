from model.activity import Activity
from model.room import Room


ACTIVITIES = [
    Activity("SLA101A", 40, ["Glen", "Lock", "Banks"], ["Numen", "Richards", "Shaw", "Singer"]),
    Activity("SLA101B", 35, ["Glen", "Lock", "Banks"], ["Numen", "Richards", "Shaw", "Singer"]),
    Activity("SLA191A", 45, ["Glen", "Lock", "Banks"], ["Numen", "Richards", "Shaw", "Singer"]),
    Activity("SLA191B", 40, ["Glen", "Lock", "Banks"], ["Numen", "Richards", "Shaw", "Singer"]),
    Activity("SLA201",  60, ["Glen", "Banks", "Zeldin", "Lock", "Singer"], ["Richards", "Uther", "Shaw"]),
    Activity("SLA291",  50, ["Glen", "Banks", "Zeldin", "Lock", "Singer"], ["Richards", "Uther", "Shaw"]),
    Activity("SLA303",  25, ["Glen", "Zeldin"], ["Banks"]),
    Activity("SLA304",  20, ["Singer", "Uther"], ["Richards"]),
    Activity("SLA394",  15, ["Tyler", "Singer"], ["Richards", "Zeldin"]),
    Activity("SLA449",  30, ["Tyler", "Zeldin", "Uther"], ["Zeldin", "Shaw"]),
    Activity("SLA451",  90, ["Lock", "Banks", "Zeldin"], ["Tyler", "Singer", "Shaw", "Glen"]),
]

ROOMS = [
    Room("Beach 201",  18),
    Room("Beach 301",  25),
    Room("Frank 119",  95),
    Room("Loft 206",   55),
    Room("Loft 310",   48),
    Room("James 325", 110),
    Room("Roman 201",  40),
    Room("Roman 216",  80),
    Room("Slater 003", 32),
]

TIMES = ["10AM", "11AM", "12PM", "1PM", "2PM", "3PM"]

FACILITATORS = [
    "Lock", "Glen", "Banks", "Richards", "Shaw",
    "Singer", "Uther", "Tyler", "Numen", "Zeldin"
]


def get_activities():
    return ACTIVITIES

def get_rooms():
    return ROOMS

def get_times():
    return TIMES

def get_facilitators():
    return FACILITATORS