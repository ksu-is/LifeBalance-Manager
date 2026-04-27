# LifeBalance Manager
# Main entry point of the program

def main():
    print("Welcome to LifeBalance Manager")

if __name__ == "__main__":
    main()
    
def get_work_schedule():
    work_schedule = {}
    while True:
        day = input("Enter a work day (or type 'done'): ")
        if day.lower() == "done":
            break
        hours = input(f"Enter work hours for {day} (e.g., 9-5): ")
        work_schedule[day] = hours
    return work_schedule
    
def get_study_time():
    hours = int(input("Enter total study hours for the week: "))
    return hours
    
def get_hobbies():
    hobbies = []
    while True:
        hobby = input("Enter a hobby (or type 'done'): ")
        if hobby.lower() == "done":
            break
        hours = int(input(f"How many hours for {hobby}? "))
        hobbies.append((hobby, hours))
    return hobbies

def create_empty_schedule():
    return {
        "Monday": [], "Tuesday": [], "Wednesday": [], 
        "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []
    }

def add_work_to_schedule(schedule, work_schedule):
    for day, hours in work_schedule.items():
        if day in schedule:
            schedule[day].append(f"Work: {hours}")

def add_study_time(schedule, study_hours):
    days = list(schedule.keys())
    per_day = study_hours // len(days)
    for day in days:
        if per_day > 0:
            schedule[day].append(f"Study: {per_day} hrs")

def add_hobbies(schedule, hobbies):
    days = list(schedule.keys())
    day_index = 0
    for hobby, hours in hobbies:
        schedule[days[day_index]].append(f"{hobby}: {hours} hrs")
        day_index = (day_index + 1) % len(days)

def display_schedule(schedule):
    print("\nWeekly Schedule:\n")
    for day, tasks in schedule.items():
        print(day)
        for task in tasks:
            print(" -", task)
        print()
