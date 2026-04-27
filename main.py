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
