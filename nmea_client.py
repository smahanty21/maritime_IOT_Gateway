# nmea_client.py

import asyncio
import websockets


class NMEAClient:
    def __init__(self, uri='ws://localhost:8765'):
        self.uri = uri
        self.current_rot = None
        self.status = "Invalid"

    async def listen(self):
        """
        Connect to WebSocket and listen for incoming NMEA ROT sentences.
        """
        print(f"Connecting to ROT WebSocket: {self.uri}")
        async with websockets.connect(self.uri) as websocket:
            print("Connected to ROT WebSocket")
            while True:
                try:
                    message = await websocket.recv()
                    self.parse_sentence(message)
                except Exception as e:
                    print(f"WebSocket error: {e}")
                    await asyncio.sleep(1)  # retry delay

    def parse_sentence(self, sentence):
        """
        Parse NMEA sentence like: $MGROT,2.0,A*33
        """
        if sentence.startswith('$MGROT'):
            parts = sentence.split(',')
            if len(parts) >= 3:
                try:
                    rot = float(parts[1])
                    status = 'Valid' if parts[2][0] == 'A' else 'Invalid'
                    self.current_rot = rot
                    self.status = status
                    print(f"ROT: {rot}°/min | Status: {status}")
                except ValueError:
                    print(f"Invalid ROT value in sentence: {sentence}")
