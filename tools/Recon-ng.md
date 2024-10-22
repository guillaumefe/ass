#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "reconng": {
        "type": "url",
        "description": "(Recon-ng) Web Reconnaissance Framework",
        "options": [
            {
                "name": "domain",
                "label": "Domain to search",
                "type": "text",
                "default": "",
                "explanation": "The domain for reconnaissance."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "reconng": lambda args: ["recon-ng", "-r"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'reconng':
    args = []
    target = data.get('domain')
    if target:
        args.append(target)
    else:
        emit('log_message', "No domain provided for Recon-ng scan.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "reconng": {
            "name": "reconng",
            "install_cmd": {
                "linux": "sudo apt-get install -y recon-ng",
                "macos": "brew install recon-ng",
                "windows": "pip install recon-ng"
            }
        }
    }
```
