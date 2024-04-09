import tkinter as tk
from tkinter import ttk

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0

def calculate_waiting_time(processes):
    total_time = 0
    for process in processes:
        total_time += process.burst_time
        process.turnaround_time = total_time
        process.waiting_time = total_time - process.burst_time - process.arrival_time

def fcfs(processes):
    processes.sort(key=lambda x: x.arrival_time)
    calculate_waiting_time(processes)

def sjf_non_preemptive(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    calculate_waiting_time(processes)

def sjf_preemptive(processes):
    pass  # Implement SJF preemptive algorithm

def round_robin(processes, quantum):
    time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        for process in remaining_processes:
            if process.remaining_time > 0:
                if process.remaining_time > quantum:
                    time += quantum
                    process.remaining_time -= quantum
                else:
                    time += process.remaining_time
                    process.waiting_time = time - process.burst_time - process.arrival_time
                    process.remaining_time = 0
        remaining_processes = [p for p in remaining_processes if p.remaining_time > 0]

def priority_non_preemptive(processes):
    processes.sort(key=lambda x: x.arrival_time)
    processes.sort(key=lambda x: x.priority)
    calculate_waiting_time(processes)

def priority_preemptive(processes):
    time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        remaining_processes.sort(key=lambda x: x.priority)
        for process in remaining_processes:
            if process.remaining_time > 0:
                if process.remaining_time > 1:
                    time += 1
                    process.remaining_time -= 1
                else:
                    time += process.remaining_time
                    process.waiting_time = time - process.burst_time - process.arrival_time
                    process.remaining_time = 0
        remaining_processes = [p for p in remaining_processes if p.remaining_time > 0]

def print_results(processes):
    total_waiting_time = sum(process.waiting_time for process in processes)
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)

    output_text = "Process\tWaiting Time\tTurnaround Time\n"
    for process in processes:
        output_text += f"{process.pid}\t{process.waiting_time}\t\t{process.turnaround_time}\n"
    output_text += f"\nAverage Waiting Time: {avg_waiting_time}\n"
    output_text += f"Average Turnaround Time: {avg_turnaround_time}\n"

    result_text.set(output_text)

def update_process_entries(event=None):
    for entry in arrival_entries + burst_entries:
        entry.grid_forget()

    arrival_entries.clear()
    burst_entries.clear()

    num_processes = num_processes_entry.get()
    if num_processes.isdigit():
        num_processes = int(num_processes)
        for i in range(num_processes):
            arrival_entry = ttk.Entry(input_frame)
            arrival_entry.grid(row=i + 5, column=0, padx=5, pady=5)
            arrival_entries.append(arrival_entry)
            
            burst_entry = ttk.Entry(input_frame)
            burst_entry.grid(row=i + 5, column=1, padx=5, pady=5)
            burst_entries.append(burst_entry)

def run_scheduler(event=None):
    num_processes = num_processes_entry.get()
    if not num_processes.isdigit() or int(num_processes) <= 0:
        result_text.set("Error: Number of processes must be a positive integer.")
        return
    
def add_process_entry_fields():
    # Add entry fields for one more process
    arrival_entry = ttk.Entry(input_frame)
    arrival_entry.grid(row=len(arrival_entries) + 5, column=0, padx=5, pady=5)
    arrival_entries.append(arrival_entry)
    
    burst_entry = ttk.Entry(input_frame)
    burst_entry.grid(row=len(burst_entries) + 5, column=1, padx=5, pady=5)
    burst_entries.append(burst_entry)

def remove_process_entry_fields():
    # Remove entry fields for the last process
    if len(arrival_entries) > 0:
        arrival_entries[-1].destroy()
        arrival_entries.pop()
    if len(burst_entries) > 0:
        burst_entries[-1].destroy()
        burst_entries.pop()

    processes = []
    for i in range(int(num_processes)):
        arrival_time = arrival_entries[i].get()
        burst_time = burst_entries[i].get()

        if not arrival_time.isdigit() or not burst_time.isdigit():
            result_text.set("Error: Arrival time and burst time must be positive integers.")
            return

        if int(arrival_time) < 0 or int(burst_time) <= 0:
            result_text.set("Error: Arrival time must be non-negative and burst time must be positive.")
            return

        processes.append(Process(i + 1, int(arrival_time), int(burst_time)))

    if scheduling_algorithm.get() == "":
        result_text.set("Error: Please select a scheduling algorithm.")
        return

    if scheduling_algorithm.get() == "Round Robin":
        quantum = quantum_entry.get()
        if not quantum.isdigit() or int(quantum) <= 0:
            result_text.set("Error: Quantum must be a positive integer for Round Robin.")
            return

    if scheduling_algorithm.get() == "FCFS":
        fcfs(processes)
    elif scheduling_algorithm.get() == "SJF (Non-preemptive)":
        sjf_non_preemptive(processes)
    elif scheduling_algorithm.get() == "SJF (Preemptive)":
        sjf_preemptive(processes)
    elif scheduling_algorithm.get() == "Round Robin":
        round_robin(processes, int(quantum))
    elif scheduling_algorithm.get() == "Priority (Non-preemptive)":
        priority_non_preemptive(processes)
    elif scheduling_algorithm.get() == "Priority (Preemptive)":
        priority_preemptive(processes)

    print_results(processes)



