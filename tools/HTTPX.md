#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "httpx": {
        "type": "url",
        "description": "(HTTPX) HTTP Probing Tool",
        "options": [
            {
                "name": "target",
                "label": "Target URL",
                "type": "text",
                "default": "",
                "explanation": "The target URL for probing HTTP headers."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "httpx": lambda args: ["httpx", "-u"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'httpx':
    args = []
    target = data.get('target')
    if target:
        args.append(target)
    else:
        emit('log_message', "No URL provided for httpx.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "httpx": {
            "name": "httpx",
            "install_cmd": {
                "linux": "sudo apt-get install -y httpx",
                "macos": "brew install httpx",
                "windows": "go get -u github.com/projectdiscovery/httpx/cmd/httpx"
            }
        }
    }
```
