#### Step 1: Update TOOLS_CONFIG

```python
"masscan": {
    "type": "ip",
    "description": "Fast Port Scanner (Masscan)",
    "options": [
        {
            "name": "ports",
            "label": "Ports to scan (e.g., 1-65535)",
            "type": "text",
            "default": "1-1000",
            "explanation": "Specify the port range for scanning."
        },
        {
            "name": "rate",
            "label": "Packets per second",
            "type": "text",
            "default": "1000",
            "explanation": "Set the scan rate in packets per second."
        }
    ]
}
```

#### Step 2: Add Tool Command to TOOLS_COMMANDS

```python
"masscan": lambda args: ["masscan"] + args
```

#### Step 3: Modify handle_scan to Include Tool Logic

```python
elif scan_type == 'masscan':
    args = []
    target = ip  # Masscan requires IP addresses
    if 'ports' in data and data['ports']:
        args.extend(['-p', data['ports']])
    if 'rate' in data and data['rate']:
        args.extend(['--rate', data['rate']])
    args.extend([target])
```

#### Step 4: Add Installation Command in install_tools

```python
"masscan": {
    "name": "masscan",
    "install_cmd": {
        "linux": "sudo apt-get install -y masscan",
        "darwin": "brew install masscan",
        "windows": "choco install masscan"
    }
}
```
