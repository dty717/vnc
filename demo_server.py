#!/usr/bin/env python3
"""
Headless MQTT demo server for the VNC device.

Behavior:
- No UI.
- Only purpose: send the auto-run command once, then collect the results.
- Waits for the device reply, state update, and telemetry from the MQTT broker.

Example:
    python3 demo_server.py
    DEVICE_ID=SmartDetect_001 python3 demo_server.py
    MQTT_BROKER=127.0.0.1 MQTT_PORT=1883 python3 demo_server.py
"""

import json
import os
import sys
import threading
import time
from typing import Any, Dict, Optional

try:
    import paho.mqtt.client as mqtt
except Exception as exc:  # pragma: no cover
    raise SystemExit("paho-mqtt is required. Install with: pip install paho-mqtt") from exc

DEVICE_ID = os.getenv("DEVICE_ID", "SmartDetect_demo")
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
RESULT_TIMEOUT = int(os.getenv("RESULT_TIMEOUT", "20"))
LEGACY_TOPIC = os.getenv("LEGACY_TOPIC", f"device/wq/{DEVICE_ID}")
COMMAND_TOPIC = os.getenv("COMMAND_TOPIC", f"vnc/{DEVICE_ID}/command")
STATE_TOPIC = os.getenv("STATE_TOPIC", f"vnc/{DEVICE_ID}/state")
TELEMETRY_TOPIC = os.getenv("TELEMETRY_TOPIC", f"vnc/{DEVICE_ID}/telemetry")


class DemoServer:
    def __init__(self):
        self.result_lock = threading.Lock()
        self.result = {
            "reply": None,
            "state": None,
            "telemetry": None,
        }
        self._done = threading.Event()

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"demo_server_{DEVICE_ID}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc != 0:
            print(f"[demo] MQTT connect failed: rc={rc}")
            return

        print(f"[demo] connected to {BROKER}:{PORT}")
        client.subscribe(COMMAND_TOPIC, qos=1)
        client.subscribe(STATE_TOPIC, qos=1)
        client.subscribe(TELEMETRY_TOPIC, qos=1)
        client.subscribe(LEGACY_TOPIC, qos=1)
        print(f"[demo] subscribed to: {COMMAND_TOPIC}, {STATE_TOPIC}, {TELEMETRY_TOPIC}, {LEGACY_TOPIC}")

    def on_message(self, client, userdata, message):
        try:
            payload = message.payload.decode("utf-8")
            obj = json.loads(payload)
        except Exception:
            print(f"[demo] non-json payload on {message.topic}: {message.payload!r}")
            return

        if not isinstance(obj, dict):
            return

        print(f"[demo] <- {message.topic}: {json.dumps(obj, ensure_ascii=False, sort_keys=True)}")

        with self.result_lock:
            if message.topic in (COMMAND_TOPIC, LEGACY_TOPIC):
                self.result["reply"] = obj
            elif message.topic == STATE_TOPIC:
                self.result["state"] = obj
            elif message.topic == TELEMETRY_TOPIC:
                self.result["telemetry"] = obj

        if obj.get("type") == "reply" or obj.get("cmd") == "operation":
            self._done.set()

    def publish_auto_run(self):
        command = {"cmd": "operation", "action": "start"}
        print(f"[demo] -> {COMMAND_TOPIC}: {json.dumps(command, ensure_ascii=False)}")
        self.client.publish(COMMAND_TOPIC, json.dumps(command), qos=1)

    def print_summary(self):
        print("\n=== Demo result summary ===")
        for key in ("reply", "state", "telemetry"):
            print(f"{key}: {json.dumps(self.result[key], ensure_ascii=False, sort_keys=True)}")

        if self.result["reply"]:
            code = self.result["reply"].get("code")
            message = self.result["reply"].get("message")
            print(f"Auto run command result: code={code}, message={message}")

    def run(self):
        self.client.connect(BROKER, PORT, keepalive=60)
        self.client.loop_start()

        try:
            self.publish_auto_run()
            if not self._done.wait(timeout=RESULT_TIMEOUT):
                print(f"[demo] no result returned within {RESULT_TIMEOUT} seconds")
            self.print_summary()
        finally:
            self.client.loop_stop()
            self.client.disconnect()


def main():
    server = DemoServer()
    try:
        server.run()
        return 0
    except KeyboardInterrupt:
        print("[demo] interrupted by user")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
