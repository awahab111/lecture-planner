from tabulate import tabulate
from termcolor import colored

class Lecture:
    def __init__(self, course, theory_lab, section, section_strength, professor, 
                 first_lecture_day, first_lecture_timeslot, first_lecture_room, 
                 first_lecture_room_size, second_lecture_day, second_lecture_timeslot, 
                 second_lecture_room, second_lecture_room_size):
        
        self.course = course
        self.theory_lab = theory_lab # 1 or 0 for theory or lab
        self.section = section
        self.section_strength = section_strength
        self.professor = professor
        self.first_lecture_day = first_lecture_day
        self.first_lecture_timeslot = first_lecture_timeslot
        self.first_lecture_room = first_lecture_room
        self.first_lecture_room_size = first_lecture_room_size
        self.second_lecture_day = second_lecture_day
        self.second_lecture_timeslot = second_lecture_timeslot
        self.second_lecture_room = second_lecture_room
        self.second_lecture_room_size = second_lecture_room_size

    def print(self):
        print('Course: ', self.course)
        print('Theory/Lab: ', self.theory_lab)
        print('Section: ', self.section)
        print('Section Strength: ', self.section_strength)
        print('Professor: ', self.professor)
        print('First Lecture Day: ', self.first_lecture_day)
        print('First Lecture Timeslot: ', self.first_lecture_timeslot)
        print('First Lecture Room: ', self.first_lecture_room)
        print('First Lecture Room Size: ', self.first_lecture_room_size)
        print('Second Lecture Day: ', self.second_lecture_day)
        print('Second Lecture Timeslot: ', self.second_lecture_timeslot)
        print('Second Lecture Room: ', self.second_lecture_room)
        print('Second Lecture Room Size: ', self.second_lecture_room_size)
    