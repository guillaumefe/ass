#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "censys": {
        "type": "ip",
        "description": "IP Information and Security Scanner",
        "options": [
            {
                "name": "ip",
                "label": "Target IP Address",
                "type": "text",
                "default": "",
                "explanation": "The target IP address to gather information from Censys."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "censys": lambda args: ["censys", "ipv4", args[0]]
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'censys':
    args = []
    ip = data.get('ip')
    if ip:
        args.append(ip)
    else:
        emit('log_message', "No IP address provided for censys.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "censys": {
            "name": "censys",
            "install_cmd": {
                "linux": "pip install censys",
                "macos": "pip install censys",
                "windows": "pip install censys"
            }
        }
    }
```
