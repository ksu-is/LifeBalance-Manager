import tkinter as tk
from tkinter import messagebox
import re

# ---------------- LOGIC FUNCTIONS ---------------- #

def create_empty_schedule():
    return {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

def get_end_time(work_str):
    """
    Attempts to find the end time in a string like '9am-5pm' or '17:00'.
    Defaults to 5:00 PM (17.0) if it can't parse it.
    """
    work_str = work_str.lower().replace(" ", "")
    # Look for the part after the hyphen
    match = re.search(r'-(\d+)(am|pm|:)?', work_str)
    if match:
        time_val = int(match.group(1))
        # Simple conversion to 24hr format
        if "pm" in work_str and time_val < 12:
            return time_val + 12
        return time_val
    return 17.0  # Default 5 PM

def format_time(decimal_hour):
    """Converts 17.5 to '5:30 PM'"""
    hour = int(decimal_hour)
    minutes = int((decimal_hour - hour) * 60)
    suffix = "PM" if hour >= 12 else "AM"
    display_hour = hour % 12
    if display_hour == 0: display_hour = 12
    return f"{display_hour}:{minutes:02d} {suffix}"

def generate_time_blocks(schedule, work_data, study_total, hobbies):
    days = list(schedule.keys())
    
    # 1. Distribute hour counts
    study_per_day = study_total / 7
    
    for i, day in enumerate(days):
        # Start time is either after work or 9 AM
        current_time = 9.0
        work_info = work_data.get(day, "")
        
        if work_info:
            schedule[day].append(f"WORK: {work_info}")
            current_time = get_end_time(work_info) + 0.5 # 30 min buffer after work
        
        # 2. Assign Study Block
        if study_per_day > 0:
            start_str = format_time(current_time)
            end_str = format_time(current_time + study_per_day)
            schedule[day].append(f"STUDY: {start_str} - {end_str}")
            current_time += study_per_day + 0.25 # 15 min break
            
        # 3. Assign Hobby Blocks
        for h_name, h_total in hobbies:
            h_per_day = h_total / 7
            if h_per_day > 0:
                start_str = format_time(current_time)
                end_str = format_time(current_time + h_per_day)
                schedule[day].append(f"{h_name}: {start_str} - {end_str}")
                current_time += h_per_day + 0.25

# ---------------- GUI APP ---------------- #

class LifeBalanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeBalance Manager")
        self.root.geometry("600x850")

        tk.Label(root, text="LifeBalance Manager", font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Work Section
        tk.Label(root, text="Work Hours (Format: 9am-5pm)", font=('Helvetica', 10, 'bold')).pack()
        self.work_entries = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            f = tk.Frame(root); f.pack(fill="x", padx=100)
            tk.Label(f, text=day, width=10).pack(side="left")
            e = tk.Entry(f); e.pack(side="right", expand=True, fill="x")
            self.work_entries[day] = e

        # Study Section
        tk.Label(root, text="\nTotal Weekly Study Hours", font=('Helvetica', 10, 'bold')).pack()
        self.study_entry = tk.Entry(root, width=10); self.study_entry.insert(0, "7"); self.study_entry.pack()

        # Hobbies Section
        tk.Label(root, text="\nHobbies (Format: Gym:7, Piano:3)", font=('Helvetica', 10, 'bold')).pack()
        self.hobby_entry = tk.Entry(root, width=40); self.hobby_entry.insert(0, "Gym:7"); self.hobby_entry.pack()

        tk.Button(root, text="GENERATE TIME SLOTS", bg="#2ECC71", fg="white", 
                  font=('Helvetica', 10, 'bold'), command=self.generate).pack(pady=20)

        self.output_text = tk.Text(root, height=20, width=70, font=('Consolas', 9))
        self.output_text.pack(padx=20, pady=10)

    def generate(self):
        try:
            schedule = create_empty_schedule()
            work_data = {d: e.get().strip() for d, e in self.work_entries.items() if e.get()}
            
            # Parse Study
            study_hrs = float(self.study_entry.get())
            
            # Parse Hobbies
            hobbies = []
            h_raw = self.hobby_entry.get().split(",")
            for item in h_raw:
                if ":" in item:
                    name, hrs = item.split(":")
                    hobbies.append((name.strip().upper(), float(hrs.strip())))

            generate_time_blocks(schedule, work_data, study_hrs, hobbies)

            self.output_text.delete("1.0", tk.END)
            for day, tasks in schedule.items():
                self.output_text.insert(tk.END, f"--- {day.upper()} ---\n")
                for t in tasks: self.output_text.insert(tk.END, f"  {t}\n")
                self.output_text.insert(tk.END, "\n")
                
        except Exception as e:
            messagebox.showerror("Error", "Check your inputs! Use numbers for hours.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LifeBalanceApp(root)
    root.mainloop()
