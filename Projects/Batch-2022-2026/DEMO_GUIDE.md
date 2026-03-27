# DDoS Detection — Demo Guide & Test Case Explanation

This document explains the purpose of the project, how it works in real-time, what each test case means, and how to present it during a demo or viva.

---

## Purpose of the Project

### The Problem It Solves

In a **Software-Defined Network (SDN)**, there is a central **SDN Controller** (the brain) that manages all network switches. This is powerful but creates a single point of failure:

```
                    +------------------+
                    |  SDN Controller   |  <-- If this gets overwhelmed,
                    |   (The Brain)     |      the ENTIRE network dies
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
        +-----------+  +-----------+  +-----------+
        | Switch 1  |  | Switch 4  |  | Switch 7  |
        +-----------+  +-----------+  +-----------+
              |              |              |
         Computers      Servers        Devices
```

A **DDoS attack** (Distributed Denial of Service) floods this network with millions of fake packets. The controller can't handle the volume, legitimate users get blocked, and services crash.

**This project's purpose:** Detect DDoS attacks in real-time by analyzing network traffic patterns using Machine Learning, so administrators can take action before the network goes down.

---

## How It Works in Real-Time (Production Scenario)

```
Three Ways to Feed Data into the System:

  +----------------+
  | 1. CSV Upload  |----+
  | (Upload .csv)  |    |
  +----------------+    |
                        |    +--------------+    +------------+
  +----------------+    +--->|  This System |--->|  Dashboard |
  | 2. API Push    |----+--->|  (ML Model)  |    |  (WebSocket|
  | (POST /api)    |    |    +--------------+    |   Live)    |
  +----------------+    |           |            +------------+
                        |    Classifies:
  +----------------+    |    DDoS or Normal
  | 3. Poller      |----+           |
  | (Pull from URL)|         +------v------+
  +----------------+         | ALERT!      |
                             | Store in DB |
                             | Suggest fix |
                             +-------------+

Real Deployment (API Push or Poller):

  Attacker --+
  Attacker --+    +----------+    +---------+    +---------+    +-----------+
  Attacker --+--->|   SDN    |--->|  SDN    |--->|  This   |--->| Dashboard |
  Normal   --+    | Switches |    |Controller|   | System  |    | (Admin)   |
  Normal   --+    +----------+    +---------+    +---------+    +-----------+
                                  REST API        ML Model      WebSocket
                                  (Push/Poll)     Predicts      Live Updates
```

**Step-by-step real-time flow:**

| Step | What Happens | Where in the Project |
|---|---|---|
| 1 | SDN switches collect flow statistics every few seconds | The `dataset_sdn.csv` is this real data from an SDN testbed |
| 2 | The system receives data via 3 methods: CSV upload, API push, or endpoint polling | Dashboard has tabbed interface for all 3 input methods |
| 3 | The system reads 13 features from each flow (pktcount, bytecount, pktrate, etc.) | The prediction form on `/predict` takes these 13 values |
| 4 | The Random Forest model classifies: DDoS (1) or Normal (0) | `model.predict([input_data])` in `app.py` |
| 5 | Result is stored in SQLite database | `predictions` table stores every classification |
| 6 | Dashboard updates instantly via WebSocket | `/dashboard` with Flask-SocketIO — no polling, instant updates |
| 7 | Suggestions page gives actionable mitigation steps | `/suggestion` shows red alerts for DDoS, green tips for normal |

---

## Real-World Use Case Example

**Scenario:** A bank's SDN network is under attack.

**Without this system:**
Network admin notices the banking website is slow. Checks logs manually. Takes 30 minutes to identify it's a DDoS. By then, thousands of customers can't access their accounts.

**With this system:**
1. SDN controller pushes flow data via API (`POST /api/predict`) or system polls the controller endpoint
2. The ML model analyzes each flow in milliseconds
3. Dashboard updates instantly via WebSocket: "DDoS Detected — 15 attacks in last minute"
4. Pie chart shows 80% attack traffic vs 20% normal
5. Line chart shows the exact moment attacks started
6. For offline analysis, admin uploads captured traffic as CSV — system processes row by row
7. Suggestions page says: "Apply rate-limiting, blacklist suspicious IPs, enable deep packet inspection"
8. Admin takes action within seconds, not minutes

---

## What Each Page Represents in Real-Time Use

