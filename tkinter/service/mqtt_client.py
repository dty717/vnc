#!/usr/bin/env python3
"""
MQTT device client for VNC project.

Combines runtime logic with the demo "envelope" protocol, pulling dynamic 
measurement/timestamp elements directly from device runtime services.
Publishes on MQTT_PUBLISH_INTERVAL only if data or state has changed.
`data` and `state` are separate root-level keys in the envelope.
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

DEVICE_ID = deviceID or "device_unknown"
MQTT_BROKER = mqttBroker or "localhost"
MQTT_PORT = int(mqttPort) if mqttPort is not None else 1883
MQTT_USER = mqttUser or ""
MQTT_PASSWORD = mqttPassword or ""
MQTT_PUBLISH_INTERVAL = int(mqttPublishInterval) if mqttPublishInterval is not None else 10

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
    if hasattr(deviceInfo, "timestamp_ms") and deviceInfo.timestamp_ms:
        return int(deviceInfo.timestamp_ms)
    return int(time.time() * 1000)


def utc_now_iso():
    if hasattr(deviceInfo, "timestamp") and deviceInfo.timestamp:
        return str(deviceInfo.timestamp)
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
        is_failure = rc.is_failure if hasattr(rc, "is_failure") else (int(rc) != 0)
        if is_failure:
            print(f"[MQTT] Connection failed with status code={rc}")
            return

        print(f"[MQTT] connected, subscribe {TOPIC}")
        client.subscribe(TOPIC, qos=1)

        status = envelope("status", online=True)
        client.publish(TOPIC, json.dumps(status), qos=1, retain=True)

    def _on_disconnect(self, client, userdata, disconnect_flags=None, rc=None, properties=None):
        print("[MQTT] Client disconnected from broker target.")

    def _handle_command_envelope(self, req):
        cmd = str(req.get("cmd") or "").lower()
        params = req.get("params") or []

        if isinstance(params, (list, tuple)):
            action = str(params[0]).lower() if len(params) > 0 else ""
        else:
            action = str(params.get("action", "")).lower() if isinstance(params, dict) else ""

        try:
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

            if cmd == "write_register":
                addr = int(params[1]) if isinstance(params, (list, tuple)) and len(params) > 1 else 0
                value = int(params[2]) if isinstance(params, (list, tuple)) and len(params) > 2 else 0
                write_single_register(addr, value, lambda rec: None, repeatTimes=0, needMesBox=False)
                return 0, "ok", {"addr": addr, "value": value}

            if cmd == "write_coil":
                addr = int(params[1]) if isinstance(params, (list, tuple)) and len(params) > 1 else 0
                value = bool(params[2]) if isinstance(params, (list, tuple)) and len(params) > 2 else False
                write_single_coil(addr, value, lambda rec: None, repeatTimes=0, needMesBox=False)
                return 0, "ok", {"addr": addr, "value": value}

            if cmd == "write_multiple":
                addr = int(params[1]) if isinstance(params, (list, tuple)) and len(params) > 1 else 0
                values = [int(v) for v in params[2]] if isinstance(params, (list, tuple)) and len(params) > 2 else []
                write_multiple_registers(addr, values, lambda rec: None, repeatTimes=0, needMesBox=False)
                return 0, "ok", {"addr": addr, "values": values}

            if cmd == "set_parameter":
                attr = params[1] if isinstance(params, (list, tuple)) and len(params) > 1 else None
                val = params[2] if isinstance(params, (list, tuple)) and len(params) > 2 else None
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
        print(f"[MQTT DEBUG] RAW RECV <- {msg.topic} : {raw}")

        try:
            payload = json.loads(raw)
        except Exception as exc:
            print(f"[MQTT] Invalid structural frame received: {exc}")
            return

        if not isinstance(payload, dict):
            return

        if payload.get("type") in ("state", "reply", "status"):
            return

        cmd_name = payload.get("cmd")
        if not cmd_name:
            return

        params = payload.get("params", [])

        code, message, data = self._handle_command_envelope({"cmd": cmd_name, "params": params})
        reply = envelope("reply", reply_to=payload.get("msg_id"), cmd=cmd_name, code=code, message=message, data=data)
        client.publish(TOPIC, json.dumps(reply), qos=1)
        print(f"reply -> code={code} msg={message}")

    def connect(self):
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()

    def disconnect(self, timeout=0.3):
        self.stop_event.set()
        try:
            self.client.publish(TOPIC, json.dumps(envelope("status", online=False)), qos=1, retain=True)
            time.sleep(timeout)
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

    def run_forever(self, interval=MQTT_PUBLISH_INTERVAL):
        last_sensors_signature = None
        last_state_signature = None
        last_sent_step = None
        try:
            while not self.stop_event.is_set():
                sensors_data = {
                    "deviceID": DEVICE_ID,
                    "timestamp": utc_now_iso(),
                    "PH": getattr(deviceInfo, "PH", None),
                    "temp": getattr(deviceInfo, "temp", None),
                    "ele": getattr(deviceInfo, "ele", None),
                    "tur": getattr(deviceInfo, "tur", None),
                    "O2": getattr(deviceInfo, "O2", None),
                }
                state_payload = {
                    "pump": bool(pumpRelay.value) if pumpRelay is not None else False,
                    "probe": bool(probeRelay.value) if probeRelay is not None else False,
                    **self._build_state_payload(),
                }

                current_step = state_payload.get("deviceStep")

                current_sensors_signature = (
                    getattr(deviceInfo, "timestamp", None),
                    sensors_data["PH"],
                    sensors_data["temp"],
                    sensors_data["ele"],
                    sensors_data["tur"],
                    sensors_data["O2"],
                )
                current_state_signature = tuple(sorted(state_payload.items()))

                sensors_changed = (last_sensors_signature is None or current_sensors_signature != last_sensors_signature)
                
                # Force data upload when entering Step 3 (Reading Data)
                if current_step == 3 and last_sent_step != 3:
                    sensors_changed = True

                state_changed = (last_state_signature is None or current_state_signature != last_state_signature)

                extra = {}
                if sensors_changed:
                    extra["data"] = sensors_data
                    last_sensors_signature = current_sensors_signature
                    if current_step == 3:
                        last_sent_step = 3
                    else:
                        last_sent_step = current_step

                if state_changed:
                    extra["state"] = state_payload
                    last_state_signature = current_state_signature

                if extra:
                    try:
                        env = envelope("state", **extra)
                        self.client.publish(TOPIC, json.dumps(env), qos=1)
                        print(f"state -> {TOPIC} (sent changes: {list(extra.keys())})")
                    except Exception as exc:
                        print(f"[MQTT] Failed to publish unified loop payload: {exc}")
                else:
                    print(f"[MQTT] No state/data changes detected, skipping publish.")

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
