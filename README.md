# SNMP Monitoring System
An end-to-end observability stack for real-time hardware monitoring using a custom SNMP agent, Telegraf, InfluxDB, and Grafana.
This project bridges local hardware telemetry (CPU, RAM, GPU, etc.) into SNMP, making it compatible with enterprise monitoring tools and modern time-series dashboards.

## Overview
The system collects hardware metrics from a local machine and exposes them through SNMP for centralized monitoring and visualization.
### Key Features
-  Custom SNMP agent for hardware telemetry


- Near real-time monitoring (1-second resolution)


- Grafana dashboards for visualization


- InfluxDB v2 for time-series storage


- Telegram alerts integration



## Architecture
The monitoring pipeline consists of four layers:
### Data Acquisition


-Hardware metrics are fetched from:  http://localhost:8085/data.json


- Provided by Hardware Monitor Web Server


### Protocol Bridge (Custom SNMP Agent)


- Python-based SNMP agent


- Converts JSON → SNMP OIDs


- Uses custom enterprise tree:  1.3.6.1.4.1.12345


### Collection Layer


Telegraf polls SNMP agents every second


### Storage & Visualization


InfluxDB v2 (storage)


Grafana (dashboards)



## Repository Structure
- /agent        → Custom SNMP agent 
- /collector    → Telegraf configuration
- /dashboard_examples         →  screenshots

## Installation
### Prerequisites

#### Agent
- Python 3.9+


- Hardware Monitor (with Web Server enabled)

#### Server


- Telegraf


- InfluxDB v2




### Enable Hardware Monitor API
Make sure your hardware monitor is running: http://localhost:8085/data.json

 ## SNMP Agent Setup
You have two options to run the agent:
 ### Option 1: Run Precompiled Agent (Recommended)
- If you include agenteSNMP.exe:

- Run: agenteSNMP.exe

### Option 2: Run Python Agent
- Install dependencies

- Run the agent:


` python agent.py `

### Agent Behavior
- Fetches hardware data every second


- Exposes SNMP UDP port 162



## Available Metrics (OID Tree)
| Component |	Metric	| OID	| Unit |
|------------|-------------|-----------------------|-------|
| CPU	 | Temperature	| 1.3.6.1.4.1.12345.1.0	| °C |
| CPU	| Power	| 1.3.6.1.4.1.12345.1.1	| Watts |
| CPU	| Load	| 1.3.6.1.4.1.12345.1.2	| % |
| RAM	| Load	| 1.3.6.1.4.1.12345.1.3	| % |
| GPU	| Temperature	| 1.3.6.1.4.1.12345.1.4	| °C |
| GPU	| Power	| 1.3.6.1.4.1.12345.1.5	| Watts |


## Telegraf Configuration

This is an example of part of the Telegraf configuration. The fields need to be filled in with the appropriate values.
```
[[inputs.snmp]] 
  agents = ["udp://127.0.0.1:162"]
  version = 2 
  community = "public" 
  interval = "1s"
```

```
[[outputs.influxdb_v2]] 
  urls = ["${INFLUX_URL}"] 
  token = "${INFLUX_TOKEN}" 
  organization = "${INFLUX_ORG}" 
  bucket = "${INFLUX_BUCKET}"
```
```
[[inputs.snmp]]
   agents = ["${REMOTE_AGENT_IP}:162"]
   name = "hardware_telemetry"
   timeout = "1s"
   version = 2
   community = "${SNMP_COMMUNITY}"

  [[inputs.snmp.field]]
      name = "Temperatura CPU"
      oid = "1.3.6.1.4.1.12345.1.0"

  [[inputs.snmp.field]]
      name = "Potencia CPU"
      oid = "1.3.6.1.4.1.12345.1.1"
```

### Run Telegraf
` telegraf --config telegraf.conf `

## Grafana Dashboard
Connect Grafana to InfluxDB


Configure dashboards and the telegram connection with the GUI interface




## Security Notes
Sensitive data removed from configs


Use environment variables:

 INFLUX_TOKEN
INFLUX_ORG
INFLUX_BUCKET


Avoid exposing SNMP publicly



## Telegram Alerts 
Include:
- Telegram Bot integration


- Real-time alerts


- Mobile notifications






## Screenshots
(See /docs for some example of dashboards)


## License
MIT License
