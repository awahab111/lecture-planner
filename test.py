import random
from tabulate import tabulate
from termcolor import colored 
import copy

# Constants
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
TIMESLOTS = ['8:30', '10:05', '11:40', '1:15', '2:50']
ROOM_CAPACITY = {'classroom': 60, 'large_hall': 120}

# Define classes
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
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

class Course:
    def __init__(self, name, lectures_per_week, is_lab):
        self.name = name
        self.lectures_per_week = lectures_per_week
        self.is_lab = is_lab

def generate_initial_population(population_size, courses, professors, sections, rooms):
    population = []
    for _ in range(population_size):
        timetable = []
        # Create a dictionary to store selected professors for each section and course
        p = copy.deepcopy(professors)
        selected_professors = {}
        for course in courses:
            for sec in sections:
                professor = random.choice(p)
                while len(professor.courses_taught) > 3:
                    professor = random.choice(p)
                selected_professors[(course, sec)] = professor
                professor.courses_taught.append(course)
        
        for course in courses:
            for sec in sections:

                if course.is_lab:
                    theory_lab = 'Lab'
                    professor = selected_professors[(course, sec)]  # Select the professor assigned to the section and course
                    room = random.choice(rooms)
                    day = [random.choice(DAYS)]
                    
                    # Choose a timeslot that is not the last one
                    available_timeslots = TIMESLOTS[:-1]
                    timeslot = random.choice(available_timeslots)
                    next_timeslot_index = TIMESLOTS.index(timeslot) + 1
                    next_timeslot = TIMESLOTS[next_timeslot_index]

                    timeslots = [timeslot, next_timeslot]
                    
                    lecture = Lecture(course.name, theory_lab, sec.name, professor.name, day, timeslots, room.name)
                    timetable.append(lecture)

                else:
                    theory_lab = 'Theory'
                    professor = selected_professors[(course, sec)]  # Select the professor assigned to the section and course
                    
                    room = random.choice(rooms)
                    day = random.choice(DAYS)
                    next_day = DAYS[(DAYS.index(day) + 2) % len(DAYS)]
                    days = [day, next_day]
                    timeslot = [random.choice(TIMESLOTS)]

                    lecture = Lecture(course.name, theory_lab, sec.name, professor.name, days, timeslot, room.name)
                    timetable.append(lecture)

        population.append(timetable)
    return population



def encode_timetable(timetable):
    chromosome = ''
    for lecture in timetable:
        course_index = courses.index(next((c for c in courses if c.name == lecture.course), None))
        theory_lab_index = 0 if lecture.theory_lab == 'Theory' else 1
        section_index = sections.index(next((s for s in sections if s.name == lecture.section), None))
        professor_index = professors.index(next((p for p in professors if p.name == lecture.professor), None))
        day_index = DAYS.index(lecture.day)
        timeslot_index = TIMESLOTS.index(lecture.timeslot)
        room_index = rooms.index(next((r for r in rooms if r.name == lecture.room), None))
        chromosome += f'{course_index:02b}{theory_lab_index:01b}{section_index:02b}{professor_index:02b}{day_index:03b}{timeslot_index:03b}{room_index:02b}'
    return chromosome

def decode_chromosome(chromosome):
    timetable = []
    for i in range(0, len(chromosome), 18):
        course_index = int(chromosome[i:i+2], 2)
        theory_lab_index = int(chromosome[i+2:i+3], 2)
        section_index = int(chromosome[i+3:i+5], 2)
        professor_index = int(chromosome[i+5:i+7], 2)
        day_index = int(chromosome[i+7:i+10], 2)
        timeslot_index = int(chromosome[i+10:i+13], 2)
        room_index = int(chromosome[i+13:i+15], 2)
        course = courses[course_index]
        theory_lab = 'Theory' if theory_lab_index == 0 else 'Lab'
        section = sections[section_index]
        professor = professors[professor_index]
        day = DAYS[day_index]
        timeslot = TIMESLOTS[timeslot_index]
        room = rooms[room_index]
        lecture = Lecture(course.name, theory_lab, section.name, professor.name, day, timeslot, room.name)
        timetable.append(lecture)
    return timetable


def fitness_function(timetable):
    conflicts = 0
    for i, lecture1 in enumerate(timetable):
        for j, lecture2 in enumerate(timetable):
            if i != j:
                # Check for conflicts based on day, timeslot, and room
                if set(lecture1.day) & set(lecture2.day) and set(lecture1.timeslot) & set(lecture2.timeslot) and lecture1.room == lecture2.room:
                    conflicts += 1

                # Check for conflicts based on professor, day, and timeslot
                if lecture1.professor == lecture2.professor and set(lecture1.day) & set(lecture2.day) and set(lecture1.timeslot) & set(lecture2.timeslot):
                    conflicts += 1

                # Check for conflicts based on section, day, and timeslot
                if lecture1.section == lecture2.section and set(lecture1.day) & set(lecture2.day) and set(lecture1.timeslot) & set(lecture2.timeslot):
                    conflicts += 1
                
    return -conflicts


