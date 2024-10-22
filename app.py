import os
import subprocess
import sys
import re
import secrets
import platform
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
from urllib.parse import urlparse
import glob
import threading
import signal

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app, async_mode='threading')

def is_running_as_root():
    """Check if the script is running with root privileges"""
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # os.geteuid() is not available on Windows

TOOLS_CONFIG = {
    "nmap": {
        "type": "ip",
        "description": "Port Scan",
        "options": [
            {
                "name": "ports",
                "label": "Ports to scan (e.g., 1-1024)",
                "type": "text",
                "default": "1-1024",
                "explanation": "Enter the port range in the format 'start-end' (e.g., '1-1024'). This defines which ports Nmap will check for active services."
            },
            {
                "name": "nmap_scan_type",
                "label": "Scan Type",
                "type": "select",
                "choices": {
                    "-sS": "SYN Scan",
                    "-sT": "TCP Connect Scan",
                    "-sU": "UDP Scan"
                },
                "default": "-sT",
                "explanation": "Choose the scan type; this controls how Nmap scans ports and influences detection and stealth of the scan."
            },
            {
                "name": "timing_template",
                "label": "Scan Speed",
                "type": "select",
                "choices": {
                    "-T0": "Paranoid (very slow)",
                    "-T1": "Sneaky",
                    "-T2": "Polite",
                    "-T3": "Normal",
                    "-T4": "Aggressive",
                    "-T5": "Insane (very fast)"
                },
                "default": "-T3",
                "explanation": "Select scan speed from -T0 (slowest) to -T5 (fastest). Higher speeds increase scan pace but can increase network load and detection risk."
            },
            {
                "name": "os_detection",
                "label": "Enable OS detection (only if app ihas been launched as root)",
                "type": "checkbox",
                "disabled": not is_running_as_root(),
                "explanation": "Check this to enable Nmap to try and determine the target's operating system by analyzing the responses from open ports."
            }
        ]
    },
    "gobuster": {
        "type": "url",
        "description": "File/Directory Scan",
        "options": [
            {
                "name": "wordlist",
                "label": "Wordlist URL or path",
                "type": "text",
                "default": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt",
                "explanation": "Enter the URL or path to a wordlist file containing directory/file names to test. This defines what paths Gobuster will scan for on the target server."
            },
            {
                "name": "extensions",
                "label": "Extensions to search (e.g., php,txt)",
                "type": "text",
                "explanation": "Specify file extensions to append to names from the wordlist (e.g., 'php,txt'). This allows targeting specific file types."
            },
            {
                "name": "status_codes",
                "label": "HTTP Status Codes to include",
                "type": "text",
                "default": "200,204,301,302,307,401,403",
                "explanation": "Enter the HTTP status codes to consider as valid responses, separated by commas (e.g., '200,301'). Gobuster will only show paths returning these codes."
            }
        ]
    },
    "sqlmap": {
        "type": "url",
        "description": "SQL Injection Scan",
        "options": [
            {
                "name": "risk",
                "label": "Risk level",
                "type": "select",
                "choices": {
                    "1": "1 - Low",
                    "2": "2 - Medium",
                    "3": "3 - High"
                },
                "default": "1",
                "explanation": "Choose the risk level from 1 (low) to 3 (high). Higher risk levels allow for more aggressive tests that may uncover more vulnerabilities but could impact the server."
            },
            {
                "name": "level",
                "label": "Exhaustiveness of tests",
                "type": "select",
                "choices": {
                    "1": "1 - Low",
                    "2": "2 - Medium",
                    "3": "3 - High",
                    "4": "4 - Very High",
                    "5": "5 - Maximum"
                },
                "default": "1",
                "explanation": "Select the depth of tests from 1 (low) to 5 (maximum). Higher levels increase the number of tests and attack vectors used by sqlmap."
            },
            {
                "name": "techniques",
                "label": "Injection techniques",
                "type": "checkboxes",
                "choices": {
                    "B": "Boolean-based blind",
                    "E": "Error-based",
                    "U": "Union query-based",
                    "S": "Stacked queries",
                    "T": "Time-based blind",
                    "Q": "Inline queries"
                },
                "explanation": "Select the SQL injection techniques to use. Sqlmap will apply these methods to try to discover vulnerabilities on the target."
            },
            {
                "name": "data",
                "label": "POST Data",
                "type": "text",
                "default": "",
                "explanation": "Enter the POST data in the format 'param1=value1&param2=value2'. Sqlmap will use this data to test SQL injections in POST requests."
            },
            {
                "name": "cookie",
                "label": "Cookie",
                "type": "text",
                "default": "",
                "explanation": "Enter the cookies to use in the format 'cookie1=value1; cookie2=value2'. Sqlmap will send these cookies with the requests to maintain sessions or access protected areas."
            }
        ]
    }
}

