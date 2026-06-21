import os
import sys
import time


class MinHeapString:
    def __init__(self):
        self.heap = []

    def insert(self, record):
        # record is a tuple (data, sequence)
        self.heap.append(record)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self.heap[index], self.heap[parent_index] = (
                self.heap[parent_index],
                self.heap[index],
            )
            self._heapify_up(parent_index)

    def dfs_search(self, search_word):
        records_searched = [0]

        def dfs(index):
            if index >= len(self.heap):
                return None

            records_searched[0] += 1
            current_data = self.heap[index][0]

            if current_data == search_word:
                return self.heap[index]

            # Optimization: If the current node is lexicographically greater than the search word,
            # we don't need to search its children because it's a min-heap and all children
            # will be even greater (or equal).
            if search_word < current_data:
                return None

            left_result = dfs(2 * index + 1)
            if left_result:
                return left_result

            right_result = dfs(2 * index + 2)
            if right_result:
                return right_result

            return None

        result = dfs(0)
        return result, records_searched[0]


def load_data(file_path):
    heap = MinHeapString()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) == 2:
                        sequence = int(parts[0])
                        data = parts[1]
                        heap.insert((data, sequence))
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    return heap


def main():
    base = "Module Eight Activity Data Sets/Module 8 Data Set-"
    i = input("Enter the numbered data set you want to search (1 - 5): ")
    file_path = base + str(i) + ".csv"

    if not os.path.exists(file_path):
        print("File not found.")
        return

    print(f"Loading data from {file_path} into a min-heap...")
    start_load = time.time()
    heap = load_data(file_path)
    if not heap:
        return
    end_load = time.time()
    print(f"Data loaded successfully in {end_load - start_load:.4f} seconds.")
    print(f"Total records in heap: {len(heap.heap)}")

    while True:
        search_word = input(
            "\nEnter a word to search for (or 'quit' to exit): "
        ).strip()
        if search_word.lower() == "quit":
            break

        if not search_word:
            continue

        start_time = time.time()
        result, records_searched = heap.dfs_search(search_word)
        end_time = time.time()

        print("\n--- Search Results ---")
        if result:
            print(f"Data: {result[0]}")
        else:
            print(f"The value '{search_word}' was not located within the data set.")

        print(f"Records searched: {records_searched}")
        print(f"Search time: {end_time - start_time:.6f} seconds")
        print("----------------------")


if __name__ == "__main__":
    main()
