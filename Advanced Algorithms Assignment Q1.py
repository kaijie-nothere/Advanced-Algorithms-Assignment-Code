import time


# --- Entity Class ---
class Medicine:
    """Represents a pharmacy product item."""

    def __init__(self, product_id, name, product_type, price, stock):
        self.product_id = product_id  # Unique identifier (Key)
        self.name = name  # Name of the medicine
        self.product_type = product_type  # e.g., 'tablets', 'syrup', 'supplements'
        self.price = price  # Unit price
        self.stock = stock  # Inventory count

    def __repr__(self):
        return (
            f"Medicine(ID: {self.product_id}, Name: {self.name}, Type: {self.product_type},"
            f" Price: ${self.price:.2f}, Stock: {self.stock})"
        )


# --- Hash Table with Linear Probing ---
class PharmacyHashTable:
    """Hash Table using Open Addressing with Linear Probing."""

    def __init__(self, size=20):
        self.size = size
        # Array structure for buckets: initialized with None to represent empty slots
        self.table = [None] * self.size

    def _hash_function(self, key):
        """Simple modulo arithmetic hash function."""
        return key % self.size

    def insert(self, medicine):
        """Inserts a medicine object using linear probing for collision resolution."""
        key = medicine.product_id
        index = self._hash_function(key)
        initial_index = index

        while self.table[index] is not None:
            # If the product_id already exists, update the entry
            if self.table[index].product_id == key:
                self.table[index] = medicine
                return True

            # Linear Probing: move to the next index sequentially
            index = (index + 1) % self.size

            # Table is full
            if index == initial_index:
                print("Error: Hash Table is full!")
                return False

        self.table[index] = medicine
        return True

    def search(self, product_id):
        """Searches for a record using linear probing."""
        index = self._hash_function(product_id)
        initial_index = index

        while self.table[index] is not None:
            if self.table[index].product_id == product_id:
                return self.table[index]

            index = (index + 1) % self.size
            if index == initial_index:
                break
        return None

    def display_all(self):
        """Displays all occupied buckets in the system."""
        print("\n--- Current Pharmacy Inventory Structure ---")
        for i, entry in enumerate(self.table):
            if entry is not None:
                print(f"Slot {i:2d} -> {entry}")
            else:
                print(f"Slot {i:2d} -> [Empty]")


# --- Performance Testing Helper (1-Dimensional Array Setup) ---
class LinearArrayStorage:
    """Simple wrapper for a 1D list to perform linear searches."""

    def __init__(self):
        self.array = []

    def insert(self, medicine):
        self.array.append(medicine)

    def search(self, product_id):
        for item in self.array:
            if item.product_id == product_id:
                return item
        return None


# --- Command-Line Interface and Main Application ---
def main_pharmacy_app():
    # Initialize both storage structures with a standard table capacity
    hash_table = PharmacyHashTable(size=15)
    linear_array = LinearArrayStorage()

    samples = [
        Medicine(101, "Paracetamol", "tablets", 4.50, 120),
        Medicine(205, "Cough Syrup", "syrup", 8.20, 45),
        Medicine(112, "Vitamin C", "supplements", 15.00, 60),
        Medicine(304, "Amoxicillin", "tablets", 12.00, 30),
        Medicine(115, "Ibuprofen", "tablets", 5.50, 85),
    ]

    while True:
        print("\n================ Pharmacy Menu ================")
        print("1. Display All Records (See structural buckets)")
        print("2. Insert a New Product")
        print("3. Search Product & Run Live Performance Test")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            hash_table.display_all()

        elif choice == "2":
            try:
                pid = int(input("Enter Product ID (int): "))
                name = input("Enter Product Name: ")
                ptype = input("Enter Product Type (tablets/syrup/supplements): ")
                price = float(input("Enter Price: "))
                stock = int(input("Enter Stock Count: "))

                med = Medicine(pid, name, ptype, price, stock)
                if hash_table.insert(med):
                    linear_array.insert(med)
                    print("Product successfully stored in both structures!")
            except ValueError:
                print("Invalid input types provided. Try again.")

        elif choice == "3":
            try:
                # Ask the user for a custom key dynamically
                search_id = int(input("Enter ANY Product ID to search and compare: "))

                # Check classification status for reporting clarity
                match_check = hash_table.search(search_id)
                classification = "Existing Key" if match_check else "Non-Existing Key"

                # 1. Benchmark for Hash Table
                start_hash = time.perf_counter_ns()
                res_hash = hash_table.search(search_id)
                end_hash = time.perf_counter_ns()
                hash_duration = end_hash - start_hash

                # 2. Benchmark for 1D Array
                start_arr = time.perf_counter_ns()
                res_arr = linear_array.search(search_id)
                end_arr = time.perf_counter_ns()
                arr_duration = end_arr - start_arr

                # Display Results in a Clean Table Matrix
                print("\n" + "=" * 85)
                print(f"{'Target ID':<12}{'Key Classification':<25}{'Hash Table Search':<24}{'1D Array Search':<24}")
                print("-" * 85)
                print(f"{search_id:<12}{classification:<25}{f'{hash_duration} ns':<24}{f'{arr_duration} ns':<24}")
                print("=" * 85)

                # Output the item details if found
                if res_hash:
                    print(f" Search Result: Item Found!\n   ↳ {res_hash}")
                else:
                    print(f" Search Result: Product ID {search_id} does not exist in the database.")

            except ValueError:
                print("Invalid format. Product ID must be an integer value.")

        elif choice == "4":
            print("Exiting Pharmacy System.")
            break


if __name__ == "__main__":
    main_pharmacy_app()