TOOLS_COMMANDS = {
    "nmap": lambda args: ["nmap"] + args,
    "gobuster": lambda args: ["gobuster", "dir"] + args,
    "sqlmap": lambda args: ["sqlmap"] + args
}

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Advanced Security Scanner</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.1/socket.io.min.js"></script>
    <style>
        #output, #logs {
            border: 1px solid #ccc;
            padding: 10px;
            height: 200px;
            overflow-y: auto;
            background-color: #f9f9f9;
            margin-bottom: 20px;
            white-space: pre-wrap;
        }
        .loader {
            display: none;
            border: 4px solid #f3f3f3;
            border-radius: 50%;
            border-top: 4px solid #3498db;
            width: 25px;
            height: 25px;
            animation: spin 1s linear infinite;
            margin-left: 10px;
        }
        #stopScan {
            display: none;
            margin-left: 10px;
        }
        #progress {
            height: 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        #scanBtn:disabled {
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <h1 class="text-center">Advanced Security Scanner</h1>

        <form id="entryForm" class="mt-4">
            <div class="form-group">
                <label for="entry">Enter an IP or URL:</label>
                <input type="text" class="form-control" id="entry" name="entry" placeholder="e.g., 192.168.1.1 or http://example.com" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>

        <div id="testForms" style="display:none;">
            <h3 id="testTitle"></h3>
            <form id="scanForm" class="mt-4">
                <input type="hidden" id="scan_entry" name="entry">
                <div class="form-group">
                    <label for="scan_type">Scan Type:</label>
                    <select class="form-control" id="scan_type" name="scan_type"></select>
                </div>
                <div id="toolOptions"></div>
                <button type="submit" id="scanBtn" class="btn btn-primary">Start Scan</button>
                <button id="stopScan" class="btn btn-danger">Stop Scan</button>
                <div class="loader" id="loader"></div>
            </form>
        </div>

        <div class="mt-4" id="progressContainer" style="display:none;">
            <h3>Scan Progress</h3>
            <div id="progress" class="progress">
                <div id="progress-bar" class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">0%</div>
            </div>
        </div>

        <div class="mt-4">
            <h3>Scan Results</h3>
            <div id="output"></div>
        </div>
        <div class="mt-4">
            <h3>Logs</h3>
            <div id="logs"></div>
        </div>
    </div>
    <script>
        const socket = io();
        const TOOLS_CONFIG = {{ TOOLS_CONFIG | tojson }};
        let currentEntry = '';

        $('#entryForm').on('submit', function(event) {
            event.preventDefault();
            const entry = $('#entry').val().trim();
            currentEntry = entry;

            if (entry === '') {
                alert('Please enter an IP or URL.');
                return;
            }

            $('#output').html('');
            $('#logs').html('');

            let isURL = entry.match(/^(http|https):\/\/[^\s/$.?#].[^\s]*$/i);
            let isIP = entry.match(/^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::\d+)?$/);

            if (isURL || isIP) {
                let ipAddress = entry;
                let portNumber = '';

                if (isIP) {
                    let ipParts = entry.split(':');
                    ipAddress = ipParts[0];
                    portNumber = ipParts[1] || '';
                    $('#testTitle').text('Tests for IP');
                } else {
                    $('#testTitle').text('Tests for URL');
                }

                $('#scan_entry').val(entry);
                $('#testForms').show();
                $('#scan_type').empty();

                let tools = [];
                if (isIP) {
                    tools = Object.entries(TOOLS_CONFIG).filter(([key, value]) => value.type === 'ip');
                } else {
                    tools = Object.entries(TOOLS_CONFIG).filter(([key, value]) => value.type === 'url');
                }

                tools.forEach(([key, value]) => {
                    $('#scan_type').append(`<option value="${key}">${value.description}</option>`);
                });

                loadToolOptions($('#scan_type').val(), portNumber);
            } else {
                alert('Invalid IP or URL.');
                return;
            }
        });

        function loadToolOptions(toolName, portNumber = '') {
            const tool = TOOLS_CONFIG[toolName];
            $('#toolOptions').empty();

            tool.options.forEach(option => {
                let optionHTML = '';
                if (option.type === 'text') {
                    let value = option.default || '';
                    if (option.name === 'ports' && portNumber !== '') {
                        value = portNumber;
                    }
                    optionHTML = `
                        <div class="form-group">
                            <label for="${option.name}">${option.label}</label>
                            <input type="text" class="form-control" id="${option.name}" name="${option.name}" value="${value}">
                            <small class="form-text text-muted">${option.explanation}</small>
                        </div>
                    `;
                } else if (option.type === 'select') {
                    let options = '';
                    for (const [val, label] of Object.entries(option.choices)) {
                        options += `<option value="${val}" ${option.default === val ? 'selected' : ''}>${label}</option>`;
                    }
                    optionHTML = `
                        <div class="form-group">
                            <label for="${option.name}">${option.label}</label>
                            <select class="form-control" id="${option.name}" name="${option.name}">
                                ${options}
                            </select>
                            <small class="form-text text-muted">${option.explanation}</small>
                        </div>
                    `;
                } else if (option.type === 'checkbox') {
                    optionHTML = `
                        <div class="form-group form-check">
                            <input type="checkbox" class="form-check-input" id="${option.name}" name="${option.name}" ${option.disabled}>
                            <label class="form-check-label" for="${option.name}">${option.label}</label>
                            <small class="form-text text-muted">${option.explanation}</small>
                        </div>
                    `;
                } else if (option.type === 'checkboxes') {
                    let checkboxes = '';
                    for (const [val, label] of Object.entries(option.choices)) {
                        checkboxes += `
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="${option.name}[]" value="${val}" id="${option.name}_${val}">
                                <label class="form-check-label" for="${option.name}_${val}">${label}</label>
                            </div>
                        `;
                    }
                    optionHTML = `
                        <div class="form-group">
                            <label>${option.label}</label>
                            ${checkboxes}
                            <small class="form-text text-muted">${option.explanation}</small>
                        </div>
                    `;
                }
                $('#toolOptions').append(optionHTML);
            });
        }

        $('#scan_type').on('change', function() {
            loadToolOptions($(this).val());
        });

        $('#scanForm').on('submit', function(event) {
            event.preventDefault();
            startScan($(this).serializeArray());
        });

        function startScan(formDataArray) {
            let formData = {};
            formDataArray.forEach(item => {
                if (formData[item.name]) {
                    if (Array.isArray(formData[item.name])) {
                        formData[item.name].push(item.value);
                    } else {
                        formData[item.name] = [formData[item.name], item.value];
                    }
                } else {
                    formData[item.name] = item.value;
                }
            });

            $('#scanBtn').prop('disabled', true);
            $('#loader').show();
            $('#stopScan').show();
            $('#progressContainer').show();
            $('#progress-bar').css('width', '0%').attr('aria-valuenow', 0).text('0%');

            socket.emit('start_scan', formData);
        }

        $('#stopScan').on('click', function(event) {
            event.preventDefault();
            socket.emit('stop_scan');
        });

        socket.on('scan_result', function(data) {
            $('#output').append(data + '<br>');
            $('#output').scrollTop($('#output')[0].scrollHeight);
        });

        socket.on('log_message', function(log) {
            $('#logs').append(log + '<br>');
            $('#logs').scrollTop($('#logs')[0].scrollHeight);
        });

        socket.on('progress_update', function(percentage) {
            $('#progress-bar').css('width', percentage + '%').attr('aria-valuenow', percentage).text(percentage + '%');
        });

        socket.on('scan_complete', function() {
            $('#scanBtn').prop('disabled', false);
            $('#loader').hide();
            $('#stopScan').hide();
        });

    </script>
</body>
</html>
"""

current_process = None

def is_tool_installed(name):
    from shutil import which
    return which(name) is not None

def install_tools():
    tools = {
        "nmap": {
            "name": "nmap",
            "install_cmd": {
                "linux": "sudo apt-get install -y nmap",
                "darwin": "brew install nmap",
                "windows": "choco install nmap"
            }
        },
        "gobuster": {
            "name": "gobuster",
            "install_cmd": {
                "linux": "sudo apt-get install -y gobuster",
                "darwin": "brew install gobuster",
                "windows": "choco install gobuster"
            }
        },
        "sqlmap": {
            "name": "sqlmap",
            "install_cmd": {
                "linux": "sudo apt-get install -y sqlmap",
                "darwin": "brew install sqlmap",
                "windows": "choco install sqlmap"
            }
        }
    }
    for tool_name, tool_info in tools.items():
        # Vérifiez si l'outil est installé
        if not is_tool_installed(tool_info['name']):
            platform_name = platform.system().lower()
            install_cmd = tool_info['install_cmd'].get(platform_name)

            if install_cmd:
                print(f"{tool_name} is not installed. Attempting to install...")
                try:
                    subprocess.run(install_cmd, shell=True, check=True)
                    print(f"{tool_name} installed successfully.")
                except subprocess.CalledProcessError:
                    print(f"Failed to install {tool_name}. Please install it manually.")
            else:
                print(f"{tool_name} installation command not available for this platform. Please install it manually.")

def format_input(user_input):
    if user_input.startswith(('http://', 'https://')):
        parsed_url = urlparse(user_input)
        hostname = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == 'https' else 80)
        return hostname, port, user_input
    else:
        ipv4_with_port_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::\d+)?$')
        if ipv4_with_port_pattern.match(user_input):
            if ':' in user_input:
                ip, port = user_input.split(':')
                port = int(port)
            else:
                ip = user_input
                port = 80
            url = f"http://{ip}:{port}"
            return ip, port, url
        else:
            return None, None, None

def fetch_wordlist_from_url(url):
    import requests
    try:
        response = requests.get(url)
        if response.status_code == 200:
            wordlist = response.text.splitlines()
            return wordlist
        else:
            return None
    except:
        return None

@app.route('/')
def index():
    return render_template_string(html_template, TOOLS_CONFIG=TOOLS_CONFIG)

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

@socketio.on('start_scan')
def handle_scan(data):
    user_input = data.get('entry', '')
    scan_type = data.get('scan_type', '')
    ip, port, url = format_input(user_input)

    if not ip:
        emit('log_message', "Invalid IP or URL.")
        emit('scan_complete')
        return

    tool_config = TOOLS_CONFIG.get(scan_type)
    command_func = TOOLS_COMMANDS.get(scan_type)

    if tool_config and command_func:
        args = []
        target = ip if tool_config['type'] == 'ip' else url

        if scan_type == 'nmap':
            args.append('-v')
            args.append('--stats-every')
            args.append('2s')
            if 'timing_template' in data and data['timing_template']:
                args.append(data['timing_template'])
            if 'ports' in data and data['ports']:
                args.extend(['-p', data['ports']])
            if 'nmap_scan_type' in data and data['nmap_scan_type']:
                args.append(data['nmap_scan_type'])
            if 'os_detection' in data and data['os_detection'] == 'on':
                args.append('-O')
            args.append(target)
        elif scan_type == 'gobuster':
            args.extend(['-u', target])
            args.append('--no-tls-validation')
            args.extend(['--status-codes-blacklist', ''])
            if 'wordlist' in data and data['wordlist']:
                wordlist_url = data['wordlist']
                wordlist = fetch_wordlist_from_url(wordlist_url)
                if not wordlist:
                    emit('log_message', "Error downloading wordlist.")
                    emit('scan_complete')
                    return
                with open('temp_wordlist.txt', 'w') as f:
                    f.write('\n'.join(wordlist))
                args.extend(['-w', 'temp_wordlist.txt'])
            else:
                emit('log_message', "Wordlist not specified.")
                emit('scan_complete')
                return
            if 'extensions' in data and data['extensions']:
                args.extend(['-x', data['extensions']])
            if 'status_codes' in data and data['status_codes']:
                args.extend(['--status-codes', data['status_codes']])
        elif scan_type == 'sqlmap':
            args.append('--batch')
            args.extend(['-u', target])
            args.append('--forms')
            if 'risk' in data and data['risk']:
                args.append(f"--risk={data['risk']}")
            if 'level' in data and data['level']:
                args.append(f"--level={data['level']}")
            if 'techniques' in data:
                techniques = data.get('techniques')
                if techniques:
                    args.append(f"--technique={''.join(techniques)}")
            if 'data' in data and data['data']:
                args.extend(['--data', data['data']])
            if 'cookie' in data and data['cookie']:
                args.extend(['--cookie', data['cookie']])
        else:
            emit('log_message', "Tool not recognized.")
            emit('scan_complete')
            return

        command = command_func(args)
        emit('log_message', f"Starting scan with command: {' '.join(command)}")
        run_scan(command)

        if scan_type == 'gobuster' and os.path.exists('temp_wordlist.txt'):
            os.remove('temp_wordlist.txt')
    else:
        emit('log_message', "Tool not recognized.")
        emit('scan_complete')

@socketio.on('stop_scan')
def stop_scan():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        emit('log_message', "Scan stopped by user.")
        emit('scan_complete')
    else:
        emit('log_message', "No scan is currently running.")

if __name__ == '__main__':
    install_tools()
    print("Application running on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000)

