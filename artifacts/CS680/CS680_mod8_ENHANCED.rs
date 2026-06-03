use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead, Write};
use std::path::Path;
use std::time::Instant;

struct SearchEngine {
    lookup_table: HashMap<String, i32>,
}

impl SearchEngine {
    fn new() -> Self {
        Self {
            lookup_table: HashMap::new(),
        }
    }

    fn add_record(&mut self, data: String, sequence: i32) {
        self.lookup_table.entry(data).or_insert(sequence);
    }

    fn search(&self, word: &str) -> (Option<i32>, u64, std::time::Duration) {
        let start = Instant::now();
        let result = self.lookup_table.get(word).copied();
        let duration = start.elapsed();
        (result, 1, duration)
    }

    fn len(&self) -> usize {
        self.lookup_table.len()
    }
}

fn load_data(file_path: &str) -> io::Result<SearchEngine> {
    let path = Path::new(file_path);
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let mut engine = SearchEngine::new();

    let mut lines = reader.lines();
    // Skip header
    lines.next();

    for line in lines {
        let line = line?;
        let parts: Vec<&str> = line.split('|').collect();
        if parts.len() == 2 {
            if let Ok(seq) = parts[0].parse::<i32>() {
                engine.add_record(parts[1].to_string(), seq);
            }
        }
    }

    Ok(engine)
}

fn main() {
    println!("--- CS680 Module Eight Search (RUST ENHANCED) ---");
    println!("Architectural Optimization: HashMap (O(1) Search)");

    print!("Enter the numbered data set you want to search (1 - 5): ");
    io::stdout().flush().unwrap();

    let mut dataset_num = String::new();
    io::stdin().read_line(&mut dataset_num).unwrap();
    let dataset_num = dataset_num.trim();

    let file_path = format!(
        "Module Eight Activity Data Sets/Module 8 Data Set-{}.csv",
        dataset_num
    );

    println!(
        "Loading data from {} into an optimized HashMap...",
        file_path
    );
    let start_load = Instant::now();
    let engine = match load_data(&file_path) {
        Ok(e) => e,
        Err(err) => {
            println!("Error loading file: {}", err);
            return;
        }
    };
    let load_duration = start_load.elapsed();

    println!("Data loaded successfully in {:.4?} seconds.", load_duration);
    println!("Total unique records indexed: {}", engine.len());

    loop {
        print!("\nEnter a word to search for (or 'quit' to exit): ");
        io::stdout().flush().unwrap();

        let mut search_word = String::new();
        io::stdin().read_line(&mut search_word).unwrap();
        let search_word = search_word.trim();

        if search_word.to_lowercase() == "quit" {
            println!("Exiting search application.");
            break;
        }

        if search_word.is_empty() {
            continue;
        }

        let (found_seq, records_searched, duration) = engine.search(search_word);

        println!("\n--- Search Results ---");
        if found_seq.is_some() {
            println!("Data: {}", search_word);
        } else {
            println!(
                "The value '{}' was not located within the data set.",
                search_word
            );
        }

        println!("Records searched: {}", records_searched);
        println!("Search time: {:.8?}", duration);
        println!("----------------------");
    }
}
