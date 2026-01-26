🖥️ Context Switching Analyzer
A terminal-based Operating System Kernel Simulation that demonstrates CPU Scheduling and Context Switching using the Round Robin (RR) algorithm.
This project visualizes how an OS kernel manages multiple processes, allocates CPU time fairly, and handles context-switching overhead.
📌 Project Overview
The Context Switching Analyzer simulates core kernel responsibilities, focusing on how processes move between the Ready Queue and the CPU Core.
It provides a clear visualization of:
Process arrival and execution
PCB (Process Control Block) allocation
Context switching events
CPU scheduling using fixed time quantums
Final performance statistics and system uptime
The simulation is designed for educational purposes to help understand OS internals in a practical way.
🎯 Objectives
Demonstrate the working of the Round Robin CPU Scheduling Algorithm
Visualize process state transitions
Understand context switching overhead
Track real-time kernel metrics such as:
System uptime
Switch count
Process execution order
⚙️ Features
⏱️ Fixed Quantum Time (07 seconds)
🔁 Preemptive Round Robin Scheduling
📋 Process Control Block (PCB) management
📊 Context Switching Analyzer
🧾 Final Kernel Audit Report
🖥️ Terminal-based UI (Linux/Unix style)
🧪 Simulated Processes
The kernel manages the following processes with different arrival times:
PROC_ALPHA
PROC_BETA
PROC_GAMMA
PROC_DELTA
PROC_SIGMA
Each process is scheduled fairly to avoid starvation.
🛠️ Tools & Technologies
Programming Language: Python
Interface: Terminal-based UI
Operating System: Linux / Unix
Concepts Used:
Round Robin Scheduling
Process Control Blocks (PCB)
Context Switching
Ready Queue Management
🧠 System Design / Methodology
Kernel initializes and allocates PCB blocks
Processes arrive and enter the Ready Queue
CPU executes a process for one quantum
Context Switch occurs:
Current process state is saved
Next process is loaded into CPU
Simulation continues until all processes complete
Kernel generates final execution statistics
📈 Results
Total System Uptime: 220 seconds
Processes Managed: 5
Multiple Context Switches Successfully Handled
No process starvation occurred
📚 References
Books
Operating System Concepts — Silberschatz, Galvin, Gagne
Modern Operating Systems — Andrew S. Tanenbaum
Web Resources
GeeksforGeeks – OS Process Management & PCB
TutorialsPoint – CPU Scheduling Algorithms
