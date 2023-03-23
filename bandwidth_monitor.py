from scapy.all import *
import threading
import time
import os

def byte_show(num):
    if num > 1e+9:
        return f"{(num / 1e+9):.2f}{' ' * (8 - len(f'{(num / 1e+9):.2f}'))}GB"
    elif num > 1000000:
        return f"{(num / 1000000):.2f}{' ' * (8 - len(f'{(num / 1000000):.2f}'))}MB"
    elif num > 1000:
        return f"{(num / 1000):.2f}{' ' * (8 - len(f'{(num / 1000):.2f}'))}kB"
    else:
        return f"{(num):.2f}{' ' * (8 - len(f'{(num):.2f}'))}B"

def main():
    try:
        pkts = []

        def _show_usage():
            total_b = 0

            while True:
                bsum = sum(pkts) if pkts else 0
                total_b += bsum
                max_b = max(pkts) if pkts else 0
                min_b = min(pkts) if pkts else 0

                pkts.clear()

                print(f"{byte_show(bsum)}{' ' * (12 - len(byte_show(bsum)))}| MIN: {byte_show(min_b)}{' ' * (12 - len(byte_show(min_b)))}| MAX: {byte_show(max_b)}{' ' * (12 - len(byte_show(max_b)))}| Total: {byte_show(total_b)}"[:os.get_terminal_size()[0] - 1])

                time.sleep(1)

        def _sniffer():
            sniff(filter="", prn=lambda x: pkts.append(len(x)))

        threading.Thread(target=_show_usage, daemon=True).start()
        threading.Thread(target=_sniffer, daemon=True).start()

        input()
    except KeyboardInterrupt:
        return
    
if __name__ == "__main__":
    main()
