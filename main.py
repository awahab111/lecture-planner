import random
from tabulate import tabulate
from termcolor import colored
from lecture import Lecture


professors = ['Prof. Smith', 'Prof. Johnson', 'Prof. Williams', 'Prof. Brown']
courses = ['Math101', 'Physics101', 'Chemistry101', 'Biology101']
theory_lab = ['Theory', 'Lab']
sections = ['A', 'B', 'C', 'D']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
timeslots = ['9:00', '10:00', '11:00', '12:00', '1:00', '2:00', '3:00']
rooms = ['Room 101', 'Room 102', 'Room 103', 'Room 104']

lectures = []

for _ in range(10):  # Generate 10 random lectures
    course = random.choice(courses)
    t_l = random.choice(theory_lab)
    section = random.choice(sections)
    section_strength = random.randint(20, 50)  # Random number between 20 and 50
    professor = random.choice(professors)
    first_day = random.choice(days)
    first_timeslot = random.choice(timeslots)
    first_room = random.choice(rooms)
    first_room_size = random.randint(30, 60)  # Random number between 30 and 60
    second_day = random.choice(days)
    second_timeslot = random.choice(timeslots)
    second_room = random.choice(rooms)
    second_room_size = random.randint(30, 60)  # Random number between 30 and 60

    lecture = Lecture(course, t_l, section, section_strength, professor, 
                      first_day, first_timeslot, first_room, first_room_size, 
                      second_day, second_timeslot, second_room, second_room_size)
    
    lectures.append(lecture)

# Now you can use the lectures list
for lecture in lectures:
    lecture.print()


# Sort lectures by day and timeslot
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

# Print table
print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
