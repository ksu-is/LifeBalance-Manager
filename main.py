import tkinter as tk
from tkinter import messagebox
import re
import math

# ---------------- LOGIC FUNCTIONS ---------------- #

def create_empty_schedule():
    return {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

def get_end_time(work_str):
    """Parses work string to find end time decimal. Defaults to 17.0."""
    work_str = work_str.lower().replace(" ", "")
    # Matches patterns like -5, -5:30, -17:00 with optional am/pm
    match = re.search(r'-(\d+)(:(\d+))?(am|pm)?', work_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(3)) if match.group(3) else 0
        
        decimal_time = hours + (minutes / 60)
        if "pm" in work_str and hours < 12:
            decimal_time += 12
        elif "am" in work_str and hours == 12:
            decimal_time = 0
            
        return decimal_time
    return 17.0 

def format_time(decimal_hour):
    """Converts 14.5 to '2:30 PM'"""
    hour = int(decimal_hour)
    minutes = int(round((decimal_hour - hour) * 60))
    if minutes >= 60: 
        hour += 1
        minutes = 0
    suffix = "PM" if hour >= 12 else "AM"
    display_hour = hour % 12
    if display_hour == 0: display_hour = 12
    return f"{display_hour}:{minutes:02d} {suffix}"

def generate_time_blocks(schedule, work_data, study_total, hobbies):
    days = list(schedule.keys())
    
    # Calculate daily needs (rounded to nearest 0.5)
    study_per_day = round((study_total / 7) * 2) / 2
    
    for day in days:
        current_time = 9.0 # Default start if no work
        work_info = work_data.get(day, "")
        
        if work_info:
            schedule[day].append(f"WORK: {work_info}")
            # Start activities 30 mins after work, snapped to next half-hour
            raw_end = get_end_time(work_info) + 0.5
            current_time = math.ceil(raw_end * 2) / 2 
        
        # Assign Study Block
        if study_per_day > 0:
            start_str = format_time(current_time)
            end_time = current_time + study_per_day
            schedule[day].append(f"STUDY: {start_str} - {format_time(end_time)}")
            current_time = end_time
            
        # Assign Hobby Blocks
        for h_name, h_total in hobbies:
            h_per_day = round((h_total / 7) * 2) / 2
            if h_per_day > 0:
                # Ensure we start on a clean half-hour
                current_time = math.ceil(current_time * 2) / 2
                start_str = format_time(current_time)
                end_time = current_time + h_per_day
                schedule[day].append(f"{h_name}: {start_str} - {format_time(end_time)}")
                current_time = end_time

# ---------------- GUI APP ---------------- #

class LifeBalanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeBalance Manager")
        self.root.geometry("600x900")
        self.root.configure(bg="#F8F9FA")

        tk.Label(root, text="LifeBalance Manager", font=('Segoe UI', 18, 'bold'), bg="#F8F9FA", fg="#2C3E50").pack(pady=15)

        # --- WORK SECTION ---
        tk.Label(root, text="Work Hours", font=('Segoe UI', 10, 'bold'), bg="#F8F9FA").pack()
        tk.Label(root, text="For Example: 9am-5pm or 8:30-4:30pm", font=('Segoe UI', 8, 'italic'), bg="#F8F9FA", fg="#6C757D").pack()
        
        self.work_entries = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            f = tk.Frame(root, bg="#F8F9FA")
            f.pack(fill="x", padx=100, pady=2)
            tk.Label(f, text=day, width=10, anchor="w", bg="#F8F9FA").pack(side="left")
            e = tk.Entry(f, highlightthickness=1)
            e.pack(side="right", expand=True, fill="x")
            self.work_entries[day] = e

        # --- STUDY SECTION ---
        tk.Label(root, text="\nTotal Weekly Study Hours", font=('Segoe UI', 10, 'bold'), bg="#F8F9FA").pack()
        tk.Label(root, text="For Example: 10 or 14", font=('Segoe UI', 8, 'italic'), bg="#F8F9FA", fg="#6C757D").pack()
        self.study_entry = tk.Entry(root, width=10, justify='center')
        self.study_entry.insert(0, "7")
        self.study_entry.pack()

        # --- HOBBY SECTION ---
        tk.Label(root, text="\nWeekly Hobbies", font=('Segoe UI', 10, 'bold'), bg="#F8F9FA").pack()
        tk.Label(root, text="For Example: Gym:7, Reading:3.5", font=('Segoe UI', 8, 'italic'), bg="#F8F9FA", fg="#6C757D").pack()
        self.hobby_entry = tk.Entry(root, width=45, justify='center')
        self.hobby_entry.insert(0, "Gym:7, Piano:3.5")
        self.hobby_entry.pack(pady=5)

        # --- GENERATE ---
        tk.Button(root, text="GENERATE SCHEDULE", bg="#007BFF", fg="white", 
                  font=('Segoe UI', 10, 'bold'), height=2, width=30, relief="flat", command=self.generate).pack(pady=20)

        # --- OUTPUT ---
        self.output_text = tk.Text(root, height=20, width=70, font=('Consolas', 10), bg="white", relief="solid", borderwidth=1)
        self.output_text.pack(padx=20, pady=10)

    def generate(self):
        try:
            schedule = create_empty_schedule()
            work_data = {d: e.get().strip() for d, e in self.work_entries.items() if e.get()}
            
            study_input = self.study_entry.get().strip()
            study_hrs = float(study_input) if study_input else 0
            
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
                if not tasks: 
                    self.output_text.insert(tk.END, "  No tasks assigned today.\n")
                for t in tasks: 
                    self.output_text.insert(tk.END, f"  {t}\n")
                self.output_text.insert(tk.END, "\n" + "━"*45 + "\n")
                
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure Study and Hobby hours are numbers.\nFor Example: Use 5 instead of 'five'.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LifeBalanceApp(root)
    root.mainloop()
