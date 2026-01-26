import curses
import time
import random

class Process:
    def __init__(self, pid, name, total_instr, arrival_time):
        self.pid = pid
        self.name = name
        self.total_instr = total_instr
        self.arrival_time = arrival_time
        self.pc = 0
        self.registers = {"R1": 0, "R2": 0, "R3": 0}
        self.is_arrived = False
        self.start_exec_time = None
        self.completion_time = None

def draw_custom_box(stdscr, y, x, h, w, title, color_pair):
    stdscr.attron(curses.color_pair(color_pair))
    stdscr.addstr(y, x, "┏" + "━" * (w-1) + "┓")
    for i in range(1, h):
        stdscr.addstr(y + i, x, "┃")
        stdscr.addstr(y + i, x + w, "┃")
    stdscr.addstr(y + h, x, "┗" + "━" * (w-1) + "┛")
    stdscr.addstr(y, x + 2, f" {title} ", curses.A_BOLD)
    stdscr.attroff(curses.color_pair(color_pair))

def show_welcome_screen(stdscr):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
   
    # Text list
    lines = [
        "➲ INITIALIZING SYSTEM KERNEL...",
        "➲ LOADING ROUND ROBIN SCHEDULER...",
        "➲ ALLOCATING PCB BLOCKS...",
        "➲ KERNEL STATUS: READY"
    ]
   
    # Ek hi baar screen clear karke saari lines ko fixed position par dikhana
    for i in range(len(lines)):
        # y-coordinate fixed hai (h//2 - 2 + i), is se text uper niche nahi hoga
        for j in range(i + 1):
            stdscr.addstr(h//2 - 2 + j, (w - len(lines[j]))//2, lines[j], curses.color_pair(2) | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.8)
   
    stdscr.addstr(h//2 + 4, (w - 25)//2, "[ PRESS ANY KEY TO START ]", curses.A_BLINK | curses.color_pair(3))
    stdscr.refresh()
    stdscr.getch()
   
    # Stable Pre-run Detection
    stdscr.clear()
    msg1 = "⚡ DETECTING INITIAL PROCESSES..."
    msg2 = "✔ ALPHA, BETA, GAMMA DETECTED IN READY QUEUE"
    stdscr.addstr(h//2 - 1, (w - len(msg1))//2, msg1, curses.color_pair(1))
    stdscr.refresh()
    time.sleep(1.2)
    stdscr.addstr(h//2 + 1, (w - len(msg2))//2, msg2, curses.color_pair(1))
    stdscr.refresh()
    time.sleep(1.5)

def run_simulation(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)  
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)    

    show_welcome_screen(stdscr)
    start_sim_time = time.time()
   
    time_quantum = 11
    procs = [
        Process(101, "PROC_ALPHA", 40, 0),
        Process(102, "PROC_BETA ", 38, 0),
        Process(103, "PROC_GAMMA", 42, 0),
        Process(104, "PROC_DELTA", 35, 20),
        Process(105, "PROC_SIGMA", 35, 40)
    ]
   
    current_idx = 0
    logs = ["Kernel Online.", "Uptime Clock Started."]
    total_switches = 0
    last_p_name = "ROOT"

    with open("history_log.txt", "w") as f:
        f.write("--- KERNEL AUDIT REPORT ---\n\n")

        while any(p.pc < p.total_instr for p in procs):
            elapsed = time.time() - start_sim_time
           
            for p in procs:
                if not p.is_arrived and elapsed >= p.arrival_time:
                    p.is_arrived = True
                    h_y, w_x = stdscr.getmaxyx()
                    # Popup position fix
                    stdscr.addstr(h_y//2, (w_x-35)//2, f" 🔔 {p.name} HAS ARRIVED! ", curses.A_REVERSE | curses.color_pair(3))
                    stdscr.refresh()
                    time.sleep(1.0)
                    msg = f"T+{int(elapsed)}s: [ARR] {p.name}"
                    logs.append(msg)
                    f.write(msg + "\n")

            active_procs = [p for p in procs if p.is_arrived and p.pc < p.total_instr]
            if not active_procs:
                time.sleep(0.5); continue

            p = active_procs[current_idx % len(active_procs)]
            if p.start_exec_time is None: p.start_exec_time = int(time.time() - start_sim_time)

            total_switches += 1
            switch_msg = f"T+{int(elapsed)}s: [SW] {last_p_name}->{p.name}"
            logs.append(switch_msg)
            f.write(switch_msg + "\n")
           
            if len(logs) > 5: logs.pop(0)
            last_p_name = p.name

            # Switch Animation Stable
            stdscr.clear()
            h_y, w_x = stdscr.getmaxyx()
            stdscr.addstr(h_y//2, (w_x-30)//2, f" ⚡ SWITCHING TO PCB_{p.pid} ⚡ ", curses.color_pair(3) | curses.A_REVERSE)
            stdscr.refresh()
            time.sleep(0.8)

            start_tick = time.time()
            while (time.time() - start_tick) <= time_quantum and p.pc < p.total_instr:
                stdscr.clear()
                h_y, w_x = stdscr.getmaxyx()
               
                # Title
                stdscr.addstr(1, (w_x-45)//2, "⚛ CONTEXT SWITCHING ANALYZER ⚛", curses.color_pair(5) | curses.A_BOLD)

                # Boxes placement
                draw_custom_box(stdscr, 3, 2, 9, 45, "CPU CORE", 1)
                stdscr.addstr(5, 5, f"RUNNING: {p.name}", curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(6, 5, f"PC: 0x{p.pc:04X} | PID: {p.pid}")
                progress = int((p.pc / p.total_instr) * 30)
                bar = "█" * progress + "░" * (30 - progress)
                stdscr.addstr(8, 5, f"LOAD: [{bar}]", curses.color_pair(1))
                stdscr.addstr(10, 5, f"R1:{p.registers['R1']} R2:{p.registers['R2']} R3:{p.registers['R3']}")

                draw_custom_box(stdscr, 3, 50, 9, 42, "READY QUEUE", 2)
                for i, pr in enumerate(procs):
                    indicator = "▶" if pr == p else " "
                    state = "DONE" if pr.pc >= pr.total_instr else ("RUN" if pr == p else "WAIT")
                    if not pr.is_arrived: state = "[PENDING]"
                    stdscr.addstr(5+i, 53, f"{indicator} {pr.name}: {state}", curses.color_pair(2))

                draw_custom_box(stdscr, 14, 2, 7, 90, "KERNEL LIVE LOGS", 4)
                for i, log in enumerate(logs):
                    stdscr.addstr(15+i, 5, f"» {log}")

                # Status Bar position
                rem = time_quantum - int(time.time() - start_tick)
                status = f" QUANTUM: {max(0,rem):02d}s | UPTIME: {int(time.time()-start_sim_time):03d}s | SWITCHES: {total_switches:03d} "
                stdscr.addstr(h_y-2, (w_x-len(status))//2, status, curses.A_REVERSE | curses.color_pair(2))

                p.pc += 1
                p.registers = {k: random.randint(1000, 9999) for k in p.registers}
                if p.pc >= p.total_instr: p.completion_time = int(time.time() - start_sim_time)
               
                stdscr.refresh()
                time.sleep(1)
            current_idx += 1

        # Save stats to file
        f.write("\n--- FINAL STATISTICS ---\n")
        f.write(f"{'Process':<12} | {'Arrival':<8} | {'Start':<8} | {'End':<8}\n")
        for p in procs:
            f.write(f"{p.name:<12} | {p.arrival_time:<8} | {p.start_exec_time:<8} | {p.completion_time:<8}\n")

    # End Screen
    stdscr.clear()
    h_y, w_x = stdscr.getmaxyx()
    draw_custom_box(stdscr, 5, 10, 12, 80, " SIMULATION COMPLETE ", 3)
    stdscr.addstr(8, 15, f"Total System Uptime: {int(time.time()-start_sim_time)}s", curses.A_BOLD)
    stdscr.addstr(10, 15, "Full audit report saved to history_log.txt", curses.color_pair(2))
    stdscr.addstr(h_y-4, (w_x-45)//2, " [R] RESTART SIMULATION  |  [Q] EXIT SYSTEM ", curses.A_BLINK | curses.color_pair(6))
    stdscr.refresh()
   
    stdscr.nodelay(0)
    while True:
        ch = stdscr.getch()
        if ch in [ord('r'), ord('R')]: return True
        if ch in [ord('q'), ord('Q')]: return False

if __name__ == "__main__":
    while True:
        try:
            if not curses.wrapper(run_simulation): break
        except KeyboardInterrupt: break
