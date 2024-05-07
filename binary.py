
import random
import math

# Define the possible values for each attribute
attributes = {
    'Course': list(range(16)),
    'Theory/Lab': list(range(2)),
    'Section': list(range(4)),
    'Section-strength': list(range(4)),
    'Professor': list(range(32)),
    'First-lecture-day': list(range(5)),
    'First-lecture-timeslot': list(range(16)),
    'First-lecture-room': list(range(16)),
    'First-lecture-room-size': list(range(16)),
    'Second-lecture-day': list(range(5)),
    'Second-lecture-timeslot': list(range(16)),
    'Second-lecture-room': list(range(16)),
    'Second-lecture-room-size': list(range(16))
}

def InitializePopulation(population_size):
    population = []
    for _ in range(population_size):
        chromosome = convertToBinary()
        population.append(chromosome)
    return population


def convertToBinary():
    chromosome = ''
    for attribute, values in attributes.items():
        # Calculate the number of bits needed to represent the attribute
        num_bits = math.ceil(math.log2(len(values)))
        
        # Randomly select a value for the attribute
        index = random.choice(values)
        
        # Convert the index to a binary string and pad it with zeros to the required length
        binary_string = format(index, '0' + str(num_bits) + 'b')
        
        # Add the binary string to the chromosome
        chromosome += binary_string
    return chromosome

def convertToLecture(chromosome):
    num_bits = {attribute: math.ceil(math.log2(len(values))) for attribute, values in attributes.items()}
    chunks = []
    start = 0
    for attribute in attributes:
        end = start + num_bits[attribute]
        chunks.append(chromosome[start:end])
        start = end
    indices = {attribute: int(chunk, 2) for attribute, chunk in zip(attributes, chunks)}
    return indices

chromosome = convertToBinary()
print(chromosome)
indices = convertToLecture(chromosome)
print(indices)



