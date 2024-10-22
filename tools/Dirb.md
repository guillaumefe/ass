#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "dirb": {
        "type": "url",
        "description": "Directory Scanner",
        "options": [
            {
                "name": "wordlist",
                "label": "Wordlist Path",
                "type": "text",
                "default": "/usr/share/dirb/wordlists/common.txt",
                "explanation": "Specify the wordlist for directory scanning."
            },
            {
                "name": "extensions",
                "label": "File Extensions",
                "type": "text",
                "default": "php,html,txt",
                "explanation": "Comma-separated file extensions to scan."
            },
            {
                "name": "proxy",
                "label": "Proxy URL",
                "type": "text",
                "default": "",
                "explanation": "Optional: Proxy URL to route the requests."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "dirb": lambda args: ["dirb"] + args,
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'dirb':
    args = []
    target = url  # Dirb works with URLs.
    
    if 'wordlist' in data and data['wordlist']:
        args.append(data['wordlist'])
    else:
        args.append('/usr/share/dirb/wordlists/common.txt')  # Default wordlist
    
    if 'extensions' in data and data['extensions']:
        args.extend(['-X', data['extensions']])
        
    if 'proxy' in data and data['proxy']:
        args.extend(['-p', data['proxy']])
        
    args.append(target)
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "dirb": {
            "name": "dirb",
            "install_cmd": {
                "linux": "sudo apt-get install -y dirb",
                "darwin": "curl -L https://sourceforge.net/projects/dirb/files/dirb/2.22/dirb222.tar.gz/download -o dirb222.tar.gz && tar xvzf dirb222.tar.gz && cd dirb222 && ./configure --prefix=$HOME/local && make && make install",
                "windows": "choco install dirb"
            }
        }
    }
```
