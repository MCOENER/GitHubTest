import time
import psutil
import GPUtil
from threading import Thread
from statistics import mean


def monitor_resources(interval=5, max_samples=100):  # Added max_samples here

    cpu_frequencies = []
    memory_used = []
    used_rams = []

    cpu_count = psutil.cpu_count(logical=True)
    print(f"CPU Count: {cpu_count}")
    ram_info = psutil.virtual_memory()
    total_ram = ram_info.total / (1024 ** 3)
    print(f"Total RAM: {total_ram:.2f} GB")

    sample_count = 0

    try:
        while sample_count < max_samples:
            # CPU
            cpu_freq = psutil.cpu_freq().current
            cpu_frequencies.append(cpu_freq)
          #  print(f"CPU Frequency: {cpu_freq} MHz")

            # RAM information
            ram_info = psutil.virtual_memory()
            used_ram = ram_info.used / (1024 ** 3)
            used_rams.append(used_ram)
            #print(f"Available RAM: {used_ram:.2f} GB")

            # GPU information
            gpus = GPUtil.getGPUs()
            if gpus:
                memory_used_by_gpus = sum(gpu.memoryUsed for gpu in gpus)
                memory_used.append(memory_used_by_gpus)
                # for gpu in gpus:
                #     print(f"GPU {gpu.id} - Name: {gpu.name}")
                #     print(f"  Memory Used: {gpu.memoryUsed:.2f} MB")
                #     print(f"  GPU Load: {gpu.load * 100:.2f}%")
            else:
                memory_used.append(0)

            sample_count += 1
            time.sleep(interval)

        # Calculate max and average values
        print("\nSummary of measurements:")
        print(f"Max CPU Frequency: {max(cpu_frequencies)} MHz")
        print(f"Average CPU Frequency: {mean(cpu_frequencies):.2f} MHz")
        print(f"Max Used RAM: {max(used_rams):.2f} GB")
        print(f"Average Used RAM: {mean(used_rams):.2f} GB")
        print(f"Max GPU Memory Used: {max(memory_used):.2f} MB")
        print(f"Average GPU Memory Used: {mean(memory_used):.2f} MB")

    except KeyboardInterrupt:
        print("Monitoring stopped")

# Start the monitoring thread with the correct arguments
thread = Thread(target=monitor_resources, args=(0.2, 100))  # Now correctly passes two arguments
thread.start()
thread.join()
