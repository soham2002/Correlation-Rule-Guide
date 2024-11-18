# Wireshark Analysis and SIEM Correlation Rule Development

This guide provides step-by-step instructions on using **Wireshark filters** to analyze a `.pcap` file and determine if a **SIEM correlation rule** can be applied. By identifying patterns, anomalies, or malicious activities, you can create effective detection rules to enhance your network security.

---

## Table of Contents
- [Step 1: Basic Traffic Analysis](#step-1-basic-traffic-analysis)
- [Step 2: Detect Suspicious DNS Activity](#step-2-detect-suspicious-dns-activity)
- [Step 3: Analyze HTTP/HTTPS Traffic](#step-3-analyze-httphttps-traffic)
- [Step 4: Detect Brute Force Attacks](#step-4-detect-brute-force-attacks)
- [Step 5: Analyze ICMP Traffic](#step-5-analyze-icmp-traffic)
- [Step 6: Monitor Suspicious File Transfers](#step-6-monitor-suspicious-file-transfers)
- [Step 7: Check for Anomalous Traffic Patterns](#step-7-check-for-anomalous-traffic-patterns)
- [Step 8: Create SIEM Correlation Rules](#step-8-create-siem-correlation-rules)

---

## Step 1: Basic Traffic Analysis

Use the following filters to establish a baseline and detect deviations:

- **General Protocols**:
  ```plaintext
  tcp or udp or icmp or dns or http
  ```
- **Specific IP Addresses**:
  ```plaintext
  ip.addr == 192.168.1.100
  ip.src == 192.168.1.100
  ip.dst == 10.0.0.1
  ```
- **Ports**:
  ```plaintext
  tcp.port == 80
  tcp.port == 443
  udp.port == 53
  ```
  
## Step 2: Detect Suspicious DNS Activity

Use the following filters to establish a baseline and detect deviations:

- **General Protocols**:
  ```plaintext
  tcp or udp or icmp or dns or http
  ```
  

