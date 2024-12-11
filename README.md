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
  
---

## Step 2: Detect Suspicious DNS Activity

Analyze DNS traffic for signs of exfiltration, C2 communication, or domain generation algorithms (DGA).

- **All DNS**:
  ```plaintext
  dns
  ```
- **Large DNS Responses (potential data exfiltration)**:
  ```plaintext
  dns and dns.resp.len > 200
  ```
- **Suspicious Domains**:
  ```plaintext
  dns.qry.name contains "example.com"
  dns.qry.name matches "(.*).xyz"
  ```
- **Unanswered DNS Requests:**:
  ```plaintext
  dns.flags.response == 0
  ```
Correlation Rule Insight: Monitor for repeated queries to uncommon domains or DGAs.

---

## Step 3: Analyze HTTP/HTTPS Traffic
Look for signs of data exfiltration, C2 communication, or malicious uploads/downloads.

**HTTP/HTTPS Filters:**
- **HTTP Traffic**:
  ```plaintext
  http
  ```
- **HTTP Non Standard Post**:
  ```plaintext
  http and !(tcp.port == 80 || tcp.port == 443)
  ```
- **HTTP Post Requests**:
  ```plaintext
  http.request.method == "POST"
  ```
- **HTTP Post Request to Non Standard Port**:
  ```plaintext
  http.request.method == "POST" && !(tcp.port == 80 || tcp.port == 443)
  ```
- **Unusual User Agents:**:
  ```plaintext
  http.user_agent contains "curl"
  ```
- **Sensitive Info in HTTP:**:
  ```plaintext
  http contains "password"
  ```
- **Sensitive Info in HTTP:**:
  ```
  tls.handshake.type == 11
  tls.handshake.extensions_server_name contains "malicious.com"
  ```
- **Check for Old TLS(v1.0 or v1.1):**
  ```
  tls.handshake.version <= 0x0302
  ```
  
  Correlation Rule Insight: Set alerts for suspicious POST requests, unusual user agents, or certificate anomalies.
  
---

## Step 4: Detect Brute Force Attacks
Identify repeated failed login attempts that might indicate a brute force attack.

- **Brute Force Filters:**
  - **SSH Authentication Failures:**
    ```
    tcp.port == 22 and ssh
    ```
  - **HTTP Login Attempts:**
    ```
    http.request.uri contains "login"
    http.response.code == 401
    ```
 - **SMB Authentication Failures:**
  ```
  smb2.cmd == 0x0a and smb2.nt_status != 0x00000000
  ```
Correlation Rule Insight: Alert on multiple failed authentication attempts from the same IP within a short timeframe.
  
---

### Step 5: Analyze ICMP Traffic
ICMP traffic may indicate reconnaissance or covert data transfers.
**ICMP Filters:**
- **All ICMP Traffic**:
  ```plaintext
  icmp
  ```
- **Large ICMP Payloads** (potential data exfiltration):
  ```plaintext
  icmp && frame.len > 200
  ```
- **Unusual Ping Patterns:**:
  ```plaintext
  icmp.type == 8 and ip.dst_host != "192.168.1.1"
  ```
  
  Correlation Rule Insight: Detect ICMP traffic with large payloads or frequent pings to multiple destinations.
  
---

### Step 6: Monitor Suspicious File Transfers
Attackers may use protocols like FTP or SMB to transfer files within the network.

**File Transfer Filters:**
- **FTP File Uploads**:
  ```plaintext
  ftp.request.command == "STOR"
  ```
- **SMB File Transfers**:
  ```plaintext
  smb2.cmd == 0x05
  ```
  
Correlation Rule Insight: Set alerts for unusual file transfers to/from sensitive directories or external IPs.
  
---
  
## Step 7: Check for Anomalous Traffic Patterns
Identify deviations from typical network traffic behavior to spot potential threats.

**Anomaly Detection Filters:**
- **Large Packets**:
  ```plaintext
  frame.len > 1500
  ```
- **Uncommon Protocols**:
  ```plaintext
  !(tcp or udp or icmp or dns or http)
  ```
- **Internal to External Traffic**(possible data exfiltration):
  ```plaintext
  ip.src == "10.0.0.0/8" && ip.dst != "10.0.0.0/8"
  ```
  
Correlation Rule Insight: Set alerts for large packets or unexpected protocol usage.

---
  
## Step 7: Check for Anomalous Traffic Patterns
Identify deviations from typical network traffic behavior to spot potential threats.

**Anomaly Detection Filters:**
- **Large Packets**:
  ```plaintext
  frame.len > 1500
  ```
- **Uncommon Protocols**:
  ```plaintext
  !(tcp or udp or icmp or dns or http)
  ```
- **Internal to External Traffic**(possible data exfiltration):
  ```plaintext
  ip.src == "10.0.0.0/8" && ip.dst != "10.0.0.0/8"
  ```
  
Correlation Rule Insight: Set alerts for large packets or unexpected protocol usage.

---

### Step 8: Create SIEM Correlation Rules
Once you've identified suspicious patterns, 
Document them and create SIEM correlation rules.
Define the conditions for a correlation rule in your SIEM system.
Test the rule for accuracy using historical data or simulated traffic.

- **Example Correlation Rule (Elastic SIEM/Kibana)**
  ```
  event.category: "authentication" AND event.outcome: "failure"
  AND source.ip: "192.168.1.10"
  AND event.action: "login"
  ```
- **Example Correlation Rule in Splunk**
  ```
  index=authentication sourcetype=linux_secure ("failed password" OR "authentication failure")
  | stats count by src_ip
  | where count > 10
  ```

