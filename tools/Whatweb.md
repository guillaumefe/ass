#### Step 1: Update TOOLS_CONFIG

```python
"whatweb": {
    "type": "url",
    "description": "Website Fingerprinting Tool (WhatWeb)",
    "options": [
        {
            "name": "aggression",
            "label": "Aggression Level",
            "type": "select",
            "choices": {
                "1": "Stealthy",
                "2": "Normal",
                "3": "Aggressive"
            },
            "default": "1",
            "explanation": "Set the aggression level for scanning."
        }
    ]
}
```

#### Step 2: Add Tool Command to TOOLS_COMMANDS

```python
"whatweb": lambda args: ["whatweb"] + args
```

#### Step 3: Modify handle_scan to Include Tool Logic

```python
elif scan_type == 'whatweb':
    args = []
    target = url
    if 'aggression' in data and data['aggression']:
        args.extend(['--aggression', data['aggression']])
    args.append(target)
```

#### Step 4: Add Installation Command in install_tools

```python
"whatweb": {
    "name": "whatweb",
    "install_cmd": {
        "linux": "sudo apt-get install -y whatweb",
        "darwin": "brew install whatweb",
        "windows": "choco install whatweb"
    }
}
```
