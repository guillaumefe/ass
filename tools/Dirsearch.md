#### Step 1: Update `TOOLS_CONFIG`

```python
TOOLS_CONFIG = {
    # Existing tools...
    "dirsearch": {
        "type": "url",
        "description": "Directory and File Enumeration Tool",
        "options": [
            {
                "name": "url",
                "label": "Target URL",
                "type": "text",
                "default": "",
                "explanation": "The target URL for directory enumeration."
            },
            {
                "name": "extensions",
                "label": "File Extensions",
                "type": "text",
                "default": "php,html",
                "explanation": "Specify file extensions to search for."
            }
        ]
    }
}
```

#### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "dirsearch": lambda args: ["dirsearch", "-u"] + args
}
```

#### Step 3: Handle Input Formatting in `handle_scan`

```python
elif scan_type == 'dirsearch':
    args = []
    url = data.get('url')
    extensions = data.get('extensions')
    if url:
        args.append(url)
    if extensions:
        args.append(f"-e {extensions}")
    else:
        emit('log_message', "No URL provided for dirsearch scan.")
```

#### Step 4: Ensure the Tool is Installed

```python
def install_tools():
    tools = {
        # Existing tools...
        "dirsearch": {
            "name": "dirsearch",
            "install_cmd": {
                "linux": "git clone https://github.com/maurosoria/dirsearch.git",
                "macos": "git clone https://github.com/maurosoria/dirsearch.git",
                "windows": "git clone https://github.com/maurosoria/dirsearch.git"
            }
        }
    }
```
