import subprocess
import re
from concurrent.futures import ThreadPoolExecutor
import time
import argparse

BASE_IP = "172.31"

def ping_ip(ip, count):
    """
    Ping an IP address a specified number of times and calculate packet loss rate.
    """
    try:
        # Ping command, adjust for your operating system
        # For Windows: ['ping', '-n', str(count), ip]
        # For Linux/Mac: ['ping', '-c', str(count), ip]
        command = ['ping', '-c', str(count), ip]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Extract packet loss rate using regex
        # print(result.stdout)
        loss_rate = re.search(r'(\d+(\.\d+)?)% packet loss', result.stdout)
        if loss_rate:
            # print(f"{ip} - Packet Loss Rate: {float(loss_rate.group(1))}%")
            return ip, float(loss_rate.group(1))
        else:
            return f"{ip} - Failed to retrieve packet loss rate"
    except Exception as e:
        return f"Error pinging {ip}: {e}"

def main():
    parser = argparse.ArgumentParser("multi_ping.py")
    parser.add_argument("-IP", "--ip_address", type=str, default=BASE_IP, help="Base IP address to ping")
    parser.add_argument("-T", "--target", type=str, default="1", help="Target IP address to ping")
    parser.add_argument("-TR", "--target_range", type=str, default="1-6", help="Target IP address range to ping")
    parser.add_argument("-C", "--count", type=int, default=30, help="Number of pings")
    args = parser.parse_args()
    
    base_ip = args.ip_address
    target_ips = args.target.split('-')
    if len(target_ips) >= 1:
        start_ip = int(target_ips[0])
        end_ip = int(target_ips[1]) if len(target_ips) > 1 else start_ip
    count = args.count
    target_range = args.target_range.split('-')
    if len(target_range) >= 1:
        start_tr = int(target_range[0])
        end_tr = int(target_range[1]) if len(target_range) > 1 else start_tr
    ip_list = [f"{base_ip}.{target_ip}.{x}" for target_ip in range(start_ip, end_ip + 1) for x in range(start_tr, end_tr + 1)]
    
    for target_ip in range(start_ip, end_ip + 1):
        print(f"Pinging IPs {base_ip}.{target_ip}.x (x = {start_tr} to {end_tr}), {count} times each...")

    results = []
    
    # Using ThreadPoolExecutor to ping multiple IPs concurrently
    with ThreadPoolExecutor(max_workers=len(ip_list)) as executor:
        results = executor.map(lambda ip: ping_ip(ip, count), ip_list)
    
    # Using a for loop to ping multiple IPs concurrently
    # for ip in ip_list:
    #     print(f"Pinging {ip}...")
    #     results.append(ping_ip(ip, count))
    
    # Print the results
    err = False
    for ip, loss_rate in results:
        if isinstance(loss_rate, float) and loss_rate > 0:
            err = True
            print(f"{ip} has a packet loss rate of {loss_rate}%")
    if not err:
        print("All passed!")
            

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
