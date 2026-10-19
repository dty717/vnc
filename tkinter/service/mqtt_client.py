#!/usr/bin/env python3
"""
MQTT device client for VNC project.

Combines the runtime logic with the demo "envelope" protocol used by the demo emulator.
- Subscribes exclusively to the device-wq style topic: device/wq/<deviceID>
- Accepts two command styles:
  1) envelope style: {"msg_id":..., "type":"cmd", "cmd":"...", "params":{...}}
  2) plain style: {"cmd":"...", ...} (backwards compatible)
- Replies using envelope reply messages on the same TOPIC the command arrived on.
- Publishes envelope telemetry and status payloads to the unified TOPIC channel.

Uses existing device runtime objects (deviceController, deviceInfo) and device control functions so UI will react the same way as user clicks.
"""

import os
import json
import time
import threading
import uuid
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except Exception as exc:  # pragma: no cover
    raise RuntimeError("paho-mqtt is required. Install with: pip install paho-mqtt") from exc

# Using print instead of logging

# Import layout attributes using lowercase camelCase fields
try:
    from config.config import (
        deviceID,
        mqttBroker,
        mqttPort,
        mqttUser,
        mqttPassword,
        mqttPublishInterval,
        topicBase
    )
except ImportError as exc:
    raise RuntimeError("Required attributes missing from config.config") from exc

# Map configuration configurations to local script variables
DEVICE_ID = deviceID or "device_unknown"
MQTT_BROKER = mqttBroker or "localhost"
MQTT_PORT = int(mqttPort) if mqttPort is not None else 1883
MQTT_USER = mqttUser or ""
MQTT_PASSWORD = mqttPassword or ""
MQTT_PUBLISH_INTERVAL = int(mqttPublishInterval) if mqttPublishInterval is not None else 10

# Unified single channel topic layout matching the reference demo code style
LEGACY_BASE = topicBase or "device/wq"
TOPIC = f"{LEGACY_BASE}/{DEVICE_ID}"

# Import device runtime components and control functions
from service.device import (
    deviceInfo,
    deviceController,
    write_single_register,
    write_single_coil,
    write_multiple_registers,
    operatingAllStep,
    operatingAllStepCancel,
    requestDeviceEvent,
)
# Optional operational modules mapping
try:
    from service.device import (
        probeRelay,
        pumpRelay,
        motor_driver,
        readProbe,
        readProbeCancel,
        manualDetectAllStep,
        manualDetectAllStepCancel,
    )
except Exception:
    probeRelay = pumpRelay = motor_driver = None
    readProbe = readProbeCancel = manualDetectAllStep = manualDetectAllStepCancel = None


def now_ms():
    return int(time.time() * 1000)


def utc_now_iso():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def envelope(msg_type, **extra):
    """Create a standard tracking envelope used by backend infrastructure."""
    return {"msg_id": uuid.uuid4().hex, "type": msg_type, "device_id": DEVICE_ID, "timestamp": now_ms(), **extra}


