import subprocess
import sys
import time

def start_pcap_capture(interface, output_file):
    """Start tcpdump to capture traffic on the specified interface"""
    return subprocess.Popen(["sudo", "tcpdump", "-i", interface, "-w", output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_pcap_capture(process):
    """Wait for 5 seconds before stopping tcpdump"""
    time.sleep(5)

    """Stop tcpdump process"""
    process.kill()

def run_nuclei(cve_id, target_ip, pcap_file):
    """Run nuclei template for the specified CVE ID on the target IP"""
    subprocess.run(["nuclei", "-t", cve_id, "-t", target_ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <interface> <target_ip> <cve_list_file>")
        sys.exit(1)

    interface = sys.argv[1]
    target_ip = sys.argv[2]
    cve_list_file = sys.argv[3]

    """Read CVE list from file and iterate over each CVE"""
    with open(cve_list_file, 'r') as file:
        cve_list = file.readlines()

        for cve_id in cve_list:
            cve_id = cve_id.strip()  # Remove leading/trailing whitespace
            print(f"Scanning CVE: {cve_id}")
            pcap_file = f"{cve_id}_capture.pcap"  # Naming pcap file with CVE ID

            """Start pcap capture"""
            pcap_process = start_pcap_capture(interface, pcap_file)

            """Run nuclei template"""
            run_nuclei(cve_id, target_ip, pcap_file)

            """Stop pcap capture"""
            stop_pcap_capture(pcap_process)

if __name__ == "__main__":
    main()