| Page | Real-Time Purpose | Who Uses It |
|---|---|---|
| **Home** | Entry point — explains what the system does | New users / management |
| **Register/Login** | Each network admin has their own account | Multiple analysts in a team |
| **Prediction** | Manually analyze a suspicious flow (paste values from switch logs) | Network engineer investigating an alert |
| **Dashboard** | Live monitoring screen with 3 data input methods — would be on a wall display in a NOC | Security team watches this 24/7 |
| **CSV Upload** | Upload bulk traffic data from switch exports or pcap conversions | Analyst reviewing captured traffic |
| **API Push** | External systems send flow data in real-time via REST API | SDN controller integration script |
| **Endpoint Poller** | System pulls data from external monitoring endpoints | Connecting to existing monitoring infrastructure |
| **Simulation** | Test the system with random traffic to verify it's working | Before deploying to production |
| **Model Info** | Prove to management/auditors the model is reliable (99.39% accuracy) | During audits, compliance reviews |
| **Suggestions** | Actionable steps — what to do RIGHT NOW based on the latest detection | Admin who needs to respond to an attack |

---

## Why These Specific 13 Features?

These are real metrics that every SDN OpenFlow switch collects:

| Feature | Real-Time Meaning | Why It Matters for DDoS |
|---|---|---|
| **switch** | Which physical switch in the network | Attacks may target specific switches |
| **pktcount** | How many packets flowed through | DDoS = massive packet count in short time |
| **bytecount** | Total data volume | DDoS floods with huge data volume |
| **dur** | How long the flow lasted | Short burst = likely attack |
| **dur_nsec** | Precise duration in nanoseconds | Fine-grained timing analysis |
| **flows** | Number of concurrent connections | DDoS uses few flows but high volume per flow |
| **pktrate** | Packets per second | Normal traffic has steady rate; DDoS causes 0 (controller overwhelmed) |
| **Pairflow** | Two-way communication flows | Normal has paired flows; DDoS is one-directional |
| **port_no** | Which switch port | Identifies which physical link is under attack |
| **tx_bytes** | Bytes sent out | High tx + low rx = flooding |
| **rx_bytes** | Bytes received | If tx >> rx, it's asymmetric (attack pattern) |
| **tx_kbps** | Sending speed | Helps identify bandwidth consumption |
| **rx_kbps** | Receiving speed | Combined with tx_kbps shows traffic direction |

---

## How the Model Distinguishes DDoS from Normal

The model learned these patterns from 104,345 real SDN traffic samples:

**DDoS Pattern (what an attack looks like):**
```
+---------------------------------------------------+
|  HIGH bytecount    (millions of bytes)            |
|  SHORT duration    (seconds, not minutes)         |
|  ZERO pktrate      (controller overwhelmed)       |
|  ZERO tx_kbps/rx_kbps (bandwidth saturated)       |
|  FEW flows         (2-3, not many connections)    |
|  ASYMMETRIC tx/rx  (sending >> receiving)         |
|                                                   |
|  Think: Fire hose aimed at a single point         |
+---------------------------------------------------+
```

**Normal Pattern (what legitimate traffic looks like):**
```
+---------------------------------------------------+
|  PROPORTIONAL bytecount to duration               |
|  ACTIVE pktrate    (300-500 packets/sec)          |
|  LONGER duration   (minutes, sustained)           |
|  BALANCED tx/rx    (two-way conversation)         |
|  ACTIVE bandwidth  (tx_kbps, rx_kbps > 0)        |
|                                                   |
|  Think: Normal phone conversation, both talking   |
+---------------------------------------------------+
```

---

## Test Case Explanations

### Test Case 1: DDoS Attack Detection

**Input values:**

| Field | Value | What this means |
|---|---|---|
| switch | 1 | Traffic coming from switch #1 in SDN network |
| pktcount | 4777 | ~4.8K packets observed |
| **bytecount** | **5,092,282** | **~5 MB of data — this is the red flag** |
| dur | 10 | Only 10 seconds duration |
| dur_nsec | 711000000 | Nanosecond precision of duration |
| flows | 3 | Only 3 active flows |
| **pktrate** | **0** | **Zero packet rate — abnormal** |
| Pairflow | 0 | No paired bidirectional flows |
| port_no | 2 | Switch port 2 |
| tx_bytes | 3753 | Very low transmitted bytes |
| rx_bytes | 1332 | Very low received bytes |
| tx_kbps | 0 | Zero transmission rate |
| rx_kbps | 0 | Zero receive rate |

**Expected Result:** `DDoS Attack Detected`

**How to explain in demo:**
"Look at the pattern — 5 million bytes were pushed through in just 10 seconds, but the pktrate and bandwidth (tx_kbps, rx_kbps) are showing zero. This is a classic DDoS flood signature — massive volume of data is being dumped in a short burst with very few flows (only 3). In normal traffic, you'd see proportional packet rates and bandwidth. The zero values here mean the SDN controller is being overwhelmed and can't compute statistics properly — that's exactly what happens during a volumetric DDoS attack."

