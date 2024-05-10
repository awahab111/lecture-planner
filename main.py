import random
from lecture import Lecture
import math
import utils as util


professors = ['Prof. Smith', 'Prof. Johnson', 'Prof. Williams', 'Prof. Brown']
courses = ['Math101', 'Physics101', 'Chemistry101', 'Biology101']
theory_lab = ['Theory', 'Lab']
sections = util.randomSections(4)
print(sections)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
timeslots = ['8:30', '10:05', '11:40', '1:15', '2:50']
room = util.randomRooms(5)
lectures = []

for _ in range(10):  # Generate 10 random lectures
    course = random.choice(courses)
    t_l = random.choice(theory_lab)
    section = random.randint(0, len(sections)-1)
    section_strength = sections[section]
    professor = random.choice(professors)
    first_day = random.choice(days)
    first_timeslot = random.choice(timeslots)
    first_room = random.randint(0, len(room)-1)
    first_room_size = room[first_room]
    second_day = random.choice(days)
    second_timeslot = random.choice(timeslots)
    second_room = random.randint(0, len(room)-1)
    second_room_size = room[second_room]

    lecture = Lecture(course, t_l, section, section_strength, professor, 
                      first_day, first_timeslot, first_room, first_room_size, 
                      second_day, second_timeslot, second_room, second_room_size)
    
    lectures.append(lecture)


def toBinary(lecture):
    # Define the possible values for each attribute
    attributes = {
        'course': courses,
        'theory-lab': theory_lab,
        'section': [i for i in range(len(sections))],
        'professor': professors,
        'first-lecture-day': days,
        'first-lecture-timeslot': timeslots,
        'first-lecture-room': [i for i in range(len(room))],
        'second-lecture-day': days,
        'second-lecture-timeslot': timeslots,
        'second-lecture-room': [i for i in range(len(room))],
    }

    # Generate a binary string for each attribute
    chromosome = ''
    for attribute, values in attributes.items():
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


def fromBinary(chromosome):
    # Define the possible values for each attribute
    attributes = {
        'course': courses,
        'theory-lab': theory_lab,
        'section': [i for i in range(len(sections))],
        'professor': professors,
        'first-lecture-day': days,
        'first-lecture-timeslot': timeslots,
        'first-lecture-room': [i for i in range(len(room))],
        'second-lecture-day': days,
        'second-lecture-timeslot': timeslots,
        'second-lecture-room': [i for i in range(len(room))],
    }

    # Initialize the start index of the slice
    start = 0

    # Initialize a dictionary to hold the attribute values
    attribute_values = {}

    # For each attribute
    for attribute, values in attributes.items():
        # Calculate the number of bits for this attribute
        num_bits = math.ceil(math.log2(len(values)))

        # Slice the chromosome to get the binary string for this attribute
        binary_string = chromosome[start:start + num_bits]

        # Convert the binary string to an index
        index = int(binary_string, 2)

        # Check if the index is within the range of the list
        if index >= len(values):
            index = len(values) - 1

        # Get the value at this index
        value = values[index]

        # Add the value to the dictionary
        attribute_values[attribute.replace('-', '_')] = value

        # Update the start index for the next slice
        start += num_bits
    
    attribute_values['section_strength'] = sections[attribute_values['section']]
    attribute_values['first_lecture_room_size'] = room[attribute_values['first_lecture_room']]
    attribute_values['second_lecture_room_size'] = room[attribute_values['second_lecture_room']]

    # Create a new Lecture object with the attribute values
    lecture = Lecture(**attribute_values)

    return lecture

def crossover(parent1, parent2):
    # Convert the parents to binary strings
    chromosome1 = toBinary(parent1)
    chromosome2 = toBinary(parent2)

    # Choose a random crossover point
    crossover_point = random.randint(0, len(chromosome1) - 1)

    # Create the offspring by combining the parents' chromosomes
    offspring1_chromosome = chromosome1[:crossover_point] + chromosome2[crossover_point:]
    offspring2_chromosome = chromosome2[:crossover_point] + chromosome1[crossover_point:]

    # Convert the offspring chromosomes back to Lecture objects
    offspring1 = fromBinary(offspring1_chromosome)
    offspring2 = fromBinary(offspring2_chromosome)

    return offspring1, offspring2


