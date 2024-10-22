#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "dnsrecon": {
        "type": "url",
        "description": "(DNSRecon) DNS Enumeration and Recon Tool",
        "options": [
            {
                "name": "domain",
                "label": "Domain to search",
                "type": "text",
                "default": "",
                "explanation": "The domain to query for DNS information."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "dnsrecon": lambda args: ["dnsrecon", "-d"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'dnsrecon':
    args = []
    target = data.get('domain')
    if target:
        args.append(target)
    else:
        emit('log_message', "No domain provided for DNSRecon scan.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "dnsrecon": {
            "name": "dnsrecon",
            "install_cmd": {
                "linux": "sudo apt-get install -y dnsrecon",
                "macos": "brew install dnsrecon",
                "windows": "pip install dnsrecon"
            }
        }
    }
```
