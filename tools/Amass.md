#### Amass

#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "amass": {
        "type": "url",
        "description": "Subdomain Enumeration and Network Mapping Tool",
        "options": [
            {
                "name": "domains",
                "label": "Domain to search",
                "type": "text",
                "default": "",
                "explanation": "The target domain for subdomain enumeration."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "amass": lambda args: ["amass", "enum", "-d"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'amass':
    args = []
    target = data.get('domains')
    if target:
        args.append(target)
    else:
        emit('log_message', "No domain provided for amass scan.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "amass": {
            "name": "amass",
            "install_cmd": {
                "linux": "sudo apt-get install -y amass",
                "macos": "brew install amass",
                "windows": "choco install amass"
            }
        }
    }
```
