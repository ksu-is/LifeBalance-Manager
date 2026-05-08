import tkinter as tk
from tkinter import messagebox

# ---------------- LOGIC FUNCTIONS ---------------- #

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
    # Use floor division to avoid float results
    per_day = study_hours // len(days)
    leftover = study_hours % len(days)
    
    for i, day in enumerate(days):
        daily_total = per_day + (1 if i < leftover else 0)
        if daily_total > 0:
            schedule[day].append(f"Study: {daily_total} hrs")

def add_hobbies(schedule, hobbies):
    days = list(schedule.keys())
    for i, (hobby, hours) in enumerate(hobbies):
        # Distribute hobbies across days using modulo
        target_day = days[i % len(days)]
        schedule[target_day].append(f"{hobby}: {hours} hrs")

def format_schedule(schedule):
    output = "--- YOUR WEEKLY SCHEDULE ---\n\n"
    for day, tasks in schedule.items():
        output += f"【 {day.upper()} 】\n"
        if not tasks:
            output += "  - No tasks scheduled\n"
        for task in tasks:
            output += f"  • {task}\n"
        output += "\n"
    return output

# ---------------- GUI APP ---------------- #

class LifeBalanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeBalance Manager Pro")
        self.root.geometry("500x700")

        # Work Schedule Section
        tk.Label(root, text="Work Schedule", font=('Helvetica', 10, 'bold')).pack(pady=(10, 0))
        tk.Label(root, text="(e.g., 9am-5pm or Shift A)", font=('Helvetica', 8, 'italic')).pack()
        
        self.work_entries = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day in days:
            frame = tk.Frame(root)
            frame.pack(fill="x", padx=50)
            tk.Label(frame, text=day, width=10, anchor="w").pack(side="left")
            entry = tk.Entry(frame)
            entry.pack(side="right", expand=True, fill="x")
            self.work_entries[day] = entry

        # Study Hours Section
        tk.Label(root, text="\nTotal Weekly Study Hours", font=('Helvetica', 10, 'bold')).pack()
        self.study_entry = tk.Entry(root, width=10)
        self.study_entry.insert(0, "0")  # Default value to prevent crash
        self.study_entry.pack()

        # Hobbies Section
        tk.Label(root, text="\nHobbies", font=('Helvetica', 10, 'bold')).pack()
        tk.Label(root, text="Format: Gym:2, Reading:1 (comma separated)", font=('Helvetica', 8, 'italic')).pack()
        self.hobby_entry = tk.Entry(root, width=50)
        self.hobby_entry.pack(pady=5)

        # Generate Button
        tk.Button(root, text="Generate Schedule", bg="#4CAF50", fg="white", 
                  font=('Helvetica', 10, 'bold'), command=self.generate_schedule).pack(pady=20)

        # Output Display
        self.output_text = tk.Text(root, height=15, width=55, font=('Consolas', 10))
        self.output_text.pack(padx=20, pady=10)

    def generate_schedule(self):
        try:
            # 1. Parse Work
            work_schedule = {day: entry.get().strip() for day, entry in self.work_entries.items() if entry.get().strip()}

            # 2. Parse Study (With error handling)
            study_input = self.study_entry.get().strip()
            study_hours = int(study_input) if study_input.isdigit() else 0

            # 3. Parse Hobbies (With safe splitting)
            hobbies = []
            hobby_input = self.hobby_entry.get().strip()
            if hobby_input:
                items = hobby_input.split(",")
                for item in items:
                    if ":" in item:
                        name, hours = item.split(":")
                        if hours.strip().isdigit():
                            hobbies.append((name.strip(), int(hours.strip())))
            
            # 4. Build and Display
            schedule = create_empty_schedule()
            add_work_to_schedule(schedule, work_schedule)
            add_study_time(schedule, study_hours)
            add_hobbies(schedule, hobbies)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, format_schedule(schedule))

        except Exception as e:
            messagebox.showerror("Oops!", f"Something went wrong: {e}\nCheck your hobby formatting!")

# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    root = tk.Tk()
    app = LifeBalanceApp(root)
    root.mainloop()
