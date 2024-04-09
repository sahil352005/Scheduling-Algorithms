import tkinter as tk
from tkinter import ttk

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.priority = priority

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

def srt(processes):
    time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        remaining_processes.sort(key=lambda x: (x.remaining_time, x.arrival_time))
        shortest_process = remaining_processes[0]
        if shortest_process.arrival_time > time:
            time = shortest_process.arrival_time
        shortest_process.remaining_time -= 1
        time += 1
        if shortest_process.remaining_time == 0:
            remaining_processes.remove(shortest_process)
            shortest_process.waiting_time = time - shortest_process.burst_time - shortest_process.arrival_time

def priority(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.priority))
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
    try:
        processes = []
        for i in range(int(num_processes_entry.get())):
            pid = i + 1
            arrival_time = int(arrival_entries[i].get())
            burst_time = int(burst_entries[i].get())
            priority_value = int(priority_entries[i].get())
            processes.append(Process(pid, arrival_time, burst_time, priority_value))

        if scheduling_algorithm.get() == "FCFS":
            fcfs(processes)
        elif scheduling_algorithm.get() == "SJF":
            sjf(processes)
        elif scheduling_algorithm.get() == "SRTN":
            srt(processes)
        elif scheduling_algorithm.get() == "Priority":
            priority(processes)
        elif scheduling_algorithm.get() == "Round Robin":
            quantum = int(quantum_entry.get())
            if quantum <= 0:
                raise ValueError("Quantum must be a positive integer")
            round_robin(processes, quantum)

        print_results(processes)
    except ValueError as e:
        result_text.set(str(e))
    except Exception as e:
        result_text.set("An error occurred: " + str(e))

# GUI setup
root = tk.Tk()
root.title("Process Scheduling")
root.geometry("600x400")

style = ttk.Style()
style.configure("TFrame", background="#dde")
style.configure("TButton", background="#ccc")
style.configure("TLabel", background="#dde")

main_frame = ttk.Frame(root)
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Number of processes
num_processes_label = ttk.Label(main_frame, text="Number of Processes:")
num_processes_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
num_processes_entry = ttk.Entry(main_frame)
num_processes_entry.grid(row=0, column=1, padx=10, pady=5)

# Scheduling algorithm
algorithm_label = ttk.Label(main_frame, text="Scheduling Algorithm:")
algorithm_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
scheduling_algorithm = ttk.Combobox(main_frame, values=["FCFS", "SJF", "SRTN", "Priority", "Round Robin"])
scheduling_algorithm.grid(row=1, column=1, padx=10, pady=5)

# Quantum (for Round Robin)
quantum_label = ttk.Label(main_frame, text="Quantum (for Round Robin):")
quantum_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
quantum_entry = ttk.Entry(main_frame)
quantum_entry.grid(row=2, column=1, padx=10, pady=5)

# Process arrival, burst, and priority times
arrival_label = ttk.Label(main_frame, text="Arrival Time")
arrival_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
burst_label = ttk.Label(main_frame, text="Burst Time")
burst_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")
priority_label = ttk.Label(main_frame, text="Priority")
priority_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")

arrival_entries = []
burst_entries = []
priority_entries = []

def update_process_entries():
    for entry in arrival_entries + burst_entries + priority_entries:
        entry.grid_forget()

    arrival_entries.clear()
    burst_entries.clear()
    priority_entries.clear()

    for i in range(int(num_processes_entry.get())):
        arrival_entry = ttk.Entry(main_frame)
        arrival_entry.grid(row=i + 4, column=0, padx=10, pady=5)
        arrival_entries.append(arrival_entry)

        burst_entry = ttk.Entry(main_frame)
        burst_entry.grid(row=i + 4, column=1, padx=10, pady=5)
        burst_entries.append(burst_entry)

        priority_entry = ttk.Entry(main_frame)
        priority_entry.grid(row=i + 4, column=2, padx=10, pady=5)
        priority_entries.append(priority_entry)

num_processes_entry.bind("<FocusOut>", lambda _: update_process_entries())

# Submit button
submit_button = ttk.Button(main_frame, text="Submit", command=submit_processes)
submit_button.grid(row=0, column=3, rowspan=3, padx=10, pady=5, sticky="e")

# Result display
result_text = tk.StringVar()
result_text.set("")
result_label = ttk.Label(main_frame, textvariable=result_text, wraplength=300)
result_label.grid(row=4, column=3, rowspan=5, padx=10, pady=5)

root.mainloop()
