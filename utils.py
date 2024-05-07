from tabulate import tabulate
from termcolor import colored
import random
import string

def printTable(lectures,timeslots):
    # Sort lectures by day and timeslot
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    lectures.sort(key=lambda x: (days.index(x.first_lecture_day), timeslots.index(x.first_lecture_timeslot)))


    # Prepare data for tabulate
    table = []
    header = ['Day'] + timeslots
    table.append(header)

    for day in days:
        row = [day]
        for timeslot in timeslots:
            # Find lecture in this timeslot
            lecture = next((l for l in lectures if l.first_lecture_day == day and l.first_lecture_timeslot == timeslot), None)
            if lecture:
                row.append(colored(lecture.course + " " + lecture.section, 'green'))
            else:
                row.append('-')  # No lecture in this timeslot
        table.append(row)
    
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


def randomSections(num):
    sections = string.ascii_uppercase
    sectionSize = []
    for _ in range(num):
        sectionSize.append(random.randint(20, 60))
    
    # Decrease the probability of large sections
    sectionSize = [size if size <= 60 else random.randint(20, 80) for size in sectionSize]
    
    sectionDict = {}
    for i in range(num):
        sectionDict[sections[i]] = sectionSize[i]
    
    return sectionDict

def randomRooms(num):
    room = string.ascii_uppercase
    roomsize = []
    
    for _ in range(num):
        weight = [0.1, 0.9]
        roomsize.append(random.choices(["Large Hall", "Classroom"], weight)[0])
    
    roomDict = {}
    for i in range(num):
        roomDict[room[i]] = roomsize[i]
    
    return roomDict