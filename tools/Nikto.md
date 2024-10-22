#### Step 1: Update TOOLS_CONFIG

```python
"nikto": {
    "type": "url",
    "description": "(Nikto) Web Vulnerability Scanner",
    "options": [
        {
            "name": "ssl",
            "label": "Use SSL",
            "type": "checkbox",
            "explanation": "Check to enforce SSL during the scan."
        },
        {
            "name": "timeout",
            "label": "Timeout (seconds)",
            "type": "text",
            "default": "10",
            "explanation": "Set the request timeout duration."
        }
    ]
}
```

#### Step 2: Add Tool Command to TOOLS_COMMANDS

```python
"nikto": lambda args: ["nikto"] + args
```

#### Step 3: Modify handle_scan to Include Tool Logic

```python
elif scan_type == 'nikto':
    args = []
    target = url
    if 'ssl' in data and data['ssl'] == 'on':
        args.append("-ssl")
    if 'timeout' in data and data['timeout']:
        args.extend(["-timeout", data['timeout']])
    args.append("-host")
    args.append(target)
```

#### Step 4: Add Installation Command in install_tools

```python
"nikto": {
    "name": "nikto",
    "install_cmd": {
        "linux": "sudo apt-get install -y nikto",
        "darwin": "brew install nikto",
        "windows": "choco install nikto"
    }
}
```
