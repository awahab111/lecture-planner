import random
from lecture import Lecture
import math
import utils as util


professors = ['Prof. Smith', 'Prof. Johnson', 'Prof. Williams', 'Prof. Brown']
courses = ['Math101', 'Physics101', 'Chemistry101', 'Biology101']
theory_lab = ['Theory', 'Lab']
sections = util.randomSections(4)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
timeslots = ['8:30', '10:05', '11:40', '1:15', '2:50']
roomDict = util.randomRooms(4)
print(roomDict)
lectures = []

for _ in range(10):  # Generate 10 random lectures
    course = random.choice(courses)
    t_l = random.choice(theory_lab)
    section = random.choice(list(sections.keys()))
    section_strength = sections[section]
    professor = random.choice(professors)
    first_day = random.choice(days)
    first_timeslot = random.choice(timeslots)
    first_room = random.choice(list(roomDict.keys()))
    first_room_size = roomDict[first_room]
    second_day = random.choice(days)
    second_timeslot = random.choice(timeslots)
    second_room = random.choice(list(roomDict.keys()))
    second_room_size = roomDict[second_room]

    lecture = Lecture(course, t_l, section, section_strength, professor, 
                      first_day, first_timeslot, first_room, first_room_size, 
                      second_day, second_timeslot, second_room, second_room_size)
    
    lectures.append(lecture)


def toBinary(lecture):
    # Define the possible values for each attribute
    attributes = {
        'course': courses,
        'theory-lab': theory_lab,
        'section': list(sections.keys()),
        'section-strength': list(sections.values()),  # Get section strength from sections dictionary
        'professor': professors,
        'first-lecture-day': days,
        'first-lecture-timeslot': timeslots,
        'first-lecture-room': list(roomDict.keys()),
        'first-lecture-room-size': list(roomDict.values()),  # Get room size from roomDict dictionary
        'second-lecture-day': days,
        'second-lecture-timeslot': timeslots,
        'second-lecture-room': list(roomDict.keys()),
        'second-lecture-room-size': list(roomDict.values())  # Get room size from roomDict dictionary
    }

    # Generate a binary string for each attribute
    chromosome = ''
    for attribute, values in attributes.items():
        # Calculate the number of bits needed to represent the attribute
        num_bits = math.ceil(math.log2(len(values)))
        
        # Get the value of the attribute from the lecture object
        value = lecture.__dict__[attribute.replace('-', '_')]
        
        # Find the index of the value in the list of possible values
        index = values.index(value)
        
        # Convert the index to a binary string and pad it with zeros to the required length
        binary_string = format(index, '0' + str(num_bits) + 'b')
        
        # Add the binary string to the chromosome
        chromosome += binary_string

    return chromosome


print(toBinary(lectures[0]))

util.printTable(lectures, timeslots)