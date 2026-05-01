import tkinter as tk
from tkinter import messagebox


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

def format_schedule(schedule):
    output = ""
    for day, tasks in schedule.items():
        output += f"{day}:\n"
        for task in tasks:
            output += f"  - {task}\n"
        output += "\n"
    return output


class LifeBalanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeBalance Manager")

        # Work Schedule
        tk.Label(root, text="Work Schedule (e.g. Monday: 9-5)").pack()
        self.work_entries = {}

        for day in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
            frame = tk.Frame(root)
            frame.pack()
            tk.Label(frame, text=day, width=10).pack(side="left")
            entry = tk.Entry(frame)
            entry.pack(side="left")
            self.work_entries[day] = entry

        # Study Hours
        tk.Label(root, text="Total Study Hours (week)").pack()
        self.study_entry = tk.Entry(root)
        self.study_entry.pack()

        # Hobbies
        tk.Label(root, text="Hobbies (format: hobby:hours, comma separated)").pack()
        self.hobby_entry = tk.Entry(root, width=40)
        self.hobby_entry.pack()

        # Generate Button
        tk.Button(root, text="Generate Schedule", command=self.generate_schedule).pack(pady=10)

        # Output
        self.output_text = tk.Text(root, height=15, width=50)
        self.output_text.pack()

    def generate_schedule(self):
        try:
            # Work
            work_schedule = {}
            for day, entry in self.work_entries.items():
                value = entry.get().strip()
                if value:
                    work_schedule[day] = value

            # Study
            study_hours = int(self.study_entry.get())

            # Hobbies
            hobbies = []
            hobby_input = self.hobby_entry.get()
            if hobby_input:
                items = hobby_input.split(",")
                for item in items:
                    name, hours = item.split(":")
                    hobbies.append((name.strip(), int(hours.strip())))

            # Build schedule
            schedule = create_empty_schedule()
            add_work_to_schedule(schedule, work_schedule)
            add_study_time(schedule, study_hours)
            add_hobbies(schedule, hobbies)

            # Display
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, format_schedule(schedule))

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LifeBalanceApp(root)
    root.mainloop()
