# Advanced Security Scanner

## Introduction

This project is a web-based security scanner application that allows users to run various security tests such as port scans, file/directory scans, and SQL injection scans. The application utilizes tools like `nmap`, `gobuster`, and `sqlmap` to perform the scans and provides real-time feedback on progress and logs through a web interface built with Flask and Flask-SocketIO.

## Features

- **Port Scanning (Nmap)**: Scan open ports on a target IP with different scan types (SYN, TCP, UDP).
- **File/Directory Scanning (Gobuster)**: Search for files and directories on a target web server.
- **SQL Injection Testing (SQLMap)**: Test for SQL injection vulnerabilities.
- **Real-Time Logs**: Get immediate feedback during the scan.
- **Progress Bar**: Shows scan progress.
- **Stop Scan Feature**: Stop scans manually if needed.

## Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO
- Nmap
- Gobuster
- SQLMap

Ensure these tools are installed and accessible from your system's PATH.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/advanced-security-scanner.git
   cd advanced-security-scanner
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   sudo python app.py  # Use 'sudo' if root privileges are required
   ```

4. **Access the application in your browser at** `http://localhost:5000`.

## Adding New Tools

You can extend the functionality of this application by adding new security tools. Follow the comprehensive steps below to integrate a new tool into the system.

### Overview

Adding a new tool involves:

1. **Defining the tool's configuration in `TOOLS_CONFIG`.**
2. **Specifying how the tool should be executed in `TOOLS_COMMANDS`.**
3. **Ensuring the tool is installed on the system or providing installation instructions.**
4. **Handling any specific input formatting or output parsing if necessary.**

### Step-by-Step Guide

#### **Step 1: Update `TOOLS_CONFIG`**

The `TOOLS_CONFIG` dictionary in `app.py` defines each tool and its options. Each entry should include:

- **Key:** The tool's name (as a string).
- **Type:** Defines the target format (`ip`, `url`, etc.).
- **Description:** Briefly describes the tool's function.
- **Options:** A list of parameters that the user can customize for the scan.

**Example:**

```python
TOOLS_CONFIG = {
    # Existing tools...
    "newtool": {
        "type": "ip",  # or 'url', depending on the target
        "description": "New Tool Description",
        "options": [
            {
                "name": "parameter_name",
                "label": "Parameter Label",
                "type": "text",  # 'text', 'select', 'checkbox', 'checkboxes'
                "default": "default_value",
                "explanation": "Explain the purpose of this option."
            },
            # Add more options as needed
        ]
    },
    # Additional tools...
}
```

### Step 2: Add the Tool Command in `TOOLS_COMMANDS`

Define how the tool is executed by adding an entry to the `TOOLS_COMMANDS` dictionary.

**Example:**

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "newtool": lambda args: ["newtool_command"] + args,
    # Additional tools...
}
```

**Explanation:**

- The lambda function takes a list of arguments (`args`) and constructs the command to execute.
- Replace `"newtool_command"` with the actual command or path to the tool's executable.
- Ensure that any necessary flags or parameters are included appropriately.

### Step 3: Handle Input Formatting in `handle_scan`

In the `handle_scan` function within `app.py`, you may need to adjust how the user's input is processed for your tool.

**Example:**

```python
@socketio.on('start_scan')
def handle_scan(data):
    # Existing code...
    elif scan_type == 'newtool':
        args = []
        target = ip if tool_config['type'] == 'ip' else url

        # Add your tool's specific argument handling
        if 'parameter_name' in data and data['parameter_name']:
            args.extend(['--parameter', data['parameter_name']])
        # Handle other options as needed

        args.append(target)
    # Rest of the code...
```

**Note:**

- Ensure that the options from `TOOLS_CONFIG` are correctly mapped to command-line arguments for your tool.
- Handle different types of inputs (`text`, `select`, `checkbox`, `checkboxes`) appropriately.
- Validate and sanitize inputs to prevent security issues.

### Step 4: Ensure the Tool is Installed

Check if the tool is installed on the system in the `install_tools` function.

**Example:**

```python
def install_tools():
    tools = {
        # Existing tools...
        "newtool": "newtool_command"
    }
    for tool_name, command in tools.items():
        if not is_tool_installed(command):
            print(f"{tool_name} is not installed. Please install it manually.")
            # Optionally, you can automate the installation:
            # if platform.system() == 'Linux':
            #     os.system("sudo apt-get install newtool")
            # elif platform.system() == 'Darwin':
            #     os.system("brew install newtool")
            # elif platform.system() == 'Windows':
            #     os.system("choco install newtool")
