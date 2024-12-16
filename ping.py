import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform
import re
from tqdm import tqdm  # For progress bar
import time

# Constants for default values
DEFAULT_SUBNET = "192.168.1"
DEFAULT_START_RANGE = 0
DEFAULT_END_RANGE = 254
DEFAULT_NUM_THREADS = 20
DEFAULT_TIMEOUT = 5  # Default timeout in seconds
DEFAULT_RETRIES = 2  # Number of retries for a ping

# Function to validate subnet format (allowing optional trailing dot)
def is_valid_subnet(subnet):
    # Validates both "192.168.144" or "192.168.144."
    return bool(re.match(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.)?$', subnet))

# Function to perform the ping test with retries
def ping_address(address, retries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT):
    for attempt in range(retries + 1):
        try:
            # Determine the ping command based on the operating system
            if platform.system().lower() == "windows":
                res = subprocess.run(['ping', '-n', '2', address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
            else:
                res = subprocess.run(['ping', '-c', '2', address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)

            # Log and print the raw ping result for debugging
            result = res.stdout.decode()
            logging.debug(f"Raw ping result for {address}: {result}")

            if res.returncode == 0:
                print(f"ITS ALIVE! {address}")  # Directly print the alive status
                return f"ITS ALIVE! {address}"
            else:
                if attempt < retries:
                    time.sleep(1)  # Optional delay between retries
                else:
                    print(f"NOBODY WILL ANSWER THE DOOR! :( {address}")  # Directly print the dead status
                    return f"NOBODY WILL ANSWER THE DOOR! :( {address}"
        except subprocess.TimeoutExpired:
            if attempt < retries:
                time.sleep(1)  # Optional delay between retries
            else:
                print(f"Ping timed out for {address}")  # Directly print timeout message
                return f"Ping timed out for {address}"
        except FileNotFoundError:
            print(f"Ping command not found. Ensure ping is installed: {address}")
            return f"Ping command not found. Ensure ping is installed: {address}"
        except Exception as e:
            print(f"Error pinging {address}: {str(e)}")
            return f"Error pinging {address}: {str(e)}"

# Function to perform a ping sweep
def ping_sweep(subnet, start_range, end_range, num_threads, retries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT):
    # Set up logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

    # Ensure subnet ends with a dot
    if not subnet.endswith('.'):
        subnet += '.'

    # Prepare list of IP addresses to ping
    addresses = [f"{subnet}{i}" for i in range(start_range, end_range)]

    logging.info(f"Pinging IP addresses from {subnet}{start_range} to {subnet}{end_range-1}...")

    # Log generated addresses for debugging
    logging.debug(f"Generated IP addresses: {addresses}")

    results = {"alive": 0, "dead": 0}
    
    # Create a thread pool to ping addresses concurrently
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(ping_address, address, retries, timeout): address for address in addresses}

        # Display progress with tqdm
        for future in tqdm(as_completed(futures), total=len(futures), desc="Pinging", unit="IP"):
            result = future.result()
            logging.info(result)

            if "ITS ALIVE" in result:
                results["alive"] += 1
            else:
                results["dead"] += 1

    return results

# Main function for user input and execution
def main():
    # Help or info message
    print("Welcome to the Ping Sweep tool!")
    print("Usage:")
    print("Enter the subnet in the format 'xxx.xxx.xxx.', followed by a range of IPs (0-254).")
    print("Specify the number of concurrent threads as desired.")
    print(f"Default subnet is '{DEFAULT_SUBNET}' and default number of threads is {DEFAULT_NUM_THREADS}.")

    # Get user input for the subnet and range with validation
    subnet = input("Enter the subnet (default: 192.168.1): ") or DEFAULT_SUBNET
    if not is_valid_subnet(subnet):
        logging.error("Invalid subnet format. Please ensure the format is 'xxx.xxx.xxx.' (e.g., 192.168.1.).")
        return
    
    try:
        start_range = int(input(f"Enter the start IP range (default: {DEFAULT_START_RANGE}): ") or DEFAULT_START_RANGE)
        end_range = int(input(f"Enter the end IP range (default: {DEFAULT_END_RANGE}): ") or DEFAULT_END_RANGE)
        num_threads = int(input(f"Enter the number of concurrent threads (default: {DEFAULT_NUM_THREADS}): ") or DEFAULT_NUM_THREADS)

        # Validate ranges
        if start_range < 0 or end_range > 254 or start_range >= end_range:
            logging.error("Invalid IP range. Please ensure 0 <= start_range < end_range <= 254.")
            return
    except ValueError:
        logging.error("Invalid input. Please enter integer values for the ranges!")
        return

    # Print the start of the scan
    logging.info(f"Starting ping sweep on {subnet}.{start_range}-{subnet}.{end_range-1}")

    # Execute the ping sweep
    results = ping_sweep(subnet, start_range, end_range, num_threads)

    # Summary with percentage
    total_ips = end_range - start_range
    alive_percentage = (results['alive'] / total_ips) * 100
    logging.info("\n--- Ping Sweep Summary ---")
    logging.info(f"Total Alive Hosts: {results['alive']} ({alive_percentage:.2f}%)")
    logging.info(f"Total Dead Hosts: {results['dead']}")
    logging.info("----------------------------")

if __name__ == "__main__":
    main()
