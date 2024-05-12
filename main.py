from tabulate import tabulate
from datetime import datetime, timedelta
from models import * 
import genetic

def print_timetable(timetable):
    headers = ["Time"] + genetic.DAYS
    table = []
    for timeslot in genetic.TIMESLOTS:
        start = datetime.strptime(timeslot, "%H:%M")
        end = start + timedelta(minutes=80)
        row = [f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"]
        for day in genetic.DAYS:
            lectures = [lecture for lecture in timetable if day in lecture.day and timeslot in lecture.timeslot]
            if lectures:
                lecture_info = "\n".join([
                    f"{lecture.course.name if hasattr(lecture.course, 'name') else lecture.course} ({lecture.theory_lab})\n{lecture.section.name}\n{lecture.professor.name}\n{lecture.room.name}\n" 
                    for lecture in lectures
                ])
                row.append(lecture_info)
            else:
                row.append("")
        table.append(row)
    
    # Write the timetable to a file
    with open('timetable.txt', 'w', encoding='utf-8') as file:
        file.write(tabulate(table, headers=headers, tablefmt="fancy_grid"))


if __name__ == "__main__":
    
    # defining algorithm parameters
    population_size = 1000
    generations = 50
    mutation_rate = 0.45
    b = genetic.run_genetic_algorithm(population_size, generations, mutation_rate)
    # Write the timetable to a file
    print_timetable(b)