# GUI setup
root = tk.Tk()
root.title("Process Scheduling")
root.resizable(True, True)

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))

input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10)

result_frame = tk.Frame(root)
result_frame.grid(row=0, column=1, padx=10, pady=10)

# Add tooltips or instructions for input fields
num_processes_label = ttk.Label(input_frame, text="Number of Processes:", anchor="w")
num_processes_label.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="w")
num_processes_entry = ttk.Entry(input_frame)
num_processes_entry.grid(row=0, column=1, padx=5, pady=(10, 5), sticky="ew")
num_processes_tooltip = ttk.Label(input_frame, text="(Enter a positive integer)", foreground="gray")
num_processes_tooltip.grid(row=0, column=2, padx=(0, 5), pady=(10, 5), sticky="w")

algorithm_label = ttk.Label(input_frame, text="Scheduling Algorithm:", anchor="w")
algorithm_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
scheduling_algorithm = ttk.Combobox(input_frame, values=["FCFS", "SJF (Non-preemptive)", "SJF (Preemptive)", "Round Robin", "Priority (Non-preemptive)", "Priority (Preemptive)"])
scheduling_algorithm.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
algorithm_tooltip = ttk.Label(input_frame, text="(Select a scheduling algorithm)", foreground="gray")
algorithm_tooltip.grid(row=1, column=2, padx=(0, 5), pady=5, sticky="w")

quantum_label = ttk.Label(input_frame, text="Quantum (for Round Robin):", anchor="w")
quantum_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
quantum_entry = ttk.Entry(input_frame)
quantum_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
quantum_tooltip = ttk.Label(input_frame, text="(Enter a positive integer)", foreground="gray")
quantum_tooltip.grid(row=2, column=2, padx=(0, 5), pady=5, sticky="w")

process_info_label = ttk.Label(input_frame, text="Process Information", anchor="w")
process_info_label.grid(row=3, column=0, columnspan=2, pady=(10, 5), sticky="w")

arrival_label = ttk.Label(input_frame, text="Arrival Time", anchor="center")
arrival_label.grid(row=4, column=0, padx=5, pady=5)
burst_label = ttk.Label(input_frame, text="Burst Time", anchor="center")
burst_label.grid(row=4, column=1, padx=5, pady=5)

# Add tooltips for the input fields in the process information section
arrival_tooltip = ttk.Label(input_frame, text="(Enter positive integers)", foreground="gray")
arrival_tooltip.grid(row=4, column=2, padx=(0, 5), pady=5, sticky="w")
burst_tooltip = ttk.Label(input_frame, text="(Enter positive integers)", foreground="gray")
burst_tooltip.grid(row=4, column=3, padx=5, pady=5, sticky="w")

# Add dynamic entry field buttons
add_button = ttk.Button(input_frame, text="Add Process", command=add_process_entry_fields)
add_button.grid(row=3, column=2, padx=5, pady=(10, 5), sticky="ew")
remove_button = ttk.Button(input_frame, text="Remove Process", command=remove_process_entry_fields)
remove_button.grid(row=3, column=3, padx=5, pady=(10, 5), sticky="ew")



arrival_entries = []
burst_entries = []

for i in range(5):  # Initially show 5 entry rows
    arrival_entry = ttk.Entry(input_frame)
    arrival_entry.grid(row=i + 5, column=0, padx=5, pady=5)
    arrival_entries.append(arrival_entry)

    burst_entry = ttk.Entry(input_frame)
    burst_entry.grid(row=i + 5, column=1, padx=5, pady=5)
    burst_entries.append(burst_entry)

submit_button = ttk.Button(input_frame, text="Run Scheduler", command=run_scheduler)
submit_button.grid(row=0, column=2, rowspan=6, padx=10, pady=10)
root.bind("<Return>", run_scheduler)

result_text = tk.StringVar()
result_text.set("")
result_label = ttk.Label(result_frame, textvariable=result_text, anchor="w", justify="left")
result_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

root.mainloop()