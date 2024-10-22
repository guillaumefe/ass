#### Step 1: Update TOOLS_CONFIG

```python
"wpscan": {
    "type": "url",
    "description": "(WPScan) WordPress Security Scanner",
    "options": [
        {
            "name": "api_token",
            "label": "API Token",
            "type": "text",
            "explanation": "Enter your WPScan API token."
        },
        {
            "name": "enumerate",
            "label": "Enumerate",
            "type": "select",
            "choices": {
                "p": "Plugins",
                "t": "Themes",
                "u": "Users"
            },
            "default": "p",
            "explanation": "Select what to enumerate on the WordPress site."
        }
    ]
}
```

#### Step 2: Add Tool Command to TOOLS_COMMANDS

```python
"wpscan": lambda args: ["wpscan"] + args
```

#### Step 3: Modify handle_scan to Include Tool Logic

```python
elif scan_type == 'wpscan':
    args = []
    target = url
    if 'api_token' in data and data['api_token']:
        args.extend(['--api-token', data['api_token']])
    if 'enumerate' in data and data['enumerate']:
        args.extend(['--enumerate', data['enumerate']])
    args.append("--url")
    args.append(target)
```

#### Step 4: Add Installation Command in install_tools

```python
"wpscan": {
    "name": "wpscan",
    "install_cmd": {
        "linux": "sudo apt-get install -y wpscan",
        "darwin": "brew install wpscan",
        "windows": "choco install wpscan"
    }
}
```
