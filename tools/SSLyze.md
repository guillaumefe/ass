#### Step 1: Update TOOLS_CONFIG

```python
"sslyze": {
    "type": "url",
    "description": "(SSLyze) SSL/TLS Configuration Scanner",
    "options": [
        {
            "name": "certinfo",
            "label": "Certificate Information",
            "type": "checkbox",
            "explanation": "Check to include detailed certificate information."
        },
        {
            "name": "reneg",
            "label": "Test Renegotiation",
            "type": "checkbox",
            "explanation": "Check to test for TLS renegotiation support."
        }
    ]
}
```

#### Step 2: Add Tool Command to TOOLS_COMMANDS

```python
"sslyze": lambda args: ["sslyze"] + args
```

#### Step 3: Modify handle_scan to Include Tool Logic

```python
elif scan_type == 'sslyze':
    args = []
    target = url
    if 'certinfo' in data and data['certinfo'] == 'on':
        args.append("--certinfo")
    if 'reneg' in data and data['reneg'] == 'on':
        args.append("--reneg")
    args.append(target)
```

#### Step 4: Add Installation Command in install_tools

```python
"sslyze": {
    "name": "sslyze",
    "install_cmd": {
        "linux": "sudo apt-get install -y sslyze",
        "darwin": "brew install sslyze",
        "windows": "choco install sslyze"
    }
}
```