def mutate(lecture, mutation_rate):
    # Convert the lecture to a binary string
    chromosome = toBinary(lecture)

    # Convert the mutation rate to a probability
    mutation_probability = mutation_rate / 100

    # Create a new chromosome by flipping each bit with a certain probability
    new_chromosome = ''
    for bit in chromosome:
        if random.random() < mutation_probability:
            new_bit = '0' if bit == '1' else '1'
        else:
            new_bit = bit
        new_chromosome += new_bit

    # Convert the new chromosome back to a Lecture object
    new_lecture = fromBinary(new_chromosome)

    return new_lecture

def fitness(lecture, all_lectures):
    conflicts = 0

    for other_lecture in all_lectures:
        if other_lecture == lecture:
            continue

        # # Check for professor conflicts
        # if lecture.professor == other_lecture.professor:
        #     if lecture.first_lecture_day == other_lecture.first_lecture_day and lecture.first_lecture_timeslot == other_lecture.first_lecture_timeslot:
        #         conflicts += 1
        #     if lecture.second_lecture_day == other_lecture.second_lecture_day and lecture.second_lecture_timeslot == other_lecture.second_lecture_timeslot:
        #         conflicts += 1

        # Check for room conflicts
        if lecture.first_lecture_room == other_lecture.first_lecture_room and lecture.first_lecture_day == other_lecture.first_lecture_day and lecture.first_lecture_timeslot == other_lecture.first_lecture_timeslot:
            conflicts += 1
        if lecture.second_lecture_room == other_lecture.second_lecture_room and lecture.second_lecture_day == other_lecture.second_lecture_day and lecture.second_lecture_timeslot == other_lecture.second_lecture_timeslot:
            conflicts += 1

        # # Check for section conflicts
        # if lecture.section == other_lecture.section:
        #     if lecture.first_lecture_day == other_lecture.first_lecture_day and lecture.first_lecture_timeslot == other_lecture.first_lecture_timeslot:
        #         conflicts += 1
        #     if lecture.second_lecture_day == other_lecture.second_lecture_day and lecture.second_lecture_timeslot == other_lecture.second_lecture_timeslot:
        #         conflicts += 1

    # The fitness is the number of non-conflicts
    return conflicts

def select(pop, scores, k=3):
    # First random selection
    selection_ix = random.randint(0, len(pop) - 1)
    for ix in random.sample(range(len(pop)), k - 1):
        # Check if better (e.g. perform a tournament)
        if scores[ix] > scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


def genetic_algorithm(lectures, n_iter, r_cross, r_mut):
    n_pop = len(lectures)

    # Enumerate generations
    for gen in range(n_iter):
        # Evaluate all candidates in the population
        scores = [fitness(c, lectures) for c in lectures]

        # Elitism: Keep the best individual from the current population
        best, best_eval = min(zip(lectures, scores), key=lambda x: x[1])
        new_population = [best]

        # Selection, crossover, and mutation to generate offspring
        while len(new_population) < n_pop:
            # Select parents
            p1 = select(lectures, scores, 3)
            p2 = select(lectures, scores, 3)

            # Crossover and mutation
            for c in crossover(p1, p2):
                # Mutation
                c = mutate(c, r_mut)
                
                # Store for next generation
                new_population.append(c)

        # Replace population
        lectures = new_population

        # print(f"Generation {gen+1}, Best Fitness: {best_eval}")
    # best.print()
    # print(scores)


    best_lecture, best_fitness = min(zip(lectures, scores), key=lambda x: x[1])
    print(scores)
    return [lectures, best_fitness]


util.printTable(lectures, timeslots)
# Run the genetic algorithm
best_lecture, best_fitness = genetic_algorithm(lectures, 10000, 0.9, 40)
# best_lecture.print()    
util.printTable(best_lecture, timeslots)

# print(best_fitness)
# print(best_lecture.print())

# for lecture in lectures:
#     if util.has_conflict(best_lecture, lecture):
#        lecture.print()

