# Advanced Security Scanner

## Introduction

This project is a web-based security scanner application, allowing users to run various security tests such as port scans, file/directory scans, and SQL injection scans. The application uses tools like `nmap`, `gobuster`, and `sqlmap` to perform the scans and provides real-time feedback on progress and logs through a web interface built with Flask and Flask-SocketIO.

## Features

- **Port Scanning (Nmap):** Scan open ports on a target IP with different scan types (SYN, TCP, UDP).
- **File/Directory Scanning (Gobuster):** Search for files and directories on a target web server.
- **SQL Injection Testing (SQLMap):** Test for SQL injection vulnerabilities.
- **Real-Time Logs:** Get immediate feedback during the scan.
- **Progress Bar:** Shows scan progress.
- **Stop Scan Feature:** Stop scans manually if needed.

## Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO
- Nmap
- Gobuster
- SQLMap

Make sure these tools are installed and accessible from your system's PATH.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/my-ass.git
   cd my-ass
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   sudo python app.py  # Use 'sudo' to ensure root privileges are available if needed
   ```

4. Access the application in your browser at `http://localhost:5000`.

## Adding New Tools

You can extend the functionality of this application by adding new security tools. Follow the steps below to integrate a new tool into the system.

### Step 1: Update `TOOLS_CONFIG`

In the `app.py` file, the `TOOLS_CONFIG` dictionary defines each tool and its options. To add a new tool, you will need to create an entry similar to the existing ones for Nmap, Gobuster, and SQLMap. Each tool should have:

- **Type:** (`ip`, `url`, etc.) defines the target format.
- **Description:** Briefly describe the tool's function.
- **Options:** A list of parameters that the user can customize for the scan.

Example:

```python
"newtool": {
    "type": "ip",  # or 'url', depending on the target
    "description": "New Tool Description",
    "options": [
        {
            "name": "parameter_name",
            "label": "Parameter Label",
            "type": "text",
            "default": "default_value",
            "explanation": "Explain the purpose of this option."
        },
        # Add more options as needed
    ]
}
```

### Step 2: Add the Tool Command

In the `TOOLS_COMMANDS` dictionary, define how the tool is executed by adding a lambda function to generate the appropriate command based on the user's input.

Example:

```python
"newtool": lambda args: ["newtool_command"] + args
```

## License

This project is licensed under the MIT License.

