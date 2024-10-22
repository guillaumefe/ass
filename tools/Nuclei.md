#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "nuclei": {
        "type": "url",
        "description": "Vulnerability Scanner",
        "options": [
            {
                "name": "target",
                "label": "Target URL",
                "type": "text",
                "default": "",
                "explanation": "The target URL for scanning vulnerabilities."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "nuclei": lambda args: ["nuclei", "-u"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'nuclei':
    args = []
    target = data.get('target')
    if target:
        args.append(target)
    else:
        emit('log_message', "No URL provided for nuclei scan.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "nuclei": {
            "name": "nuclei",
            "install_cmd": {
                "linux": "sudo apt-get install -y nuclei",
                "macos": "brew install nuclei",
                "windows": "go get -u github.com/projectdiscovery/nuclei/v2/cmd/nuclei"
            }
        }
    }
```
