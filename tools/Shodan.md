#### Shodan

#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "shodan": {
        "type": "url",
        "description": "Shodan Search Tool",
        "options": [
            {
                "name": "query",
                "label": "Search Query",
                "type": "text",
                "default": "",
                "explanation": "The Shodan search query to use."
            },
            {
                "name": "apikey",
                "label": "API Key",
                "type": "text",
                "default": "",
                "explanation": "Your Shodan API Key."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "shodan": lambda args: ["shodan", "search", "--fields", "ip_str,port,org", "--limit", "10"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'shodan':
    args = []
    query = data.get('query')
    apikey = data.get('apikey')
    if query and apikey:
        args.append(query)
        args.append(apikey)
    else:
        emit('log_message', "Query and API key must be provided.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "shodan": {
            "name": "shodan",
            "install_cmd": {
                "linux": "pip install shodan",
                "macos": "pip install shodan",
                "windows": "pip install shodan"
            }
        }
    }
```
