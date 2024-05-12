class Lecture:
    def __init__(self, course, theory_lab, section, professor, day, timeslot, room):
        self.course = course
        self.theory_lab = theory_lab
        self.section = section
        self.professor = professor
        self.day = day
        self.timeslot = timeslot
        self.room = room

class Section:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength

class Professor:
    def __init__(self, name):
        self.name = name
        self.courses_taught = []

class Room:
    def __init__(self, name, capacity, floor):
        self.name = name
        self.capacity = capacity
        self.floor = floor

class Course:
    def __init__(self, name, lectures_per_week, is_lab):
        self.name = name
        self.lectures_per_week = lectures_per_week
        self.is_lab = is_lab
