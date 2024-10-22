#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "subfinder": {
        "type": "url",
        "description": "(Subfinder) Subdomain Enumeration Tool",
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
    "subfinder": lambda args: ["subfinder", "-d"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'subfinder':
    args = []
    target = data.get('domains')
    if target:
        args.append(target)
    else:
        emit('log_message', "No domain provided for subfinder scan.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "subfinder": {
            "name": "subfinder",
            "install_cmd": {
                "linux": "sudo apt-get install -y subfinder",
                "macos": "brew install subfinder",
                "windows": "go get -u github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
            }
        }
    }
```

