# Ping Sweep Tool

This Python script performs a **ping sweep** to check the availability of IP addresses within a specified subnet and range. It supports concurrent pinging using threads, making it efficient for scanning large networks. You can specify the subnet, IP range, and number of threads to control the scan's scope and speed.

## Features
- **Subnet Validation**: Ensures the entered subnet is in a valid format.
- **Concurrent Pinging**: Utilizes threads to ping multiple IPs simultaneously, speeding up the scan.
- **Customizable Parameters**: Specify the subnet, range of IPs, and number of concurrent threads.
- **Progress Bar**: Shows real-time progress using the `tqdm` library.
- **Retry Mechanism**: Retries failed ping attempts for more accurate results.

## Prerequisites

Before running the script, make sure you have **Python 3** installed and the required libraries. The script uses the following third-party libraries:

- `tqdm`: For showing a progress bar during the scan.
- `subprocess`: For running the ping command (part of Python's standard library).
- `concurrent.futures`: For running the ping sweep with threads (part of Python's standard library).

To install the required libraries, run the following command:

```bash
pip install tqdm
```

## Installation

1. **Clone or download the repository**:

   You can either clone the repository (if applicable) or simply download the script file.

2. **Install the required dependencies**:

   Run the following command to install **tqdm**:
   ```bash
   pip install tqdm
   ```

3. **Run the script**:

   Once the dependencies are installed, you can run the script via the command line:

   ```bash
   python ping_sweep.py
   ```

## Usage

When you run the script, you'll be prompted for the following inputs:

- **Subnet**: Enter the base of your subnet (e.g., `192.168.1` or `192.168.144`). The script will append the appropriate range (from 0 to 254) for pinging.
- **Start IP Range**: Specify the starting IP for the sweep (default: 0).
- **End IP Range**: Specify the ending IP for the sweep (default: 254).
- **Number of Concurrent Threads**: Specify how many threads to use for the scan (default: 20). The more threads, the faster the scan will complete.

Example of usage:

```bash
Enter the subnet (default: 192.168.1): 192.168.144
Enter the start IP range (default: 0): 120
Enter the end IP range (default: 254): 130
Enter the number of concurrent threads (default: 20): 10
```

## Example Output

The script will output a progress bar and the status for each IP address:

```bash
Welcome to the Ping Sweep tool!
Usage:
Enter the subnet in the format 'xxx.xxx.xxx.', followed by a range of IPs (0-254).
Specify the number of concurrent threads as desired.
Default subnet is '192.168.1' and default number of threads is 20.
Enter the subnet (default: 192.168.1): 192.168.144
Enter the start IP range (default: 0): 120
Enter the end IP range (default: 254): 130
Enter the number of concurrent threads (default: 20): 10
Pinging: 100%|█████████████████████████████████████████████████████████████████████████| 10/10 [00:10<00:00,  1.01s/IP]
```

After the scan, the script will display a summary of alive and dead hosts in the specified range:

```bash
Pinging:   0%|                                                                                  | 0/10 [00:00<?, ?IP/s]ITS ALIVE! 192.168.1.126
Pinging:  10%|███████▍                                                                  | 1/10 [00:01<00:09,  1.02s/IP]ITS ALIVE! 192.168.1.125
ITS ALIVE! 192.168.1.129
ITS ALIVE! 192.168.1.122
Pinging:  30%|██████████████████████▏                                                   | 3/10 [00:04<00:10,  1.44s/IP]ITS ALIVE! 192.168.1.128
ITS ALIVE! 192.168.1.123
ITS ALIVE! 192.168.1.127
Pinging:  70%|███████████████████████████████████████████████████▊                      | 7/10 [00:04<00:01,  1.83IP/s]ITS ALIVE! 192.168.1.124
ITS ALIVE! 192.168.1.120
Pinging:  80%|███████████████████████████████████████████████████████████▏              | 8/10 [00:10<00:03,  1.50s/IP]ITS ALIVE! 192.168.1.121
Pinging: 100%|█████████████████████████████████████████████████████████████████████████| 10/10 [00:10<00:00,  1.01s/IP]
```

## Troubleshooting

- If you get an error indicating that `tqdm` is not installed, you can manually install it with `pip install tqdm`.
- If the script hangs or runs too slowly, you can try increasing the number of threads (e.g., `50` or `100`).
- Ensure that your network allows ICMP traffic (the type of traffic used by the `ping` command).

## License

This script is open-source and available for use under the MIT License.