**Key indicators:** High bytecount + short duration + zero pktrate/kbps = **flood attack**

---

### Test Case 2: Normal Traffic

**Input values:**

| Field | Value | What this means |
|---|---|---|
| switch | 1 | Same switch as Test Case 1 |
| pktcount | 45304 | ~45K packets — much higher |
| bytecount | 48,294,064 | ~48 MB — high but over longer time |
| **dur** | **100** | **100 seconds — sustained connection** |
| dur_nsec | 716000000 | Nanosecond precision |
| flows | 3 | 3 active flows |
| **pktrate** | **451** | **451 packets/sec — healthy, active rate** |
| Pairflow | 0 | No paired flows |
| port_no | 3 | Switch port 3 |
| **tx_bytes** | **143,928,631** | **~144 MB transmitted — large but legitimate** |
| rx_bytes | 3917 | Low received bytes |
| tx_kbps | 0 | Zero kbps |
| rx_kbps | 0 | Zero kbps |

**Expected Result:** `Normal Traffic`

**How to explain in demo:**
"Even though the byte count is high (48 MB), notice the key difference from Test Case 1 — the duration is 100 seconds (not 10) and the pktrate is 451 packets/second. This means traffic is flowing steadily over time, not in a sudden burst. The high tx_bytes (144 MB) with a sustained packet rate indicates a legitimate bulk data transfer — like downloading a large file or streaming. The model learned that consistent packet rate + longer duration = normal behavior, even with high data volume."

**Key indicators:** Active pktrate (451) + longer duration (100s) = **legitimate traffic**

---

### Test Case 3: DDoS Attack (Multiple Switches)

**Input values:**

| Field | Value | Key point |
|---|---|---|
| **switch** | **7** | **Different switch — attack spreads across network** |
| pktcount | 12,146 | ~12K packets |
| **bytecount** | **12,947,636** | **~13 MB in short time** |
| **dur** | **27** | **Only 27 seconds** |
| flows | **2** | **Only 2 flows — very few** |
| **pktrate** | **0** | **Zero again — abnormal** |
| tx_bytes | 3185 | Very low tx |
| rx_bytes | 3059 | Very low rx |
| tx_kbps | 0 | Zero bandwidth |
| rx_kbps | 0 | Zero bandwidth |

**Expected Result:** `DDoS Attack Detected`

**How to explain in demo:**
"This test proves the model works across different switches in the SDN topology — not just switch 1. The attack pattern is the same: 13 MB pushed through in just 27 seconds with only 2 flows and zero pktrate/bandwidth readings. In a real SDN environment, DDoS attacks target multiple switches to overwhelm the controller. The model detects this because it learned the pattern — high byte volume + few flows + zero rate metrics = attack — regardless of which switch it occurs on."

**Key indicators:** High bytecount + only 2 flows + zero pktrate on switch 7 = **distributed attack**

---

### Test Case 4: Normal Traffic (Different Switch)

**Input values:**

| Field | Value | Key point |
|---|---|---|
| **switch** | **4** | **Different switch — model works everywhere** |
| pktcount | 19,138 | ~19K packets |
| bytecount | 20,401,108 | ~20 MB |
| dur | 41 | 41 seconds |
| **pktrate** | **446** | **Active packet rate — healthy** |
| port_no | 4 | Switch port 4 |
| **tx_bytes** | **2882** | **Balanced with rx** |
| **rx_bytes** | **2924** | **Balanced with tx** |

**Expected Result:** `Normal Traffic`

**How to explain in demo:**
"Even with 20 MB of data, the model classifies this as normal. Why? Three reasons: (1) pktrate is 446 — traffic is flowing actively, not dumped all at once, (2) tx_bytes and rx_bytes are nearly balanced (2882 vs 2924) — meaning it's a two-way conversation, not one-way flooding, (3) duration is moderate at 41 seconds. This proves the model correctly identifies normal traffic on switch 4 — it's not biased toward any specific switch."

**Key indicators:** Active pktrate (446) + balanced tx/rx + moderate duration = **normal**

---

### Test Case 5: DDoS Attack (High Volume)

**Input values:**

| Field | Value | Key point |
|---|---|---|
| **pktcount** | **130,634** | **130K+ packets — extremely high** |
| **bytecount** | **135,522,132** | **135 MB — massive volume** |
| dur | 650 | 650 seconds (~11 minutes) |
| pktrate | 0 | Zero rate |
| **tx_bytes** | **135,529,018** | **135 MB transmitted** |
| **rx_bytes** | **65,390** | **Only 65 KB received** |

