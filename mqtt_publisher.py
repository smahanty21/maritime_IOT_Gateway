# mqtt_publisher.py

import paho.mqtt.client as mqtt
from datetime import datetime


class MqttPublisher:
    def __init__(self, client_id="ows-challenge-090725"):
        self.broker = "broker.hivemq.com"
        self.port = 1883
        self.client = mqtt.Client(client_id=client_id)
        self.last_sent = {}  # topic -> last value
        self.last_sent_time = {}  # topic -> timestamp

    def connect(self):
        self.client.will_set("ows-challenge/mv-sinking-boat/status", payload="connection lost", qos=1, retain=True)
        self.client.connect(self.broker, self.port, keepalive=600)
        self.client.loop_start()
        print("Connected to MQTT broker")

    def publish(self, topic, value, status):
        """
        Publish if value differs by threshold or max every 5 min.
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d at %H:%M UTC')
        payload = f"{value}, {status}, {timestamp}"

        last_value = self.last_sent.get(topic)
        last_time = self.last_sent_time.get(topic)

        significant_change = False
        try:
            numeric_value = float(str(value).split()[0])
            numeric_last = float(str(last_value).split()[0]) if last_value else None
            diff = abs(numeric_value - numeric_last) if numeric_last is not None else None
            significant_change = diff is None or diff > 1.0
        except:
            significant_change = True

        now = datetime.utcnow()

        force_publish = False
        if last_time:
            elapsed = (now - last_time).total_seconds()
            if elapsed >= 300:  # 5 min
                force_publish = True

        if significant_change or force_publish:
            self.client.publish(topic, payload)
            print(f"Published: {topic} -> {payload}")
            self.last_sent[topic] = value
            self.last_sent_time[topic] = now
