#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "zap": {
        "type": "url",
        "description": "(ZAP) Zed Attack Proxy",
        "options": [
            {
                "name": "url",
                "label": "URL to scan",
                "type": "text",
                "default": "",
                "explanation": "The target URL to scan for vulnerabilities."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "zap": lambda args: ["zap-cli", "quick-scan", args[0]]
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'zap':
    args = []
    target = data.get('url')
    if target:
        args.append(target)
    else:
        emit('log_message', "No URL provided for ZAP scan.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "zap": {
            "name": "zap",
            "install_cmd": {
                "linux": "sudo apt-get install -y zaproxy",
                "macos": "brew install zaproxy",
                "windows": "choco install zap"
            }
        }
    }
```