```

**Alternative: Automate Installation**

You can automate the installation process by including the installation commands directly. Be cautious with this approach, as it may require elevated privileges.

### Step 5: Update the Frontend (Optional)

The frontend dynamically generates forms based on `TOOLS_CONFIG`. If your tool requires special handling, you might need to update the JavaScript code.

However, in most cases, defining the options in `TOOLS_CONFIG` is sufficient, and the UI will adapt accordingly.

### Step 6: Test the New Tool

- **Run the Application:**

  ```bash
  sudo python app.py
  ```

- **Access the Web Interface:**

  Navigate to `http://localhost:5000` in your browser.

- **Test the Tool:**

  - Enter a valid IP or URL based on your tool's target type.
  - Select your new tool from the "Scan Type" dropdown.
  - Fill in any additional options you defined.
  - Start the scan and monitor the logs and output.

- **Verify:**

  - Ensure that the tool runs without errors.
  - Check that the command constructed is correct.
  - Confirm that the options are passed as intended.
  - Validate that the output is displayed appropriately.

### Step 7: Handle Output Parsing (If Necessary)

If your tool's output requires special parsing or handling, you might need to adjust the `run_scan` function.

**Example:**

```python
def run_scan(command):
    global current_process
    try:
        current_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        socketio.emit('progress_update', 0)

        for line in iter(current_process.stdout.readline, ''):
            if line:
                # Add custom parsing here if needed
                socketio.emit('scan_result', line.strip())
                socketio.sleep(0)

        current_process.stdout.close()
        current_process.wait()
        socketio.emit('progress_update', 100)
        socketio.emit('log_message', "Scan complete.")
        socketio.emit('scan_complete')
    except Exception as e:
        socketio.emit('log_message', f"Error during scan execution: {str(e)}")
        socketio.emit('scan_complete')
    finally:
        current_process = None
```

**Notes:**

- **Custom Parsing:** If you need to extract specific information from the tool's output, you can implement parsing logic within the loop.
- **Error Handling:** Ensure that any exceptions are caught, and appropriate messages are emitted to the user.

### Example: Adding Masscan Tool

To illustrate, here's how you might add `masscan`, a fast port scanner.

#### **1. Update `TOOLS_CONFIG`**

```python
TOOLS_CONFIG = {
    # Existing tools...
    "masscan": {
        "type": "ip",
        "description": "Fast Port Scanner",
        "options": [
            {
                "name": "ports",
                "label": "Ports to scan (e.g., 1-65535)",
                "type": "text",
                "default": "1-1000",
                "explanation": "Specify the range of ports to scan."
            },
            {
                "name": "rate",
                "label": "Packets per second",
                "type": "text",
                "default": "1000",
                "explanation": "Set the rate of packets per second."
            }
        ]
    }
}
```

#### **2. Add the Tool Command**

```python
TOOLS_COMMANDS = {
    # Existing tools...
    "masscan": lambda args: ["masscan"] + args
}
```

#### **3. Handle Input Formatting in `handle_scan`**

```python
elif scan_type == 'masscan':
    args = []
    target = ip  # Masscan operates on IP addresses. The ip parameter contains the client's IP address, so we need to use it directly.
    if 'ports' in data and data['ports']:
        args.extend(['-p', data['ports']])
    if 'rate' in data and data['rate']:
        args.extend(['--rate', data['rate']])
    args.extend(['--open', target])
```

#### **4. Ensure the Tool is Installed**

```python
def install_tools():
    tools = {
        # Existing tools...
        "masscan": {
            "name": "masscan",
            "install_cmd": {
                "linux": "sudo apt-get install -y masscan",
                "darwin": "brew install masscan",
                "windows": "choco install masscan"
            }
        }
    }
```

#### **5. Test the Tool**

Follow the steps in **Step 6** and **Step 7** to test and validate the integration.

## License

This project is licensed under the GNU General Public License.