class MqttDeviceClient:
    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD):
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.stop_event = threading.Event()

        # Upgraded client generation incorporating standard modern Paho version tracking
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"device/{DEVICE_ID}")
        except (AttributeError, TypeError):
            self.client = mqtt.Client(client_id=f"device/{DEVICE_ID}")

        if self.user:
            self.client.username_pw_set(self.user, self.password)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if int(rc) != 0:
            print(f"[MQTT] Connection failed with status code={rc}")
            return

        print(f"[MQTT] connected, subscribe {TOPIC}")
        # Subscribe exclusively to the single unified topic framework
        client.subscribe(TOPIC, qos=1)

        # Publish retained online notification frame matching the demo behavior
        status = envelope("status", online=True)
        client.publish(TOPIC, json.dumps(status), qos=1, retain=True)

    def _on_disconnect(self, client, userdata, disconnect_flags=None, rc=None, properties=None):
        print("[MQTT] Client disconnected from broker target.")

    def _handle_command_envelope(self, req):
        """Processes high-level routing strings down to functional register calls."""
        cmd = str(req.get("cmd") or "").lower()
        params = req.get("params") or {}
        action = str(params.get("action", "")).lower()

        try:
            # Emergency Stop Implementation matching design requirements
            if cmd == "stop":
                deviceController.deviceAutoRun = 0
                deviceController.manualDetect = 0
                deviceController.threadDate = datetime.now()
                operatingAllStepCancel()
                if manualDetectAllStepCancel is not None:
                    manualDetectAllStepCancel()
                if probeRelay is not None:
                    probeRelay.off()
                if pumpRelay is not None:
                    pumpRelay.off()
                return 0, "ok", {"state": self._build_state_payload()}

            # Routine Operation Management Flow
            if cmd == "operation":
                if action == "start":
                    if deviceController.deviceAutoRun == 0:
                        deviceController.deviceAutoRun = 1
                        deviceController.threadDate = datetime.now()
                        threading.Thread(target=operatingAllStep, args=(deviceController.threadDate,)).start()
                    return 0, "ok", {"deviceAutoRun": deviceController.deviceAutoRun}
                elif action == "stop":
                    if deviceController.deviceAutoRun == 1:
                        deviceController.deviceAutoRun = 0
                        deviceController.threadDate = datetime.now()
                        operatingAllStepCancel()
                    return 0, "ok", {"deviceAutoRun": deviceController.deviceAutoRun}
                else:
                    if deviceController.deviceAutoRun == 0:
                        deviceController.deviceAutoRun = 1
                        deviceController.threadDate = datetime.now()
                        threading.Thread(target=operatingAllStep, args=(deviceController.threadDate,)).start()
                    else:
                        deviceController.deviceAutoRun = 0
                        deviceController.threadDate = datetime.now()
                        operatingAllStepCancel()
                    return 0, "ok", {"deviceAutoRun": deviceController.deviceAutoRun}

            if cmd == "get_status":
                return 0, "ok", {"state": self._build_state_payload()}

            # Relay Toggle Points
            if cmd == "probe" and probeRelay is not None:
                if action in ("on", "start"):
                    probeRelay.on()
                else:
                    probeRelay.off()
                return 0, "ok", {"probe": bool(probeRelay.value)}

            if cmd == "pump" and pumpRelay is not None:
                if action in ("on", "start"):
                    pumpRelay.on()
                else:
                    pumpRelay.off()
                return 0, "ok", {"pump": bool(pumpRelay.value)}

            # Motor Step Configurations
            if cmd == "motor":
                if action == "init":
                    deviceController.motorInit = 1
                elif action == "up":
                    deviceController.motorUp = 1
                elif action == "down":
                    deviceController.motorDown = 1
                elif action == "stop":
                    deviceController.motorStop = 1
                    try:
                        if motor_driver is not None:
                            motor_driver.value = deviceController.motorStopPWM
                    except Exception:
                        pass
                elif action == "up_little":
                    deviceController.motorUpLittle = 1
                elif action == "down_little":
                    deviceController.motorDownLittle = 1
                elif action == "clear":
                    deviceController.motorInit = deviceController.motorUp = deviceController.motorDown = 0
                    deviceController.motorStop = deviceController.motorUpLittle = deviceController.motorDownLittle = 0
                else:
                    return 400, "unknown motor action", {}
                return 0, "ok", {"motor_flags": True}

            # Manual Detection Protocols
            if cmd == "manual_detect":
                if action == "start" and manualDetectAllStep is not None:
                    if deviceController.manualDetect == 0:
                        deviceController.manualDetect = 1
                        deviceController.threadDate = datetime.now()
                        threading.Thread(target=manualDetectAllStep, args=(deviceController.threadDate,)).start()
                    return 0, "ok", {"manualDetect": deviceController.manualDetect}
                elif action == "stop" and manualDetectAllStepCancel is not None:
                    deviceController.manualDetect = 0
                    deviceController.threadDate = datetime.now()
                    manualDetectAllStepCancel()
                    return 0, "ok", {"manualDetect": deviceController.manualDetect}

            # Serial Modbus Direct Writing Maps
            if cmd == "write_register":
                addr = int(params.get("addr", 0))
                value = int(params.get("value", 0))
                write_single_register(addr, value, lambda rec: None, repeatTimes=0, needMesBox=False)
                return 0, "ok", {"addr": addr, "value": value}

            if cmd == "write_coil":
                addr = int(params.get("addr", 0))
                value = bool(params.get("value", False))
                write_single_coil(addr, value, lambda rec: None, repeatTimes=0, needMesBox=False)
                return 0, "ok", {"addr": addr, "value": value}

            if cmd == "write_multiple":
                addr = int(params.get("addr", 0))
                values = [int(v) for v in params.get("values", [])]
                write_multiple_registers(addr, values, lambda rec: None, repeatTimes=0, needMesBox=False)
                return 0, "ok", {"addr": addr, "values": values}

            # Runtime Object Attribute Modifications
            if cmd == "set_parameter":
                attr = params.get("attr")
                val = params.get("value")
                if not attr:
                    return 400, "missing attr", {}
                try:
                    setattr(deviceController, attr, float(val))
                except Exception:
                    try:
                        setattr(deviceController, attr, int(val))
                    except Exception as e:
                        return 500, f"set error: {e}", {}
                return 0, "ok", {attr: getattr(deviceController, attr)}

            return 404, f"unknown cmd: {cmd}", {}
        finally:
            # Explicit GUI notification trigger to refresh Tkinter windows instantly
            try:
                requestDeviceEvent.set()
            except Exception:
                pass

    def _build_state_payload(self):
        return {
            "modelSelect": getattr(deviceController, "modelSelect", None),
            "operationSelect": getattr(deviceController, "operationSelect", None),
            "samplePump": getattr(deviceController, "samplePump", None),
            "manualDetect": getattr(deviceController, "manualDetect", None),
            "deviceStep": getattr(deviceController, "deviceStep", None),
            "deviceAutoRun": getattr(deviceController, "deviceAutoRun", None),
            "warningInfo": getattr(deviceInfo, "warningInfo", None),
            "currentState": getattr(deviceInfo, "currentState", None),
        }

    def _on_message(self, client, userdata, msg):
        raw = msg.payload.decode("utf-8")
        try:
            payload = json.loads(raw)
        except Exception as exc:
            print(f"[MQTT] Invalid structural frame received: {exc}")
            return

        # Suppress processing messages matching telemetry data, status updates, or existing replies
        if isinstance(payload, dict) and payload.get("type") in ("telemetry", "reply", "status"):
            return

        print(f"recv <- {msg.topic} : {raw}")
        code, message, data = 404, "unknown request format", {}
        cmd_name = "unknown"

        # Parsing Standard Tracking Envelope Structure
        if isinstance(payload, dict) and payload.get("type") == "cmd":
            cmd_name = payload.get("cmd")
            code, message, data = self._handle_command_envelope(payload)
            reply = envelope("reply", reply_to=payload.get("msg_id"), cmd=cmd_name, code=code, message=message, data=data)
            client.publish(TOPIC, json.dumps(reply), qos=1)
            print(f"reply -> code={code} msg={message}")
            return

        # Parsing Direct Single-Line Command Elements
        if isinstance(payload, dict) and payload.get("cmd"):
            cmd_name = payload.get("cmd")
            params = payload.get("params") or {}
            code, message, data = self._handle_command_envelope({"cmd": cmd_name, "params": params})
            reply = envelope("reply", reply_to=payload.get("msg_id"), cmd=cmd_name, code=code, message=message, data=data)
            client.publish(TOPIC, json.dumps(reply), qos=1)
            print(f"reply -> code={code} msg={message}")
            return

    def connect(self):
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()

    def disconnect(self):
        self.stop_event.set()
        # Drop clean offline payload to update broker status registries matching main demo logic
        try:
            self.client.publish(TOPIC, json.dumps(envelope("status", online=False)), qos=1, retain=True)
            time.sleep(0.3)
        except Exception:
            pass
        try:
            self.client.loop_stop()
        except Exception:
            pass
        try:
            self.client.disconnect()
        except Exception:
            pass
        print("stopped")

    def publish_telemetry(self):
        # Gather live telemetry data elements matching device hardware states
        sensors_data = {
            "deviceID": DEVICE_ID,
            "timestamp": utc_now_iso(),
            "PH": getattr(deviceInfo, "PH", None),
            "temp": getattr(deviceInfo, "temp", None),
            "ele": getattr(deviceInfo, "ele", None),
            "tur": getattr(deviceInfo, "tur", None),
            "O2": getattr(deviceInfo, "O2", None),
        }
        actuators_state = {
            "pump": bool(pumpRelay.value) if pumpRelay is not None else False,
            "probe": bool(probeRelay.value) if probeRelay is not None else False,
            "state": self._build_state_payload(),
        }
        # Format and publish utilizing standard single channel envelope structure
        try:
            env = envelope("telemetry", data={**sensors_data, "actuators": actuators_state})
            self.client.publish(TOPIC, json.dumps(env), qos=1)
            print(f"telemetry -> {TOPIC}")
        except Exception as exc:
            print(f"[MQTT] Failed to publish unified loop payload: {exc}")

    def run_forever(self, interval=MQTT_PUBLISH_INTERVAL):
        try:
            while not self.stop_event.is_set():
                self.publish_telemetry()
                for _ in range(interval):
                    if self.stop_event.is_set():
                        break
                    time.sleep(1)
        except KeyboardInterrupt:
            print("[MQTT] Connection runner killed by interrupt signal.")


if __name__ == "__main__":
    client = MqttDeviceClient()
    client.connect()
    try:
        client.run_forever()
    finally:
        client.disconnect()
