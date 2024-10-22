#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "anew": {
        "type": "url",
        "description": "(Anew) Unique URL Finding Tool",
        "options": [
            {
                "name": "urls",
                "label": "List of URLs",
                "type": "text",
                "default": "",
                "explanation": "The list of URLs to filter unique results."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "anew": lambda args: ["anew"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'anew':
    args = []
    urls = data.get('urls')
    if urls:
        args.append(urls)
    else:
        emit('log_message', "No URLs provided for anew.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "anew": {
            "name": "anew",
            "install_cmd": {
                "linux": "sudo apt-get install -y anew",
                "macos": "brew install anew",
                "windows": "go get -u github.com/tomnomnom/anew"
            }
        }
    }
```
