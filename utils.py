from tabulate import tabulate
from termcolor import colored
import random
import string

def printTable(lectures, timeslots):
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
            # Find lectures in this timeslot
            lectures_in_timeslot = [l for l in lectures if (l.first_lecture_day == day and l.first_lecture_timeslot == timeslot) or (l.second_lecture_day == day and l.second_lecture_timeslot == timeslot)]
            if lectures_in_timeslot:
                lecture_info = ', '.join([colored(lecture.course + " " + str(lecture.section) + " " + str(lecture.first_lecture_room) , 'green') if lecture.first_lecture_timeslot == timeslot else colored(lecture.course + " " + str(lecture.section) + " "  +str(lecture.second_lecture_room), 'blue') for lecture in lectures_in_timeslot])
                row.append(lecture_info)
            else:
                row.append('-')  # No lecture in this timeslot
        table.append(row)

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


def randomSections(num):
    sectionSize = []
    for _ in range(num):
        sectionSize.append(random.randint(20, 60))
    
    # Decrease the probability of large sections
    sectionSize = [size if size <= 60 else random.randint(20, 80) for size in sectionSize]
    
    return sectionSize
    
def randomRooms(num):
    roomsize = []
    
    for _ in range(num):
        weight = [0.1, 0.9]
        roomsize.append(random.choices(["Large Hall", "Classroom"], weight)[0])
    
    return roomsize

def has_conflict(lecture1, lecture2):
    # Check for professor conflicts
    # if lecture1.professor == lecture2.professor:
    #     if lecture1.first_lecture_day == lecture2.first_lecture_day and lecture1.first_lecture_timeslot == lecture2.first_lecture_timeslot:
    #         return True
    #     if lecture1.second_lecture_day == lecture2.second_lecture_day and lecture1.second_lecture_timeslot == lecture2.second_lecture_timeslot:
    #         return True

    # Check for room conflicts
    if lecture1.first_lecture_room == lecture2.first_lecture_room and lecture1.first_lecture_day == lecture2.first_lecture_day and lecture1.first_lecture_timeslot == lecture2.first_lecture_timeslot:
        return True
    if lecture1.second_lecture_room == lecture2.second_lecture_room and lecture1.second_lecture_day == lecture2.second_lecture_day and lecture1.second_lecture_timeslot == lecture2.second_lecture_timeslot:
        return True

    # Check for section conflicts
    # if lecture1.section == lecture2.section:
    #     if lecture1.first_lecture_day == lecture2.first_lecture_day and lecture1.first_lecture_timeslot == lecture2.first_lecture_timeslot:
    #         return True
    #     if lecture1.second_lecture_day == lecture2.second_lecture_day and lecture1.second_lecture_timeslot == lecture2.second_lecture_timeslot:
    #         return True

    return False


def timeConflicts(lectures):
    for i in range(len(lectures)):
        for j in range(i+1, len(lectures)):
            lecture1 = lectures[i]
            lecture2 = lectures[j]
            if has_conflict(lecture1, lecture2):
                print("There is a conflict between the two lectures.")
                lecture1.print()
                lecture2.print()
