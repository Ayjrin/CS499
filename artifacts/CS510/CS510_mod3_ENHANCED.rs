//! A multithreaded program template ported from Python to Rust.
//!
//! Dependencies (add to Cargo.toml):
//! [dependencies]
//! sysinfo = "0.30"

use std::io::{self, Write};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc::{self, Sender};
use std::sync::Arc;
use std::thread;
use std::time::Duration;

use sysinfo::{CpuRefreshKind, MemoryRefreshKind, Networks, RefreshKind, System};

/// Define the type of messages sent to the dashboard
enum MonitorUpdate {
    Cpu(String),
    Ram(String),
    Net(String),
    Stopped(&'static str),
    Done,
}

/// Monitors CPU usage percentage.
/// Puts updates into data_queue.
fn read_cpu(stop_event: Arc<AtomicBool>, tx: Sender<MonitorUpdate>) {
    let mut sys =
        System::new_with_specifics(RefreshKind::new().with_cpu(CpuRefreshKind::everything()));

    while !stop_event.load(Ordering::SeqCst) {
        // sysinfo needs a refresh to calculate CPU usage over an interval
        sys.refresh_cpu();
        thread::sleep(Duration::from_secs(1));
        sys.refresh_cpu();

        let cpu_usage = sys.global_cpu_info().cpu_usage();
        if tx
            .send(MonitorUpdate::Cpu(format!("{:.1}%", cpu_usage)))
            .is_err()
        {
            break;
        }
    }
    let _ = tx.send(MonitorUpdate::Stopped("CPU"));
    let _ = tx.send(MonitorUpdate::Done);
}

/// Monitors RAM usage percentage.
/// Puts updates into data_queue.
fn read_ram(stop_event: Arc<AtomicBool>, tx: Sender<MonitorUpdate>) {
    let mut sys =
        System::new_with_specifics(RefreshKind::new().with_memory(MemoryRefreshKind::everything()));

    while !stop_event.load(Ordering::SeqCst) {
        sys.refresh_memory();
        let total = sys.total_memory();
        let used = sys.used_memory();

        let ram_usage = if total > 0 {
            (used as f64 / total as f64) * 100.0
        } else {
            0.0
        };

        if tx
            .send(MonitorUpdate::Ram(format!("{:.1}%", ram_usage)))
            .is_err()
        {
            break;
        }

        // Emulate stop_event.wait(timeout=2)
        for _ in 0..20 {
            if stop_event.load(Ordering::SeqCst) {
                break;
            }
            thread::sleep(Duration::from_millis(100));
        }
    }
    let _ = tx.send(MonitorUpdate::Stopped("RAM"));
    let _ = tx.send(MonitorUpdate::Done);
}

/// Monitors Network Speed (Upload/Download).
/// Puts updates into data_queue.
fn read_network(stop_event: Arc<AtomicBool>, tx: Sender<MonitorUpdate>) {
    let mut networks = Networks::new_with_refreshed_list();

    // Initial reading
    let mut last_total_rx: u64 = networks.iter().map(|(_, d)| d.total_received()).sum();
    let mut last_total_tx: u64 = networks.iter().map(|(_, d)| d.total_transmitted()).sum();

    while !stop_event.load(Ordering::SeqCst) {
        // Wait 1 second (logic from Python's stop_event.wait(timeout=1))
        for _ in 0..10 {
            if stop_event.load(Ordering::SeqCst) {
                break;
            }
            thread::sleep(Duration::from_millis(100));
        }

        if stop_event.load(Ordering::SeqCst) {
            break;
        }

        networks.refresh();
        let current_rx: u64 = networks.iter().map(|(_, d)| d.total_received()).sum();
        let current_tx: u64 = networks.iter().map(|(_, d)| d.total_transmitted()).sum();

        let rx_speed = (current_rx.saturating_sub(last_total_rx)) as f64 / 1024.0;
        let tx_speed = (current_tx.saturating_sub(last_total_tx)) as f64 / 1024.0;

        let msg = format!("Up: {:.1} KB/s, Down: {:.1} KB/s", tx_speed, rx_speed);
        if tx.send(MonitorUpdate::Net(msg)).is_err() {
            break;
        }

        last_total_rx = current_rx;
        last_total_tx = current_tx;
    }
    let _ = tx.send(MonitorUpdate::Stopped("NET"));
    let _ = tx.send(MonitorUpdate::Done);
}

/// Reads from the queue and updates the terminal display.
/// Acts as the single source of truth for screen output.
fn dashboard_display(stop_event: Arc<AtomicBool>, rx: mpsc::Receiver<MonitorUpdate>) {
    let mut cpu_state = String::from("Initializing...");
    let mut ram_state = String::from("Initializing...");
    let mut net_state = String::from("Initializing...");
    let mut active_workers = 3;

    // Clear screen once at start
    print!("\x1B[2J\x1B[1;1H");
    let _ = io::stdout().flush();

    while active_workers > 0 {
        // Wait for an update from any thread with a timeout (similar to queue.get(timeout=0.5))
        if let Ok(update) = rx.recv_timeout(Duration::from_millis(500)) {
            match update {
                MonitorUpdate::Cpu(msg) => cpu_state = msg,
                MonitorUpdate::Ram(msg) => ram_state = msg,
                MonitorUpdate::Net(msg) => net_state = msg,
                MonitorUpdate::Stopped(source) => match source {
                    "CPU" => cpu_state = "Stopped".to_string(),
                    "RAM" => ram_state = "Stopped".to_string(),
                    "NET" => net_state = "Stopped".to_string(),
                    _ => {}
                },
                MonitorUpdate::Done => active_workers -= 1,
            }

            // Move cursor to top-left (ANSI escape code)
            print!("\x1b[H");

            println!("========================================");
            println!(" SYSTEM MONITORING DASHBOARD");
            println!("========================================");
            println!(" CPU Usage     : {:<20}", cpu_state);
            println!(" RAM Usage     : {:<20}", ram_state);
            println!(" Network Speed : {:<20}", net_state);
            println!("----------------------------------------");
            if !stop_event.load(Ordering::SeqCst) {
                println!(" Press ENTER to stop monitoring.");
            } else {
                println!(" Stopping threads... please wait.");
            }
            println!("========================================");
            let _ = io::stdout().flush();
        }
    }
}

/// Entry point of the program: Create, start and join threads
fn main() {
    let stop_signal = Arc::new(AtomicBool::new(false));
    let (tx, rx) = mpsc::channel();

    // Create worker threads
    let stop1 = Arc::clone(&stop_signal);
    let tx1 = tx.clone();
    let one_thread = thread::spawn(move || read_cpu(stop1, tx1));

    let stop2 = Arc::clone(&stop_signal);
    let tx2 = tx.clone();
    let two_thread = thread::spawn(move || read_ram(stop2, tx2));

    let stop3 = Arc::clone(&stop_signal);
    let tx3 = tx.clone();
    let three_thread = thread::spawn(move || read_network(stop3, tx3));

    // Create display thread
    let stop_display = Arc::clone(&stop_signal);
    let display_thread = thread::spawn(move || dashboard_display(stop_display, rx));

    // Main thread waits for user input
    let mut input = String::new();
    let _ = io::stdin().read_line(&mut input);

    // Shutdown sequence
    stop_signal.store(true, Ordering::SeqCst);

    let _ = one_thread.join();
    let _ = two_thread.join();
    let _ = three_thread.join();
    let _ = display_thread.join();

    println!("\nMain: Monitoring stopped successfully.");
}