**Expected Result:** `DDoS Attack Detected`

**How to explain in demo:**
"This is the most obvious DDoS case. Look at the asymmetry — tx_bytes is 135 MB but rx_bytes is only 65 KB. That's a 2000:1 ratio. In normal two-way communication, you'd see somewhat balanced tx and rx. This massive one-directional data flow means something is flooding the network. Even though the duration is long (650 seconds), the packet count is 130K+ with zero pktrate, which means the SDN controller metrics are broken — a clear sign of an ongoing sustained DDoS attack. This is what we call a 'volumetric attack' — the goal is to consume all available bandwidth."

**Key indicators:** tx_bytes >> rx_bytes (2000:1 ratio) + zero pktrate + 130K packets = **volumetric DDoS flood**

---

### Test Case 6: Dashboard, 3 Data Input Methods & Simulation

**What it tests:** The dashboard visualization, 3 data input methods (CSV Upload, API Push, Endpoint Poller), simulation, and WebSocket live updates.

After running Test Cases 1-5, go to `/dashboard`. You'll see:

| Component | What It Shows | How to Explain |
|---|---|---|
| **Stat Cards** | Total: 5, DDoS: 3, Normal: 2, Users: 1 | "Real-time counters showing all predictions stored in SQLite database — 3 attacks detected, 2 normal" |
| **Pie Chart** | 60% DDoS, 40% Normal | "Visual distribution of attack vs normal traffic — in our tests, 3 out of 5 were attacks" |
| **Line Chart** | rx_kbps over time with colored dots | "Traffic timeline — red dots are DDoS predictions, green dots are normal. This helps network admins spot attack patterns over time" |
| **Recent Table** | 5 rows with user, result, source, timestamp | "Full audit trail — who ran which prediction, when, and from what source (manual, simulation, csv, api, or poller)" |
| **Data Input Tabs** | 3 tabs for CSV Upload, API Push, Endpoint Poller | "Three ways to feed data into the system — upload a CSV file, push via REST API, or pull from an external endpoint" |
| **Simulation Panel** | Enter 5, click Run | "This generates 5 random network packets with realistic SDN values, classifies each one, and stores results" |
| **WebSocket** | Instant updates, no polling | "The dashboard uses Flask-SocketIO for instant live updates — no page reload needed. Open two browser tabs and both update simultaneously" |

**CSV Upload Demo Steps:**
1. Click the **Upload CSV** tab
2. Select `dataset_sdn.csv` from the project folder
3. Set max rows to **20** and speed to **1s / row**
4. Click **Upload & Analyze** — the page does NOT reload (AJAX upload)
5. Watch the progress bar fill row by row, stats and charts update live
6. Each row shows DDoS (red) or Normal (green) classification in real-time
7. Click **Stop** mid-way to demonstrate graceful stop

**API Push Demo Steps:**
1. Click the **API Push** tab — shows curl and Python examples
2. Open a terminal and run the curl command shown on the page
3. Dashboard updates instantly — no page reload
4. Show the batch endpoint for processing multiple records at once

**Endpoint Poller Demo Steps:**
1. Click the **Endpoint Poller** tab
2. Enter any URL that returns JSON with the 13 SDN fields
3. Set interval to 5s, max polls to 10
4. Click **Start Polling** — system fetches and classifies data every 5 seconds
5. Click **Stop** to stop polling

---

### Test Case 7: Model Info Page

**What it tests:** Can the user understand how good the model is?

| Metric | Value | What to Say in Demo |
|---|---|---|
| **Accuracy** | 99.39% | "Out of 20,869 test samples, the model correctly classified 99.39% — only 127 mistakes out of 20,869" |
| **Precision** | 99.40% | "When the model says 'DDoS', it's right 99.4% of the time — very few false alarms" |
| **Recall** | 99.39% | "The model catches 99.39% of actual attacks — it misses very few real DDoS events" |
| **F1 Score** | 99.39% | "F1 is the balance between precision and recall — 99.39% means both are excellent" |

**Confusion Matrix explanation:**
Out of 20,869 test samples:
- **10,356** DDoS attacks were correctly detected (True Positive)
- **10,386** normal packets were correctly identified (True Negative)
- **72** normal packets were wrongly flagged as DDoS (False Positive — false alarm)
- **55** DDoS attacks were missed (False Negative — this is the dangerous one)

So the model only missed 55 real attacks and gave 72 false alarms out of 20,869 samples — that's extremely reliable.

**Model Comparison:**

