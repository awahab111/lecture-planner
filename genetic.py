import copy
import random
from datetime import datetime, timedelta
from models import *

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
ROOM_CAPACITY = {'class': 60, 'largehall': 120}
TIMESLOTS = ['8:30', '10:05', '11:40', '13:15', '14:50', '16:25']

courses = [
    Course(name='PDC', lectures_per_week=2, is_lab=False),
    Course(name='Software Engineering', lectures_per_week=2, is_lab=False),
    Course(name='Artificial Intelligence', lectures_per_week=2, is_lab=False),
    Course(name='Web Programming', lectures_per_week=2, is_lab=False),
    Course(name='Numerical Computing', lectures_per_week=2, is_lab=False),
    Course(name='AI LAB', lectures_per_week=1, is_lab=True),
]

# Define professors
professors = [
    Professor(name='Prof. Aadil Ur Rehman'),
    Professor(name='Prof. Usama Imtiaz'),
    Professor(name='Prof. Zille Huma'),
    Professor(name='Prof. Bilal Khalid'),
    Professor(name='Prof. Muhammad Ali'),
    Professor(name='Prof. Saad Salman'),
    Professor(name='Prof. Aqib Rehman'),
    Professor(name='Prof. Moore'),
    Professor(name='Prof. Taylor'),
    Professor(name='Prof. Anderson'),
    Professor(name='Prof. Thomas'),
    Professor(name='Prof. Johnson'),
]

# Define sections
sections = [
    Section(name='A', strength=30),
    Section(name='B', strength=25),
    Section(name='C', strength=35),
    Section(name='D', strength=40),
    Section(name='E', strength=20),
    Section(name='F', strength=74),
]

# Define rooms
rooms = [
    Room(name='301-C', capacity=60, floor=3),
    Room(name='302-C', capacity=60, floor=3),
    Room(name='304-C', capacity=60, floor=3),
    Room(name='305-C', capacity=60, floor=3),
    Room(name='102-D', capacity=120, floor=1),
    Room(name='101-D', capacity=120, floor=1)
]


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
                while len(professor.courses_taught) >= 3:
                    professor = random.choice(p)
                selected_professors[(course, sec)] = professor
                professor.courses_taught.append(course)
        
        for course in courses:
            for sec in sections:

                if course.is_lab:
                    theory_lab = 'Lab'
                    professor = selected_professors[(course, sec)]
                    room = random.choice(rooms)
                    day = [random.choice(DAYS)]
                    
                    available_timeslots = TIMESLOTS[:-1]
                    timeslot = random.choice(available_timeslots)
                    next_timeslot = random.choice(available_timeslots)

                    timeslots = [timeslot, next_timeslot]
                    
                    lecture = Lecture(course.name, theory_lab, sec, professor, day, timeslots, room)
                    timetable.append(lecture)

                else:
                    theory_lab = 'Theory'
                    professor = selected_professors[(course, sec)]
                    room = random.choice(rooms)

                    day = random.choice(DAYS)
                    day1 = random.choice(DAYS)
                    days = [day, day1]
                    timeslot = [random.choice(TIMESLOTS)]

                    lecture = Lecture(course.name, theory_lab, sec, professor, days, timeslot, room)
                    timetable.append(lecture)

        population.append(timetable)
    return population


# Fitness function implemented based on the hard contraints and soft constraints
def fitness_function(timetable):
    conflicts = 0
    softconflicts = 0
    for i, lecture1 in enumerate(timetable):
        for j, lecture2 in enumerate(timetable):
            if i != j:
                # conflicts based on day, timeslot, and room
                if set(lecture1.day) & set(lecture2.day) and set(lecture1.timeslot) & set(lecture2.timeslot) and lecture1.room == lecture2.room:
                    conflicts += 1

                # conflicts based on professor, day, and timeslot
                if lecture1.professor == lecture2.professor and set(lecture1.day) & set(lecture2.day) and set(lecture1.timeslot) & set(lecture2.timeslot):
                    conflicts += 1

                # conflicts based on section, day, and timeslot
                if lecture1.section == lecture2.section and set(lecture1.day) & set(lecture2.day) and set(lecture1.timeslot) & set(lecture2.timeslot):
                    conflicts += 1

        if lecture1.theory_lab == 'Lab':
            # Check if a lab is scheduled before 2:35
            lab_start_time = datetime.strptime(lecture1.timeslot[0], "%H:%M").time()
            preferred_time = datetime.strptime("14:35", "%H:%M").time()
            if lab_start_time < preferred_time:
                softconflicts += 1
            if TIMESLOTS.index(lecture1.timeslot[1]) != TIMESLOTS.index(lecture1.timeslot[0]) + 1:
                conflicts += 1

        if lecture1.theory_lab == 'Theory':
            if lecture1.day[1] != DAYS[(DAYS.index(lecture1.day[0]) + 2) % len(DAYS)] :
                conflicts += 1

        if lecture1.section.strength > 60 and lecture1.room.capacity == 60:
            conflicts += 1
        if lecture1.section.strength <= 60 and lecture1.room.capacity == 120:
            conflicts += 1


    return -(conflicts+softconflicts)

# Tournament selection 
def selection(population, scores, k=3):
    selected = [random.choice(population) for _ in range(k)]
    selected_scores = [scores[population.index(individual)] for individual in selected]
    return selected[selected_scores.index(max(selected_scores))]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Mutation function: Mutates the day and timeslot of a lecture based on if it is a theory or lab
def mutation(off1, mutation_rate):
    for i in range(0,len(off1), 1):

        if off1[i].theory_lab == 'Theory':
            if random.random() < mutation_rate:
                next_day = DAYS[(DAYS.index(off1[i].day[0]) + 2) % len(DAYS)]
                off1[i].day[1] = next_day
        if off1[i].theory_lab == 'Lab':
            if random.random() < mutation_rate:                
                next_timeslot_index = TIMESLOTS.index(off1[i].timeslot[0]) + 1
                next_timeslot = TIMESLOTS[next_timeslot_index]
                off1[i].timeslot[1] = next_timeslot

    return off1
    
        
def evolve_population(population, mutation_rate):
    new_population = []
    scores = [fitness_function(timetable) for timetable in population]
    for _ in range(1000): # Create 1000 new individuals from the initial population

        parent1 = selection(population, scores)
        parent2 = selection(population, scores)

        offspring1, offspring2 = crossover(parent1, parent2)
        offspring1  = mutation(offspring1, mutation_rate )
        
        # Add the new population into the 
        new_population.extend([offspring1, offspring2])
        
    return new_population


def run_genetic_algorithm(population_size, generations, mutation_rate):
    population = generate_initial_population(population_size, courses, professors, sections, rooms)
    for gen in range(generations):
        population = evolve_population(population, mutation_rate)
        best_timetable = max(population, key=lambda x: fitness_function(x))
        print(f"Generation {gen+1}, Best Fitness: {fitness_function(best_timetable)}")
        if fitness_function(best_timetable) > -3:
            break
    return best_timetable