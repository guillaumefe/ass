#### TheHarvester

#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "theharvester": {
        "type": "url",
        "description": "Email and subdomain OSINT Tool",
        "options": [
            {
                "name": "domain",
                "label": "Domain to search",
                "type": "text",
                "default": "",
                "explanation": "The target domain to search for emails and subdomains."
            },
            {
                "name": "source",
                "label": "Data Source",
                "type": "select",
                "choices": {
                    "google": "Google",
                    "bing": "Bing",
                    "all": "All"
                },
                "default": "all",
                "explanation": "Choose the data source to gather information from."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "theharvester": lambda args: ["theharvester", "-d", args[0], "-b", args[1]]
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'theharvester':
    args = []
    domain = data.get('domain')
    source = data.get('source')
    if domain and source:
        args.append(domain)
        args.append(source)
    else:
        emit('log_message', "Domain and source must be provided.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "theharvester": {
            "name": "theharvester",
            "install_cmd": {
                "linux": "sudo apt-get install -y theharvester",
                "macos": "brew install theharvester",
                "windows": "pip install theharvester"
            }
        }
    }
```

