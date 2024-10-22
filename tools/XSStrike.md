#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "xsstrike": {
        "type": "url",
        "description": "(XSStrike) Cross-Site Scripting Detection Tool",
        "options": [
            {
                "name": "url",
                "label": "URL to scan",
                "type": "text",
                "default": "",
                "explanation": "Enter the target URL to test for XSS vulnerabilities."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "xsstrike": lambda args: ["xsstrike", "-u"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'xsstrike':
    args = []
    target = data.get('url')
    if target:
        args.append(target)
    else:
        emit('log_message', "No URL provided for XSStrike scan.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "xsstrike": {
            "name": "xsstrike",
            "install_cmd": {
                "linux": "sudo apt-get install -y xsstrike",
                "macos": "pip install xsstrike",
                "windows": "pip install xsstrike"
            }
        }
    }
```