| Algorithm | Accuracy | Notes |
|---|---|---|
| **Random Forest** | **99.39%** | Best model — uses multiple decision trees and votes on the answer |
| Decision Tree | 99.25% | Single tree — almost as good but less robust |
| K-Nearest Neighbors | 92.65% | Compares to nearby data points — decent but slower |
| Gradient Boosting | 95.96% | Builds trees sequentially — good but slower to train |
| SVM | 99.39% | Finds optimal boundary — tied with RF but slower |

We chose Random Forest because it's fast, accurate, and handles the 13 features well without overfitting.

**Feature Importance (top 5 = 72% of detection):**

| Rank | Feature | Importance | What It Means |
|---|---|---|---|
| 1 | bytecount | 18.2% | Total data volume is the biggest signal |
| 2 | pktcount | 16.5% | Number of packets is second |
| 3 | tx_bytes | 14.2% | How much data was sent |
| 4 | rx_bytes | 13.8% | How much data was received |
| 5 | pktrate | 9.8% | Packet rate |

The model basically looks at: "How much data, how many packets, and how fast?" — which aligns with how network engineers manually detect DDoS.

---

### Test Case 8: Suggestions Based on DB

**What it tests:** Context-aware security recommendations.

**After DDoS prediction (Test Cases 1, 3, or 5):**
The system shows red alert mitigation steps:
- Monitor abnormal traffic spikes and alert your team immediately
- Use IP blacklisting to restrict suspicious sources
- Apply rate-limiting policies
- Enable deep packet inspection for sensitive applications
- Consider geo-blocking for known malicious regions

**After Normal prediction (Test Cases 2 or 4):**
The system shows green maintenance tips:
- Network appears stable — continue monitoring
- Maintain your firewall and IDS configurations
- Keep security patches up to date
- Schedule regular vulnerability scans
- Educate users on phishing and social engineering

The suggestions are database-backed — it queries the most recent prediction for the logged-in user from SQLite and changes recommendations accordingly. This simulates how a real security dashboard would give actionable advice based on current network status.

---

## Quick Summary Table for Demo

| Test | Input Pattern | Result | Proves |
|---|---|---|---|
| **TC1** | High bytes, short time, 0 pktrate | **DDoS** | Model detects volumetric floods |
| **TC2** | Active pktrate, long duration | **Normal** | Model recognizes steady traffic |
| **TC3** | Same DDoS pattern on switch 7 | **DDoS** | Works across different switches |
| **TC4** | Balanced tx/rx, active rate on switch 4 | **Normal** | Not biased to specific switches |
| **TC5** | tx >> rx (2000:1), 130K packets | **DDoS** | Detects asymmetric flooding |
| **TC6** | Dashboard + CSV upload + API push + poller + simulation | **Visual** | Real-time monitoring with 3 data input methods + WebSocket |
| **TC7** | Model metrics page | **99.39%** | Model is highly accurate |
| **TC8** | Suggestions change per result | **Adaptive** | Context-aware recommendations |

---

## Demo Script (What to Say When Presenting)

"This project addresses a critical security challenge in Software-Defined Networks. In SDN, a single controller manages all network switches — which makes it efficient but also a target for DDoS attacks.

We built a Machine Learning-based detection system using a Random Forest classifier trained on 104,000+ real SDN traffic samples with 99.39% accuracy.

The system takes 13 network flow features — like packet count, byte count, packet rate, and bandwidth — and classifies traffic as either DDoS or Normal in real-time.

Let me demonstrate: [run Test Case 1] — see how 5 MB in 10 seconds with zero packet rate is detected as DDoS. Now [run Test Case 2] — same switch, but with active packet rate over 100 seconds is correctly classified as Normal.

Now let me show the three ways to feed data into the system:

First, CSV Upload — [upload dataset_sdn.csv with 20 rows at 1s speed]. Watch the dashboard update row by row via WebSocket. The progress bar fills up, stat cards change, pie chart animates, and the line chart grows — all in real-time without any page reload.

Second, the REST API — external systems like SDN controllers can push data directly. [run curl command from the API Push tab]. See the dashboard update instantly.

Third, the Endpoint Poller — the system can pull data from any external monitoring endpoint at regular intervals. In production, this would connect to your SDN controller's REST API.

The model info page proves our 99.39% accuracy with confusion matrix, and the suggestions page gives actionable mitigation steps based on the latest detection.

In a real deployment, you would use either the API Push (SDN controller sends data to us) or the Endpoint Poller (we pull from the controller) to achieve continuous real-time monitoring — giving network administrators instant visibility into attacks, reducing response time from minutes to seconds."
