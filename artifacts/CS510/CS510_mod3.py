"""
A multithreaded program template.
"""

import os
import queue
import threading
import time

import psutil


def functionOne(stop_event, data_queue):
    """
    Monitors CPU usage percentage.
    Puts updates into data_queue.
    """
    try:
        while not stop_event.is_set():
            # Get CPU percentage (blocking call for 1 second)
            cpu_usage = psutil.cpu_percent(interval=1)
            data_queue.put(("CPU", f"{cpu_usage}%"))
    finally:
        # Ensures this runs even if an exception occurs
        data_queue.put(("CPU", "Stopped"))
        data_queue.put(None)  # Signal that this thread is done


def functionTwo(stop_event, data_queue):
    """
    Monitors RAM usage percentage.
    Puts updates into data_queue.
    """
    try:
        while not stop_event.is_set():
            # Get RAM percentage
            ram_usage = psutil.virtual_memory().percent
            data_queue.put(("RAM", f"{ram_usage}%"))
            stop_event.wait(timeout=2)
    finally:
        data_queue.put(("RAM", "Stopped"))
        data_queue.put(None)


def functionThree(stop_event, data_queue):
    """
    Monitors Network Speed (Upload/Download).
    Puts updates into data_queue.
    """
    old_net = psutil.net_io_counters()

    try:
        while not stop_event.is_set():
            stop_event.wait(timeout=1)
            if stop_event.is_set():
                break

            new_net = psutil.net_io_counters()

            sent_speed = new_net.bytes_sent - old_net.bytes_sent
            recv_speed = new_net.bytes_recv - old_net.bytes_recv

            msg = (
                f"Up: {sent_speed / 1024:.1f} KB/s, Down: {recv_speed / 1024:.1f} KB/s"
            )
            data_queue.put(("NET", msg))

            old_net = new_net
    finally:
        data_queue.put(("NET", "Stopped"))
        data_queue.put(None)


def dashboard_display(stop_event, data_queue):
    """
    Reads from the queue and updates the terminal display.
    Acts as the single source of truth for screen output.
    """
    state = {
        "CPU": "Initializing...",
        "RAM": "Initializing...",
        "NET": "Initializing...",
    }

    active_workers = 3

    # Clear screen once at start
    os.system("cls" if os.name == "nt" else "clear")

    while active_workers > 0:
        try:
            # Wait for an update from any thread
            item = data_queue.get(timeout=0.5)

            if item is None:
                active_workers -= 1
                continue

            source, message = item
            state[source] = message

            # Move cursor to top-left (ANSI escape code)
            print("\033[H", end="")

            print("=" * 40)
            print(" SYSTEM MONITORING DASHBOARD")
            print("=" * 40)
            print(f" CPU Usage     : {state['CPU']:<20}")
            print(f" RAM Usage     : {state['RAM']:<20}")
            print(f" Network Speed : {state['NET']:<20}")
            print("-" * 40)
            if not stop_event.is_set():
                print(" Press ENTER to stop monitoring.")
            else:
                print(" Stopping threads... please wait.")
            print("=" * 40)

        except queue.Empty:
            pass


def main():
    """
    Entry point of the program: Create, start and join threads
    """
    stop_signal = threading.Event()
    data_queue = queue.Queue()

    # Create worker threads
    one_thread = threading.Thread(target=functionOne, args=(stop_signal, data_queue))
    two_thread = threading.Thread(target=functionTwo, args=(stop_signal, data_queue))
    three_thread = threading.Thread(
        target=functionThree, args=(stop_signal, data_queue)
    )

    # Create display thread
    display_thread = threading.Thread(
        target=dashboard_display, args=(stop_signal, data_queue)
    )

    # Start all threads
    one_thread.start()
    two_thread.start()
    three_thread.start()
    display_thread.start()

    # Main thread waits for user input
    try:
        input()
    except EOFError:
        pass  # Handle case where input stream is closed

    # Shutdown sequence
    stop_signal.set()

    one_thread.join()
    two_thread.join()
    three_thread.join()
    display_thread.join()

    print("\nMain: Monitoring stopped successfully.")


if __name__ == "__main__":
    main()
