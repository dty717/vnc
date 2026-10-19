# MQTT protocol for VNC device (branch: mqtt_for_device)

Summary
- The MQTT client in this branch supports two interoperable command styles:
  1) Plain JSON commands (used by vnc/* topics in the repo)
  2) Envelope (demo/legacy) style used by earlier demo scripts and the emulator
- The client subscribes to:
  - vnc/<deviceID>/command (plain-style commands)
  - device/wq/<deviceID> (legacy/envelope commands) — configurable with TOPIC_BASE env
- When commands arrive the client updates the same runtime state (deviceController / deviceInfo) and calls the same background routines the UI uses. The Tk UI refresh loop then updates the widgets — MQTT behaves exactly like a UI click.

Topics
- vnc telemetry/state/commands (repo-native)
  - Telemetry publish: vnc/<deviceID>/telemetry
  - State publish:     vnc/<deviceID>/state
  - Command subscribe: vnc/<deviceID>/command

- Legacy/envelope topic (demo compatibility)
  - device/wq/<deviceID>  (default legacy base TOPIC_BASE="device/wq")

Envelopes (legacy/demo format)
- Generic envelope used in legacy/demo messages:

{
  "msg_id": "<uuid>",
  "type": "<telemetry|status|cmd|reply>",
  "device_id": "<DEVICE_ID>",
  "timestamp": 123456789,   // ms
  ...
}

- Example envelope command (sent to device/wq/<deviceID>):

{
  "msg_id": "abc123",
  "type": "cmd",
  "cmd": "pump",
  "params": {"action": "start"}
}

- The device replies with an envelope on the same topic:

{
  "msg_id": "reply-uuid",
  "type": "reply",
  "reply_to": "abc123",
  "cmd": "pump",
  "code": 0,
  "message": "ok",
  "data": { "running": true }
}

Plain command style (repo-native)
- Example plain command (sent to vnc/<deviceID>/command):

{"cmd":"operation","action":"start"}

- The client also replies on the same topic with an envelope-style reply to keep responses uniform.

Main commands (supported)
- operation
  - Start auto-run: {"cmd":"operation","action":"start"}
  - Stop auto-run:  {"cmd":"operation","action":"stop"}
  - Toggle:         {"cmd":"operation"}  // optional toggle
  - Behavior: updates deviceController.deviceAutoRun and starts/stops operatingAllStep(...) exactly as GUI’s MainBoard.operating().

- get_status
  - {"cmd":"get_status"}
  - Behavior: immediately publishes the device state and telemetry.

- probe / pump
  - {"cmd":"probe","params":{"action":"on"}} / {"cmd":"probe","params":{"action":"off"}}
  - {"cmd":"pump","params":{"action":"on"}} / {"cmd":"pump","params":{"action":"off"}}
  - If hardware bindings exist the client calls probeRelay.on()/off() and pumpRelay.on()/off().

- motor
  - {"cmd":"motor","params":{"action":"init"|"up"|"down"|"stop"|"up_little"|"down_little"|"clear"}}
  - Behavior: sets corresponding deviceController motor flags; motor_stop may set motor_driver.value accordingly.

- manual_detect
  - {"cmd":"manual_detect","params":{"action":"start"}} / {"cmd":"manual_detect","params":{"action":"stop"}}
  - Behavior: spawns/cancels manualDetectAllStep thread just like the GUI.

- set_parameter
  - {"cmd":"set_parameter","params":{"attr":"motorDownTime","value":12.5}}
  - Behavior: sets attribute on deviceController (float/int) — same as SettingBoard.setControllerValue.

- write_register / write_coil / write_multiple
  - Forwarded to existing serial/write functions:
    - {"cmd":"write_register","params":{"addr":2,"value":3}}
    - {"cmd":"write_coil","params":{"addr":10,"value":true}}
    - {"cmd":"write_multiple","params":{"addr":30,"values":[100,200,300]}}

Telemetry payload (vnc/<deviceID>/telemetry)
- Example:

{
  "deviceID": "SmartDetect_...",
  "timestamp": "2026-10-18T10:00:00Z",
  "PH": 7.2,
  "temp": 22.5,
  "ele": 300.1,
  "tur": 0.5,
  "O2": 8.1
}

State payload (vnc/<deviceID>/state)
- Example:

{
  "deviceID": "SmartDetect_...",
  "timestamp": "2026-10-18T10:00:00Z",
  "type": "state",
  "modelSelect": 0,
  "operationSelect": 1,
  "samplePump": 0,
  "manualDetect": 0,
  "deviceStep": 0,
  "deviceAutoRun": 1,
  "warningInfo": 0,
  "currentState": 0
}

Reply envelope (uniform reply format)
- For both command styles the client publishes a reply envelope. Example:

{
  "msg_id": "reply-uuid",
  "type": "reply",
  "reply_to": "orig-msg-id",
  "cmd": "operation",
  "code": 0,
  "message": "ok",
  "data": {"deviceAutoRun":1}
}

UI integration and safety
- MQTT handlers update runtime objects (deviceController, deviceInfo) and call the same background functions the UI uses (operatingAllStep, manualDetectAllStep, etc.).
- The MQTT client does NOT call Tkinter widget methods directly. Instead it sets `requestDeviceEvent` so RequestDevice() and the UI refresh loops pick up changes and update the GUI on the main thread.
- This preserves a single source of truth and avoids Tk thread-safety issues.

Environment variables (optional)
- MQTT_BROKER / MQTT_HOST (default: localhost)
- MQTT_PORT (default: 1883)
- MQTT_USER / MQTT_PASS
- DEVICE_ID (fallback to tkinter/config/config.py deviceID if available)
- TOPIC_BASE (legacy envelope base, default: device/wq)
- MQTT_PUBLISH_INTERVAL (seconds, default: 10)

Quick test examples (using mosquitto_pub)
- Operation start:
  mosquitto_pub -h <broker> -t "vnc/SmartDetect_ID/command" -m '{"cmd":"operation","action":"start"}'
- Probe ON (if supported):
  mosquitto_pub -h <broker> -t "vnc/SmartDetect_ID/command" -m '{"cmd":"probe","params":{"action":"on"}}'
- Envelope command (legacy topic):
  mosquitto_pub -h <broker> -t "device/wq/0001" -m '{"msg_id":"abc","type":"cmd","cmd":"pump","params":{"action":"start"}}'

Security and production notes
- For production, enable TLS and broker authentication; do not use public credentials in code.
- Consider adding schema versioning in payloads, stricter validation, and rate-limiting.
- Choose appropriate QoS/retain flags for your use case.

Changelog
- This branch merges the demo/envelope protocol into the main MQTT client and enables the MQTT client to run in the same process as the Tk GUI. Commands use the same deviceController/deviceInfo and background routines to ensure UI behavior is identical to manual control.
