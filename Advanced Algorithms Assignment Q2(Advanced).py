import time


# --- Entity Class ---
class Transaction:
    """Represents a retail commercial transaction (Entity Class)."""

    def __init__(self, transaction_id: int, customer_name: str, product_name: str, amount: float,
                 transaction_date: str):
        self.transaction_id = transaction_id  # Unique Identifier Primary Key
        self.customer_name = customer_name
        self.product_name = product_name
        self.amount = amount
        self.transaction_date = transaction_date

    def __repr__(self):
        return (f"[TX-ID: {self.transaction_id:03d} | Client: {self.customer_name:<10} "
                f" | Product: {self.product_name:<12} | Total: ${self.amount:<7.2f} | Date: {self.transaction_date}]")


# --- Merge Sort Helper State ---
class MergeSortTracker:
    """Helper wrapper to maintain state during tracked Merge Sort processes."""

    def __init__(self):
        self.call_count = 0

    def reset(self):
        self.call_count = 0


# --- Merge Sort (Divide & Conquer) ---
def tracked_merge_sort(arr: list, attribute: str, tracker: MergeSortTracker) -> list:
    """Advanced implementation of Merge Sort that captures and logs recursion metrics."""
    tracker.call_count += 1  # ADVANCED FEATURE: Track recursive iterations

    # Base Case: Array segment of size 1 or 0 is intrinsically sorted.
    if len(arr) <= 1:
        return arr

    # 1. DIVIDE Phase: Bisect array via structural midpoint
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # 2. CONQUER Phase: Recursively process individual subsegments
    left_sorted = tracked_merge_sort(left_half, attribute, tracker)
    right_sorted = tracked_merge_sort(right_half, attribute, tracker)

    # 3. COMBINE Phase: Collate segments using designated criteria
    return merge(left_sorted, right_sorted, attribute)


def merge(left: list, right: list, attribute: str) -> list:
    """Stitches two independent sorted slices into a uniform sequence."""
    merged_output = []
    i = j = 0

    while i < len(left) and j < len(right):
        # ADVANCED FEATURE: Support dynamic sorting by variable attributes
        val_left = getattr(left[i], attribute)
        val_right = getattr(right[j], attribute)

        if val_left <= val_right:
            merged_output.append(left[i])
            i += 1
        else:
            merged_output.append(right[j])
            j += 1

    # Flush out remaining entries
    merged_output.extend(left[i:])
    merged_output.extend(right[j:])
    return merged_output


# --- Binary Search (Divide & Conquer) ---
def recursive_binary_search(arr: list, target_id: int, low: int, high: int) -> int:
    """Recursive Binary Search implementation over a sorted list."""
    if low > high:
        return -1  # Target completely absent from space

    # DIVIDE phase
    mid = (low + high) // 2
    current_id = arr[mid].transaction_id

    # CONQUER & COMBINE phases
    if current_id == target_id:
        return mid
    elif current_id > target_id:
        return recursive_binary_search(arr, target_id, low, mid - 1)
    else:
        return recursive_binary_search(arr, target_id, mid + 1, high)


# --- Linear Search Baseline ---
def linear_search_baseline(arr: list, target_id: int) -> int:
    """Sequential fallback loop used to contrast algorithmic runtimes."""
    for index, item in enumerate(arr):
        if item.transaction_id == target_id:
            return index
    return -1


