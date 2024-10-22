#### Sublist3r

#### Step 1: Update `TOOLS_CONFIG`

\```python
TOOLS_CONFIG = {
    # Existing tools...
    "sublist3r": {
        "type": "url",
        "description": "Subdomain Enumeration Tool",
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
\```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

\```python
TOOLS_COMMANDS = {
    # Existing tools...
    "sublist3r": lambda args: ["sublist3r", "-d"] + args
}
\```

#### Step 3: Handle Input Formatting in `handle_scan`

\```python
elif scan_type == 'sublist3r':
    args = []
    target = data.get('domains')
    if target:
        args.append(target)
    else:
        emit('log_message', "No domain provided for sublist3r scan.")
\```

#### Step 4: Ensure the Tool is Installed

\```python
def install_tools():
    tools = {
        # Existing tools...
        "sublist3r": {
            "name": "sublist3r",
            "install_cmd": {
                "linux": "sudo apt-get install -y sublist3r",
                "macos": "brew install sublist3r",
                "windows": "pip install sublist3r"
            }
        }
    }
\```
