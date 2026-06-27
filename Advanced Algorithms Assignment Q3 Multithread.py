import threading
import time


def compute_factorial(n: int) -> int:
    """Calculates the factorial of a given number."""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def run_multithreaded_round() -> int:
    """Creates 3 separate threads to calculate 50!, 100!, and 200!.
    Measures and returns the total time taken in nanoseconds."""

    targets = [50, 100, 200]
    threads = []

    # Capture: Start_Time_Of_Thread_That_Started_First
    start_time = time.perf_counter_ns()

    # Create and start 3 separate threads (one for each operation)
    for num in targets:
        worker = threading.Thread(target=compute_factorial, args=(num,))
        threads.append(worker)
        worker.start()

    # Block main program until all 3 threads have safely finished
    for worker in threads:
        worker.join()

    # Capture: End_Time_Of_Thread_Finished_Last
    end_time = time.perf_counter_ns()

    # Formula: Time_Elapsed = End_Time - Start_Time
    time_elapsed = end_time - start_time

    return time_elapsed


def main():
    """Runs the benchmark for 10 rounds and calculates the average."""
    total_rounds = 10
    round_times = []

    # --- Print Table Header ---
    print("\n" + "=" * 45)
    print(" FACTORIAL MULTITHREADING BENCHMARK SUITE")
    print("=" * 45)
    print(f"{'Round Index':<15} | {'Time Taken (T) in ns':<25}")
    print("-" * 45)

    # --- Run 10 Rounds ---
    for round_num in range(1, total_rounds + 1):
        # Get Time taken (T) for this round
        t = run_multithreaded_round()
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