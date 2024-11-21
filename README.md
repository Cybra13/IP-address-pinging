# IP-address-pinging
Tool for pinging multiple ip addresses to test if losing packages
## Usage

To use the IP-address-pinging tool, you need to provide the base IP address, target IP address, and the number of pings. You can do this using the following arguments:

```python
parser = argparse.ArgumentParser("multi_ping.py")
parser.add_argument("-IP", "--ip_address", type=str, help="Base IP address to ping")
parser.add_argument("-T", "--target", type=str, help="Target IP address to ping")
parser.add_argument("-TR", "--target_range", type=str, help="Target IP address range to ping")
parser.add_argument("-C", "--count", type=int, help="Number of pings")
```

### Example

```sh
python multi_ping.py -IP 192.168 -T 1-4 -TR 1-6 -C 10
```

This command will ping the target IP address `192.168.1.1` from the base IP address `192.168.4.6` 10 times.