def selection(population, scores, k=3):
    selected = [random.choice(population) for _ in range(k)]
    selected_scores = [scores[population.index(individual)] for individual in selected]
    return selected[selected_scores.index(max(selected_scores))]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(off1, off2, mutation_rate):
    for i in range(0,len(off1), 10):
        if random.random() < mutation_rate: # Mutate Course Swap
            if random.random() < mutation_rate: # Mutate Course Swap
                swap = off1[i].course
                off1[i].course = off2[i].course
                off2[i].course = swap
            if random.random() < mutation_rate: # Mutate Professor Swap
                swap = off1[i].professor
                off1[i].professor = off2[i].professor
                off2[i].professor = swap
            if random.random() < mutation_rate: # Mutate Room Swap
                swap = off1[i].room
                off1[i].room = off2[i].room
                off2[i].room = swap
            if random.random() < mutation_rate: # Mutate Day Swap
                swap = off1[i].day
                off1[i].day = off2[i].day
                off2[i].day = swap
            if random.random() < mutation_rate: # Mutate Timeslot Swap
                swap = off1[i].timeslot
                off1[i].timeslot = off2[i].timeslot
                off2[i].timeslot = swap
        
    return off1, off2
    


        
def evolve_population(population, mutation_rate):
    new_population = []
    scores = [fitness_function(timetable) for timetable in population]
    for _ in range(1000):
        parent1 = selection(population, scores)
        parent2 = selection(population, scores)
        offspring1, offspring2 = crossover(parent1, parent2)
        offspring1 , offspring2 = mutation(offspring1, offspring2, mutation_rate )
        new_population.append(offspring1)  # Fix: Use append instead of indexing
        new_population.append(offspring2)  # Fix: Use append instead of indexing
    return new_population


def run_genetic_algorithm(population_size, generations, mutation_rate):
    population = generate_initial_population(population_size, courses, professors, sections, rooms)
    for gen in range(generations):
        population = evolve_population(population, mutation_rate)
        best_timetable = max(population, key=lambda x: fitness_function(x))
        print(f"Generation {gen+1}, Best Fitness: {fitness_function(best_timetable)}")
        if fitness_function(best_timetable) == 0:
            break
        # print(best_timetable)
    return best_timetable


# Define courses
courses = [
    Course(name='Math101', lectures_per_week=2, is_lab=False),
    Course(name='Physics101', lectures_per_week=2, is_lab=False),
    Course(name='Chemistry101', lectures_per_week=2, is_lab=False),
    Course(name='Biology101', lectures_per_week=2, is_lab=False),
    Course(name='Lab101', lectures_per_week=1, is_lab=True),
    Course(name='Lab102', lectures_per_week=1, is_lab=True)
]

# Define professors
professors = [
    Professor(name='Prof. Smith'),
    Professor(name='Prof. Johnson'),
    Professor(name='Prof. Williams'),
    Professor(name='Prof. Brown'),
    Professor(name='Prof. Davis'),
    Professor(name='Prof. Miller'),
    Professor(name='Prof. Wilson'),
    Professor(name='Prof. Moore'),
    Professor(name='Prof. Taylor'),
    Professor(name='Prof. Anderson'),
    Professor(name='Prof. Thomas'),
    Professor(name='Prof. Jackson'),
    Professor(name='Prof. White'),
]

# Define sections
sections = [
    Section(name='A', strength=30),
    Section(name='B', strength=25),
    Section(name='C', strength=35),
    Section(name='D', strength=40),
    Section(name='E', strength=20),
    Section(name='F', strength=30),
]

# Define rooms
rooms = [
    Room(name='Room1', capacity=60),
    Room(name='Room2', capacity=60),
    Room(name='Room3', capacity=60),
    Room(name='Room4', capacity=60),
    Room(name='LargeHall1', capacity=120),
    Room(name='LargeHall2', capacity=120)
]

# Define other parameters
population_size = 100
generations = 50
mutation_rate = 0.05

def print_timetable(timetable):
    headers = ["Time"] + DAYS
    table = []
    for timeslot in TIMESLOTS:
        row = [timeslot]
        for day in DAYS:
            lectures = [lecture for lecture in timetable if day in lecture.day and timeslot in lecture.timeslot]
            if lectures:
                lecture_info = "\n".join([
                    f"{lecture.course.name if hasattr(lecture.course, 'name') else lecture.course} ({lecture.theory_lab})\n{lecture.section}\n{lecture.professor}\n{lecture.room}" 
                    for lecture in lectures
                ])
                row.append(lecture_info)
            else:
                row.append("")
        table.append(row)
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


if __name__ == "__main__":
    # Define courses, professors, sections, and rooms
    # Initialize other parameters (population_size, generations, mutation_rate)
    
    # Run genetic algorithm

    b = run_genetic_algorithm(population_size, generations, mutation_rate)
    print_timetable(b)

