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

def sjf(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    calculate_waiting_time(processes)

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

def submit_processes():
    processes = []
    for i in range(int(num_processes_entry.get())):
        pid = i + 1
        arrival_time = int(arrival_entries[i].get())
        burst_time = int(burst_entries[i].get())
        processes.append(Process(pid, arrival_time, burst_time))

    if scheduling_algorithm.get() == "FCFS":
        fcfs(processes)
    elif scheduling_algorithm.get() == "SJF":
        sjf(processes)
    elif scheduling_algorithm.get() == "Round Robin":
        quantum = int(quantum_entry.get())
        round_robin(processes, quantum)

    print_results(processes)

# GUI setup
root = tk.Tk()
root.title("Process Scheduling")

# Number of processes
num_processes_label = tk.Label(root, text="Number of Processes:")
num_processes_label.grid(row=0, column=0)
num_processes_entry = tk.Entry(root)
num_processes_entry.grid(row=0, column=1)

# Scheduling algorithm
algorithm_label = tk.Label(root, text="Scheduling Algorithm:")
algorithm_label.grid(row=1, column=0)
scheduling_algorithm = ttk.Combobox(root, values=["FCFS", "SJF", "Round Robin"])
scheduling_algorithm.grid(row=1, column=1)

# Quantum (for Round Robin)
quantum_label = tk.Label(root, text="Quantum (for Round Robin):")
quantum_label.grid(row=2, column=0)
quantum_entry = tk.Entry(root)
quantum_entry.grid(row=2, column=1)

# Process arrival and burst times
arrival_label = tk.Label(root, text="Arrival Time")
arrival_label.grid(row=3, column=0)
burst_label = tk.Label(root, text="Burst Time")
burst_label.grid(row=3, column=1)

arrival_entries = []
burst_entries = []

def update_process_entries():
    for entry in arrival_entries + burst_entries:
        entry.grid_forget()

    arrival_entries.clear()
    burst_entries.clear()

    for i in range(int(num_processes_entry.get())):
        arrival_entry = tk.Entry(root)
        arrival_entry.grid(row=i + 4, column=0)
        arrival_entries.append(arrival_entry)

        burst_entry = tk.Entry(root)
        burst_entry.grid(row=i + 4, column=1)
        burst_entries.append(burst_entry)

num_processes_entry.bind("<FocusOut>", lambda _: update_process_entries())

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_processes)
submit_button.grid(row=0, column=2, rowspan=3)

# Result display
result_text = tk.StringVar()
result_text.set("")
result_label = tk.Label(root, textvariable=result_text)
result_label.grid(row=4, column=2, rowspan=5)

root.mainloop()
