#!/usr/bin/env python3
"""
Headless MQTT demo server for the VNC device.
Triggers manual detection, parses step progress using stepString logic,
and dynamically waits until the device completes its full cycle and returns to idle.
"""

import json
import os
import sys
import threading
import time
import uuid
from typing import Any, Dict, Optional

try:
    import paho.mqtt.client as mqtt
except Exception as exc:  
    raise SystemExit("paho-mqtt is required. Install with: pip install paho-mqtt") from exc

DEVICE_ID = os.getenv("DEVICE_ID", "0001")
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "user")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "abcd")
# Increased timeout to 120 seconds (or configurable via environment variable) to allow lengthy hardware sequences to complete
RESULT_TIMEOUT = int(os.getenv("RESULT_TIMEOUT", "480"))
TARGET_TOPIC = os.getenv("TARGET_TOPIC", f"device/wq/{DEVICE_ID}")


class DemoServer:
    def __init__(self):
        self.result_lock = threading.Lock()
        self.result = {"reply": None, "state": None, "telemetry": None}
        self._done = threading.Event()
        self.sent_msg_id = None
        self.operation_started = False
        
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"demo_server_{DEVICE_ID}")
        
        if MQTT_USER or MQTT_PASSWORD:
            self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
            
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def step_string(self, deviceAutoRun, deviceStep):
        """Translates device auto-run flags and step codes into descriptions (from mainBoard.py)."""
        stepStr = ""
        if deviceAutoRun:
            stepStr = "自动流程"
        elif deviceStep:
            stepStr = "手动流程"
            
        if deviceStep == 0x00:
            stepStr += "系统空闲"
        elif deviceStep == 0x01:
            stepStr += "(排空清水)"
        elif deviceStep == 0x02:
            stepStr += "(采集水样)"
        elif deviceStep == 0x03:
            stepStr += "(读取数据)"
        elif deviceStep == 0x04:
            stepStr += "(排空水样)"
        elif deviceStep == 0x05:
            stepStr += "(填充清水)"
        elif deviceStep == 0x06:
            stepStr += "(清洗滤膜)"
        elif deviceStep == 0x0A:
            stepStr += "(读取GPS)"
        elif deviceStep == 0x0B:
            stepStr += "(电机初始化)"
        elif deviceStep == 0x0C:
            stepStr += "(向下投放)"
        elif deviceStep == 0x0D:
            stepStr += "(蠕动泵抽)"
        elif deviceStep == 0x0E:
            stepStr += "(向上回收)"
        elif deviceStep == 0x0F:
            stepStr += "(向上微调)"
        elif deviceStep == 0x10:
            stepStr += "(向下微调)"
        else:
            stepStr += f"(未知步骤: {deviceStep})"
        return stepStr

    def on_connect(self, client, userdata, flags, rc, properties=None):
        is_failure = rc.is_failure if hasattr(rc, "is_failure") else (int(rc) != 0)
        if is_failure:
            print(f"[demo] MQTT connect failed: rc={rc}")
            return
        print(f"[demo] connected to {BROKER}:{PORT}")
        client.subscribe(TARGET_TOPIC, qos=1)
        print(f"[demo] subscribed to: {TARGET_TOPIC}")

    def on_message(self, client, userdata, message):
        try:
            payload = message.payload.decode("utf-8")
            obj = json.loads(payload)
        except Exception:
            return
            
        if not isinstance(obj, dict) or obj.get("type") == "cmd":
            return
            
        msg_type = obj.get("type")
        print(f"[demo] <- {message.topic} [{msg_type}]: {json.dumps(obj, ensure_ascii=False)}")
        
        with self.result_lock:
            if msg_type == "telemetry":
                self.result["telemetry"] = obj
                if "data" in obj and "actuators" in obj["data"] and "state" in obj["data"]["actuators"]:
                    current_state = obj["data"]["actuators"]["state"]
                    self.result["state"] = current_state
                    
                    device_auto_run = current_state.get("deviceAutoRun", 0) or 0
                    device_step = current_state.get("deviceStep", 0) or 0
                    manual_detect = current_state.get("manualDetect", 0) or 0
                    
                    # Analyze and print step description using stepString logic
                    step_desc = self.step_string(device_auto_run, device_step)
                    print(f"[demo] -> [Device Status Analysis] StepCode: {device_step} | State Text: {step_desc}")

                    # Lifecycle tracking: detect start and wait for return to idle (0x00)
                    if device_step != 0 or device_auto_run == 1 or manual_detect == 1:
                        self.operation_started = True
                    
                    if self.operation_started and device_step == 0 and device_auto_run == 0 and manual_detect == 0:
                        print("[demo] -> Operation complete! Device returned to idle (System Idle).")
                        self._done.set()

            elif msg_type == "reply" and obj.get("reply_to") == self.sent_msg_id:
                self.result["reply"] = obj
                print("[demo] Command acknowledgment reply received.")

            elif msg_type == "status":
                self.result["state"] = obj

    def publish_manual_detect(self):
        self.sent_msg_id = uuid.uuid4().hex
        command = {
            "msg_id": self.sent_msg_id,
            "type": "cmd",
            "device_id": DEVICE_ID,
            "timestamp": int(time.time() * 1000),
            "cmd": "manual_detect",
            "params": {"action": "start"}
        }
        print(f"[demo] -> {TARGET_TOPIC}: {json.dumps(command, ensure_ascii=False)}")
        self.client.publish(TARGET_TOPIC, json.dumps(command), qos=1)

    def print_summary(self):
        print("\n=== Demo result summary (Final State) ===")
        for key in ("reply", "state", "telemetry"):
            print(f"{key}: {json.dumps(self.result[key], ensure_ascii=False, sort_keys=True)}")

    def run(self):
        self.client.connect(BROKER, PORT, keepalive=60)
        self.client.loop_start()
        try:
            time.sleep(1.0)
            self.publish_manual_detect()
            
            print(f"[demo] Waiting up to {RESULT_TIMEOUT} seconds for procedure to finish and return to idle...")
            if not self._done.wait(timeout=RESULT_TIMEOUT):
                print(f"[demo] Warning: Result collection timed out after {RESULT_TIMEOUT} seconds.")
            
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