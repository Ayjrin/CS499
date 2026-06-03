import os
import time


class HashTableSearch:
    """
    Enhanced search engine using a Hash Table (Python dictionary)
    to provide O(1) average search complexity.
    """

    def __init__(self):
        self.lookup_table = {}
        self.record_count = 0

    def add_record(self, data, sequence):
        # We store the data string as the key.
        # Since the requirement is to search for a word and display it,
        # and exact match is implied, the hash table is ideal.
        # If multiple records have the same word, we'll store the first one encountered,
        # consistent with the original heap DFS behavior.
        if data not in self.lookup_table:
            self.lookup_table[data] = sequence
            self.record_count += 1

    def search(self, word):
        # Time the lookup to demonstrate performance gain.
        start_time = time.perf_counter()
        # In a hash table, the 'search' is an O(1) lookup.
        # We return 1 for 'records searched' to indicate the direct access.
        found_sequence = self.lookup_table.get(word)
        end_time = time.perf_counter()

        search_duration = end_time - start_time
        return found_sequence, 1, search_duration


def load_data(file_path):
    engine = HashTableSearch()
    try:
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return engine

            # Skip header line (e.g., sequence|data)
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) == 2:
                    try:
                        seq = int(parts[0])
                        data = parts[1]
                        engine.add_record(data, seq)
                    except ValueError:
                        # Skip malformed lines
                        continue
        return engine
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


def main():
    # File path configuration matching the original structure
    base_path = "Module Eight Activity Data Sets/Module 8 Data Set-"

    print("--- CS680 Module Eight Search (ENHANCED) ---")
    print("Architectural Optimization: Hash Table (O(1) Search)")

    dataset_num = input(
        "Enter the numbered data set you want to search (1 - 5): "
    ).strip()
    file_path = base_path + dataset_num + ".csv"

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f"Loading data from {file_path} into an optimized Hash Table...")
    start_load = time.perf_counter()
    engine = load_data(file_path)
    end_load = time.perf_counter()

    if engine is None:
        return

    print(f"Data loaded successfully in {end_load - start_load:.4f} seconds.")
    print(f"Total unique records indexed: {engine.record_count}")

    while True:
        search_word = input(
            "\nEnter a word to search for (or 'quit' to exit): "
        ).strip()

        if search_word.lower() == "quit":
            print("Exiting search application.")
            break

        if not search_word:
            continue

        # Execute the optimized search
        found_seq, records_searched, duration = engine.search(search_word)

        print("\n--- Search Results ---")
        if found_seq is not None:
            # Result found. Labeled data field shown; integer sequence hidden.
            print(f"Data: {search_word}")
        else:
            print(f"The value '{search_word}' was not located within the data set.")

        print(f"Records searched: {records_searched}")
        print(f"Search time: {duration:.8f} seconds")
        print("----------------------")


if __name__ == "__main__":
    main()
