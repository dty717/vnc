import os
import json
import time
import threading
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except Exception as exc:  # pragma: no cover
    raise RuntimeError("paho-mqtt is required. Install with: pip install paho-mqtt") from exc

try:
    from config.config import deviceID
except Exception:  # pragma: no cover
    deviceID = os.environ.get("DEVICE_ID", "device_unknown")

from service.device import (
    deviceInfo,
    deviceController,
    write_single_register,
    write_single_coil,
    write_multiple_registers,
)

MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_USER = os.environ.get("MQTT_USER", "")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "")
MQTT_PUBLISH_INTERVAL = int(os.environ.get("MQTT_PUBLISH_INTERVAL", "10"))

BASE_TOPIC = f"vnc/{deviceID}"
TELEMETRY_TOPIC = f"{BASE_TOPIC}/telemetry"
STATE_TOPIC = f"{BASE_TOPIC}/state"
COMMAND_TOPIC = f"{BASE_TOPIC}/command"


def utc_now_iso():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


class MqttDeviceClient:
    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD):
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.stop_event = threading.Event()
        self.client = mqtt.Client(client_id=f"vnc-device-{deviceID}")
        if self.user:
            self.client.username_pw_set(self.user, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT] connected rc={rc}")
        client.subscribe(COMMAND_TOPIC, qos=1)

    def on_disconnect(self, client, userdata, rc):
        print(f"[MQTT] disconnected rc={rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode("utf-8")
            data = json.loads(payload)
        except Exception as exc:
            print("[MQTT] invalid payload:", exc)
            return

        cmd = data.get("cmd")
        print(f"[MQTT] command received: {cmd} payload={data}")

        try:
            if cmd == "ping":
                client.publish(
                    STATE_TOPIC,
                    json.dumps({
                        "deviceID": deviceID,
                        "timestamp": utc_now_iso(),
                        "type": "pong",
                        "status": "ok"
                    }),
                    qos=1,
                )
                return

            if cmd == "write_register":
                addr = int(data.get("addr", 0))
                value = int(data.get("value", 0))
                write_single_register(
                    addr,
                    value,
                    lambda rec: print("[MQTT] write_register ok:", rec),
                    repeatTimes=0,
                    needMesBox=False,
                )
                return

            if cmd == "write_coil":
                addr = int(data.get("addr", 0))
                value = bool(data.get("value", False))
                write_single_coil(
                    addr,
                    value,
                    lambda rec: print("[MQTT] write_coil ok:", rec),
                    repeatTimes=0,
                    needMesBox=False,
                )
                return

            if cmd == "write_multiple":
                addr = int(data.get("addr", 0))
                values = [int(v) for v in data.get("values", [])]
                write_multiple_registers(
                    addr,
                    values,
                    lambda rec: print("[MQTT] write_multiple ok:", rec),
                    repeatTimes=0,
                    needMesBox=False,
                )
                return

            if cmd == "get_status":
                self.publish_state()
                self.publish_telemetry()
                return

            print(f"[MQTT] unknown command: {cmd}")
        except Exception as exc:
            print(f"[MQTT] command error: {exc}")

    def connect(self):
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()

    def disconnect(self):
        self.stop_event.set()
        try:
            self.client.loop_stop()
        except Exception:
            pass
        try:
            self.client.disconnect()
        except Exception:
            pass

    def publish_telemetry(self):
        payload = {
            "deviceID": deviceID,
            "timestamp": utc_now_iso(),
            "PH": getattr(deviceInfo, "PH", None),
            "temp": getattr(deviceInfo, "temp", None),
            "ele": getattr(deviceInfo, "ele", None),
            "tur": getattr(deviceInfo, "tur", None),
            "O2": getattr(deviceInfo, "O2", None),
            "COD": getattr(deviceInfo, "COD", None),
            "NH3": getattr(deviceInfo, "NH3", None),
            "NO3": getattr(deviceInfo, "NO3", None),
            "chl": getattr(deviceInfo, "chl", None),
        }
        self.client.publish(TELEMETRY_TOPIC, json.dumps(payload), qos=1)

    def publish_state(self):
        payload = {
            "deviceID": deviceID,
            "timestamp": utc_now_iso(),
            "type": "state",
            "modelSelect": getattr(deviceController, "modelSelect", None),
            "operationSelect": getattr(deviceController, "operationSelect", None),
            "samplePump": getattr(deviceController, "samplePump", None),
            "manualDetect": getattr(deviceController, "manualDetect", None),
            "deviceStep": getattr(deviceController, "deviceStep", None),
            "warningInfo": getattr(deviceInfo, "warningInfo", None),
            "currentState": getattr(deviceInfo, "currentState", None),
        }
        self.client.publish(STATE_TOPIC, json.dumps(payload), qos=1)

    def run_forever(self, interval=MQTT_PUBLISH_INTERVAL):
        try:
            while not self.stop_event.is_set():
                try:
                    self.publish_telemetry()
                    self.publish_state()
                except Exception as exc:
                    print(f"[MQTT] publish error: {exc}")
                for _ in range(interval):
                    if self.stop_event.is_set():
                        break
                    time.sleep(1)
        except KeyboardInterrupt:
            print("[MQTT] main loop stopped")


if __name__ == "__main__":
    client = MqttDeviceClient()
    client.connect()
    try:
        client.run_forever()
    finally:
        client.disconnect()
