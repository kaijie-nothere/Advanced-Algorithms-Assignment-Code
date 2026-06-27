import time


def compute_factorial(n: int) -> int:
    """Calculates the factorial of a given number."""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def run_sequential_round() -> int:
    """
    Calculates 50!, 100!, and 200! sequentially (without multithreading).
    Measures and returns the total time taken in nanoseconds.
    """
    # Capture: Start Time before the first calculation begins
    start_time = time.perf_counter_ns()

    # Execute the calculations one after another in a single thread
    compute_factorial(50)
    compute_factorial(100)
    compute_factorial(200)

    # Capture: End Time after the final calculation finishes
    end_time = time.perf_counter_ns()

    # Formula: Time_Elapsed = End_Time - Start_Time
    time_elapsed = end_time - start_time

    return time_elapsed


def main():
    """Runs the sequential benchmark for 10 rounds and calculates the average."""
    total_rounds = 10
    round_times = []

    # --- Print Table Header ---
    print("\n" + "=" * 45)
    print(" FACTORIAL SEQUENTIAL BENCHMARK SUITE")
    print("=" * 45)
    print(f"{'Round Index':<15} | {'Time Taken (T) in ns':<25}")
    print("-" * 45)

    # --- Run 10 Rounds ---
    for round_num in range(1, total_rounds + 1):
        # Get Time taken (T) for this sequential round
        t = run_sequential_round()
        round_times.append(t)

        # Display T for each round
        print(f"Round {round_num:<9} | {t:<25}")

    # --- Calculate and Display Average ---
    print("-" * 45)
    average_t = sum(round_times) / total_rounds
    print(f"{'AVERAGE (T)':<15} | {average_t:<25.2f}")
    print("=" * 45 + "\n")


if __name__ == "__main__":
    main()