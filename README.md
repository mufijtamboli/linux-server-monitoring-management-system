
# LSMMS — Linux Server Monitoring and Management System

LSMMS is a Linux-focused server monitoring and management project built using Bash, Python, Flask, and SQLite.

The project provides a web dashboard to monitor basic Linux server information, manage a configured service, create project backups, generate system reports, and view monitoring history.

## Features

### 1. System Monitoring
- System hostname, operating system, uptime, and date/time
- CPU model and load average
- RAM and swap usage
- Disk and filesystem usage
- SSH service status

### 2. Service Management
- Start the configured cron service
- Stop the configured cron service
- Restart the configured cron service
- Display service action results on the dashboard

Service controls require appropriate Linux permissions. SSH is monitored, but the dashboard does not provide an option to stop SSH.

### 3. Project Backup
- Create a timestamped compressed `.tar.gz` archive
- Verify the created archive
- Display available backup files
- Download backup archives from the dashboard

The current backup script archives selected project files. It does not include the SQLite database file or generated report files.

### 4. System Report Generation
- Generate a timestamped text report
- Include system, CPU, RAM, and disk information
- Include SSH and cron service status
- Include a summary of available project backup archives
- Download generated reports from the dashboard

### 5. SQLite Monitoring History
- Save successful monitoring results
- Store the monitoring type and timestamp
- Display recent saved records
- View the full output associated with each record

### 6. Web Dashboard
- Separate sections for Overview, Monitoring, Services, Backups, Reports, and History
- Refresh individual monitoring items
- Refresh all monitoring items together
- Display success or failure messages for operations

## Technology Stack

- **Operating System:** Debian GNU/Linux 13
- **Scripting:** Bash
- **Backend:** Python and Flask
- **Database:** SQLite
- **Frontend:** HTML and CSS
- **Version Control:** Git

Python is mainly used to connect the Bash scripts with Flask and SQLite. Linux monitoring and administration tasks are handled by Bash scripts.

## Project Structure

```text
lsmms/
├── app/
│   ├── app.py
│   └── database.py
├── backups/
├── logs/
├── reports/
├── scripts/
│   ├── backup/
│   │   └── backup.sh
│   ├── monitoring/
│   │   ├── system_info.sh
│   │   ├── cpu_monitor.sh
│   │   ├── ram_monitor.sh
│   │   └── disk_monitor.sh
│   ├── reports/
│   │   └── generate_report.sh
│   └── services/
│       ├── service_status.sh
│       └── service_manage.sh
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── requirements.txt
├── .gitignore
└── README.md
```

The SQLite database file, `lsmms.db`, is created in the project root when the database code runs. The `venv/` directory contains the Python virtual environment and is not included in the repository.

## Prerequisites

- Debian Linux server
- Python 3
- Bash
- Flask
- VirtualBox, if running the server inside a virtual machine
- SSH access to the Debian VM when connecting from the host OS

SQLite is provided through Python's built-in `sqlite3` module, so a separate SQLite server is not required.

## Setup and Installation

Open a terminal on the Debian server and enter the project directory:

```bash
cd ~/lsmms
```

Activate the Python virtual environment:

```bash
source ~/lsmms/venv/bin/activate
```

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

Check the Python files:

```bash
python -m py_compile app/app.py app/database.py
```

## Start the Web Dashboard

Start Flask from the project directory:

```bash
python app/app.py
```

The application listens on:

```text
http://127.0.0.1:5000/
```

Keep the Flask terminal running while using the dashboard.

### Accessing the Dashboard from the Omarchy Host

If the Debian VM uses VirtualBox port forwarding from host port `2222` to guest SSH port `22`, open a separate terminal on the Omarchy host and run:

```bash
ssh -L 5000:127.0.0.1:5000 -p 2222 mufij@127.0.0.1
```

Keep this SSH session open. Then open the following address in the host browser:

```text
http://127.0.0.1:5000/
```

Replace the SSH username or port if your environment uses different settings.

## Main Bash Scripts

| Script | Purpose |
|---|---|
| `system_info.sh` | Collect system information |
| `cpu_monitor.sh` | Display CPU information and load average |
| `ram_monitor.sh` | Display memory and swap usage |
| `disk_monitor.sh` | Display filesystem usage |
| `service_status.sh` | Check SSH service status |
| `service_manage.sh` | Start, stop, restart, or check the configured cron service |
| `backup.sh` | Create and verify a compressed project archive |
| `generate_report.sh` | Generate a consolidated system report |

## Testing

The project has been manually tested for:

- Bash script syntax
- Monitoring script execution
- Flask backend startup and monitoring endpoints
- SQLite table creation and saving monitoring records
- Dashboard monitoring refresh operations
- Refresh All Data
- Cron service management
- Project backup creation
- System report generation
- Backup and report downloads
- Dashboard navigation and monitoring history

## Security Notes

- The Flask server is configured to listen on `127.0.0.1` for local development.
- Use SSH port forwarding to access the dashboard from the host.
- Service management requires administrative permissions.
- The lab setup uses a restricted sudo rule for cron service actions. Review and adapt permissions before using the project on another server.
- Do not commit passwords, secrets, virtual environments, database files, or generated archives to a public repository.

## Limitations and Future Scope

- Full Linux server backup and recovery can be added in the future.
- Project backups can be extended to include the SQLite database and generated reports.
- Automated periodic monitoring and alerting can be added.
- Monitoring history can be extended with graphical trends and more detailed analysis.

## Project Summary

LSMMS demonstrates how Bash-based Linux administration scripts can be connected to a lightweight Flask web interface and SQLite database to provide a practical server monitoring and management system.