# --- Command-Line Interface and Main Application ---
def main_transaction_suite():
    # Create an initial unsorted dataset with 10 records
    dataset = [
        Transaction(104, "Alice", "Laptop", 1249.99, "2026-06-20"),
        Transaction(101, "Bob", "Headphones", 149.50, "2026-06-21"),
        Transaction(109, "Charlie", "Smartphone", 899.00, "2026-06-21"),
        Transaction(102, "David", "Mechanical KB", 85.00, "2026-06-22"),
        Transaction(108, "Emma", "Monitor", 320.00, "2026-06-22"),
        Transaction(105, "Frank", "Gaming Mouse", 65.25, "2026-06-23"),
        Transaction(103, "Grace", "Office Chair", 199.99, "2026-06-23"),
        Transaction(110, "Henry", "USB-C Hub", 45.00, "2026-06-24"),
        Transaction(107, "Ivy", "Desk Mat", 29.99, "2026-06-24"),
        Transaction(106, "Jack", "HDMI Cable", 15.50, "2026-06-25")
    ]

    sort_tracker = MergeSortTracker()
    is_sorted_by_id = False

    while True:
        print("\n================ Transaction Analytics Board ================")
        print("1. Display All Current Database Records [Compulsory]")
        print("2. Run Recursive Merge Sort [Compulsory + Advanced Parameters]")
        print("3. Execute Binary Search [Compulsory - Requires Sorted Keys]")
        print("4. Execute Baseline Linear Search [Compulsory]")
        print("5. Dynamic Data Ingestion Link [Advanced Option A]")
        print("6. Exit Suite")

        choice = input("Enter option index (1-6): ").strip()

        if choice == '1':
            print("\n--- Current Dataset ---")
            for item in dataset:
                print(item)

        elif choice == '2':
            print("\nSort by which criteria?")
            print("a) Transaction ID\nb) Purchase Amount")
            mode = input("Choice (a/b): ").strip().lower()
            target_attr = "transaction_id" if mode != 'b' else "amount"

            print("\nArray Before Merge Sort:")
            for item in dataset: print(item)

            sort_tracker.reset()
            t_start = time.perf_counter_ns()
            dataset = tracked_merge_sort(dataset, target_attr, sort_tracker)
            t_duration = time.perf_counter_ns() - t_start

            print("\nArray After Merge Sort:")
            for item in dataset: print(item)

            print(f"\n[Performance Profile]: Sorted by '{target_attr}' in {t_duration} ns.")
            print(f"[Recursion Metrics]: Total Divide & Conquer Stack Operations: {sort_tracker.call_count}")
            if target_attr == "transaction_id":
                is_sorted_by_id = True

        elif choice == '3':
            if not is_sorted_by_id:
                print(" Search Warning: Binary Search requires a collection sorted strictly by Transaction ID. Run Option 2(a) first.")
                continue
            try:
                tid = int(input("Enter search target Transaction ID: "))
                t_start = time.perf_counter_ns()
                idx = recursive_binary_search(dataset, tid, 0, len(dataset) - 1)
                t_duration = time.perf_counter_ns() - t_start

                if idx != -1:
                    print(f"✓ Found target record at collection index [{idx}]:\n  {dataset[idx]}")
                else:
                    print(f" Record ID {tid} was not located within this data store.")
                print(f"[Search Performance]: Binary search completed in {t_duration} ns.")
            except ValueError:
                print("Invalid data type format entered.")

        elif choice == '4':
            try:
                tid = int(input("Enter baseline search target Transaction ID: "))
                t_start = time.perf_counter_ns()
                idx = linear_search_baseline(dataset, tid)
                t_duration = time.perf_counter_ns() - t_start

                if idx != -1:
                    print(f"✓ Found item via Linear sweep at index [{idx}]:\n  {dataset[idx]}")
                else:
                    print(" Target item not found.")
                print(f"[Search Performance]: Linear baseline executed in {t_duration} ns.")
            except ValueError:
                print("Invalid numerical data.")

        elif choice == '5':
            try:
                new_id = int(input("Assign New Transaction ID: "))
                c_name = input("Customer Name: ").strip()
                p_name = input("Product Label: ").strip()
                amt = float(input("Purchase Amount ($): "))
                dt = input("Date Token (YYYY-MM-DD): ").strip()

                dataset.append(Transaction(new_id, c_name, p_name, amt, dt))
                is_sorted_by_id = False  # Reset sorting constraint since a new record was added
                print("✓ Record safely appended to primary array storage.")
            except ValueError:
                print("Input verification failure. Entry dropped.")

        elif choice == '6':
            print("Terminating Analytics Suite System.")
            break


if __name__ == "__main__":
    main_transaction_suite()