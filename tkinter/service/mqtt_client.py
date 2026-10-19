#!/usr/bin/env python3
"""
MQTT device client for VNC project.

Combines the previous vnc/ topic style and the demo "envelope" protocol used by the demo emulator.
- Subscribes to both vnc/<deviceID>/command and device-wq style topic device/wq/<deviceID>
- Accepts two command styles:
  1) envelope style: {"msg_id":..., "type":"cmd", "cmd":"...", "params":{...}}
  2) plain style: {"cmd":"...", ...} (backwards compatible)
- Replies using envelope reply messages on the same topic the command arrived on.
- Publishes both vnc telemetry/state and envelope telemetry for legacy/demo tools.

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

# Try to import deviceID from repo config if available
try:
    from config.config import deviceID as CONFIG_DEVICE_ID
except Exception:
    CONFIG_DEVICE_ID = None

DEVICE_ID = os.environ.get("DEVICE_ID", CONFIG_DEVICE_ID or "device_unknown")

# Broker settings
MQTT_BROKER = os.environ.get("MQTT_BROKER", os.environ.get("MQTT_HOST", "localhost"))
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_USER = os.environ.get("MQTT_USER", "")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "")
MQTT_PUBLISH_INTERVAL = int(os.environ.get("MQTT_PUBLISH_INTERVAL", "10"))

# Topic layout
VNC_BASE = f"vnc/{DEVICE_ID}"
VNC_TELEMETRY = f"{VNC_BASE}/telemetry"
VNC_STATE = f"{VNC_BASE}/state"
VNC_COMMAND = f"{VNC_BASE}/command"

LEGACY_BASE = os.environ.get("TOPIC_BASE", "device/wq")
LEGACY_TOPIC = f"{LEGACY_BASE}/{DEVICE_ID}"

# import device runtime and control functions
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
# optional imports for more control if available
try:
    from service.device import probeRelay, pumpRelay, motor_driver, readProbe, readProbeCancel, manualDetectAllStep, manualDetectAllStepCancel
except Exception:
    probeRelay = pumpRelay = motor_driver = None
    readProbe = readProbeCancel = manualDetectAllStep = manualDetectAllStepCancel = None


def now_ms():
    return int(time.time() * 1000)


def utc_now_iso():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def envelope(msg_type, **extra):
    """Create a standard envelope used by legacy/demo scripts."""
    return {"msg_id": uuid.uuid4().hex, "type": msg_type, "device_id": DEVICE_ID, "timestamp": now_ms(), **extra}


class MqttDeviceClient:
    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD):
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.stop_event = threading.Event()
        self.client = mqtt.Client(client_id=f"vnc-device-{DEVICE_ID}")
        if self.user:
            self.client.username_pw_set(self.user, self.password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT] connected rc={rc}")
        # subscribe to both vnc command topic and legacy topic
        client.subscribe(VNC_COMMAND, qos=1)
        client.subscribe(LEGACY_TOPIC, qos=1)
        # publish retained status on both topics
        status = envelope("status", online=True)
        client.publish(LEGACY_TOPIC, json.dumps(status), qos=1, retain=True)
        client.publish(VNC_BASE + "/status", json.dumps({"deviceID": DEVICE_ID, "timestamp": utc_now_iso(), "online": True}), qos=1, retain=True)

    def _on_disconnect(self, client, userdata, rc):
        print("[MQTT] disconnected")

    def _handle_command_envelope(self, req):
        """Handle an envelope-style command (type=="cmd"). Return (code, message, data).
        This maps high-level commands to existing device functions and state updates so the UI reflects changes.
        """
        cmd = str(req.get("cmd") or "").lower()
        params = req.get("params") or {}
        action = str(params.get("action", "")).lower()

        try:
            # Basic control commands mapped to deviceController
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
                    # toggle
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

            # hardware toggles (probe/pump)
            if cmd == "probe" and probeRelay is not None:
                if action == "on":
                    probeRelay.on()
                else:
                    probeRelay.off()
                return 0, "ok", {"probe": bool(probeRelay.value)}

            if cmd == "pump" and pumpRelay is not None:
                if action == "on":
                    pumpRelay.on()
                else:
                    pumpRelay.off()
                return 0, "ok", {"pump": bool(pumpRelay.value)}

            # motor flags
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

            # manual detect
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

            # write register/coil/multiple are forwarded to existing serial functions
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

            # set_parameter for SettingBoard
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
            # Wake the UI refresh loop so changes are visible in Tkinter promptly
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
        # try parse JSON
        try:
            payload = json.loads(raw)
        except Exception as exc:
            print("[MQTT] invalid json payload:", exc)
            return

        # If envelope-style (legacy/demo)
        if isinstance(payload, dict) and payload.get("type") == "cmd":
            # envelope command
            code, message, data = self._handle_command_envelope(payload)
            reply = envelope("reply", reply_to=payload.get("msg_id"), cmd=payload.get("cmd"), code=code, message=message, data=data)
            client.publish(msg.topic, json.dumps(reply), qos=1)
            return

        # Backwards compatible: plain command style used earlier in repo
        if isinstance(payload, dict) and payload.get("cmd"):
            # support short-style commands same as before
            cmd = payload.get("cmd")
            # convert to unified params structure
            params = payload.get("params") or {}
            # forward to envelope handler for common logic
            req = {"cmd": cmd, "params": params}
            code, message, data = self._handle_command_envelope(req)
            # reply as envelope on same topic
            reply = envelope("reply", reply_to=payload.get("msg_id"), cmd=cmd, code=code, message=message, data=data)
            client.publish(msg.topic, json.dumps(reply), qos=1)
            return

        # otherwise ignore non-command messages
        return

    def connect(self):
        if self.user:
            self.client.username_pw_set(self.user, self.password)
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
        # simple vnc telemetry (backwards compatible)
        telemetry = {
            "deviceID": DEVICE_ID,
            "timestamp": utc_now_iso(),
            "PH": getattr(deviceInfo, "PH", None),
            "temp": getattr(deviceInfo, "temp", None),
            "ele": getattr(deviceInfo, "ele", None),
            "tur": getattr(deviceInfo, "tur", None),
            "O2": getattr(deviceInfo, "O2", None),
        }
        try:
            self.client.publish(VNC_TELEMETRY, json.dumps(telemetry), qos=1)
        except Exception:
            pass
        # legacy envelope telemetry on legacy topic to support demo tools
        try:
            env = envelope("telemetry", data={"sensors": telemetry, "actuators": {}})
            self.client.publish(LEGACY_TOPIC, json.dumps(env), qos=1)
        except Exception:
            pass

    def publish_state(self):
        state = {"deviceID": DEVICE_ID, "timestamp": utc_now_iso(), "type": "state", **self._build_state_payload()}
        try:
            self.client.publish(VNC_STATE, json.dumps(state), qos=1)
        except Exception:
            pass
        # also publish envelope state on legacy topic
        try:
            env = envelope("status", online=True, state=self._build_state_payload())
            self.client.publish(LEGACY_TOPIC, json.dumps(env), qos=1)
        except Exception:
            pass

    def run_forever(self, interval=MQTT_PUBLISH_INTERVAL):
        try:
            while not self.stop_event.is_set():
                try:
                    self.publish_telemetry()
                    self.publish_state()
                except Exception as exc:
                    print("[MQTT] publish error:", exc)
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
