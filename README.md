# Maritime IoT Gateway — Code Challenge

This project is my solution for providing the below data from sensor to MQTT. 

● 4 temperature sensors for the temperature of the luffing winch motors.
● A Rate of turn (ROT) sensor which indicates the speed of the crane’s boom moving around its
vertical axis.
● In addition to collecting the data, sends it towards the cloud, using MQTT (with the application
being the client)
 
It demonstrates how an IoT Gateway can collect data from Modbus TCP temperature sensors and a NMEA Rate of Turn (ROT) sensor and forward that data to a cloud MQTT broker.

---

## **Project Structure**
maritime-iot-gateway/
├── main.py # Entry point
├── modbus_client.py # Handles Modbus TCP temperature sensor readings
├── nmea_client.py # Handles ROT sensor readings via WebSocket
├── mqtt_publisher.py # Publishes measurements to MQTT broker
├── requirements.txt # Python dependencies
├── .gitignore # Git exclusions
└── README.md # This file
Create & activate a virtual environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate

4.Install dependencies:

pip install -r requirements.txt

5 Start the simulation server in a separate terminal:

python crane_simulation.py

6- run the IoT Gateway:
In the project folder:


python main.py
How It Works
 Temperature sensors (Modbus TCP)

Connects to local Modbus server (127.0.0.1:8889).

Reads 4 luffing winch motor temperatures every 2 seconds.



 ROT sensor (NMEA over WebSocket)

Connects to local WebSocket server (simulator).

Parses NMEA sentences for valid Rate of Turn values.

 MQTT publishing

Publishes temperature & ROT data to broker.hivemq.com.

Uses the topic structure required by the challenge.

Only publishes if values change by more than 1°C or 1°/min, or at least once every 5 minutes.

Includes timestamps in UTC.

Sends LWT (Last Will & Testament) on each topic to report unexpected disconnects.