
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
import subprocess
import os

from database import create_table, save_log, get_logs

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
app.secret_key = "lsmms-local-project-key"

PROJECT_DIR = os.path.expanduser("~/lsmms")
BACKUP_DIR = os.path.join(PROJECT_DIR, "backups")
REPORT_DIR = os.path.join(PROJECT_DIR, "reports")

create_table()

MONITORING_SCRIPTS = {
    "system": "scripts/monitoring/system_info.sh",
    "cpu": "scripts/monitoring/cpu_monitor.sh",
    "ram": "scripts/monitoring/ram_monitor.sh",
    "disk": "scripts/monitoring/disk_monitor.sh",
    "service": "scripts/services/service_status.sh"
}

MONITORING_ITEMS = [
    {
        "type": "system",
        "title": "System Information",
        "description": "Hostname, operating system and uptime."
    },
    {
        "type": "cpu",
        "title": "CPU Monitoring",
        "description": "Processor and CPU load information."
    },
    {
        "type": "ram",
        "title": "RAM Monitoring",
        "description": "Memory and swap usage."
    },
    {
        "type": "disk",
        "title": "Disk Usage",
        "description": "Filesystem space information."
    },
    {
        "type": "service",
        "title": "SSH Service",
        "description": "SSH service status."
    }
]

VALID_VIEWS = {
    "overview", "monitoring", "services",
    "backups", "reports", "history"
}


def dashboard_redirect(default_view):
    view = request.form.get("view", default_view)

    if view not in VALID_VIEWS:
        view = default_view

    return redirect(url_for("home", view=view))


def run_script(script_path, input_text=None, timeout=60):
    return subprocess.run(
        ["bash", os.path.join(PROJECT_DIR, script_path)],
        input=input_text,
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        timeout=timeout
    )


def list_files(folder, extension):
    if not os.path.isdir(folder):
        return []

    return sorted(
        [
            name for name in os.listdir(folder)
            if name.endswith(extension)
            and os.path.isfile(os.path.join(folder, name))
        ],
        reverse=True
    )


@app.route("/")
def home():
    logs = get_logs()[:20]

    latest = {}

    for log in logs:
        if log[1] not in latest:
            latest[log[1]] = {
                "output": log[2],
                "created_at": log[3]
            }

    return render_template(
        "index.html",
        monitoring_items=MONITORING_ITEMS,
        latest=latest,
        logs=logs,
        backup_files=list_files(BACKUP_DIR, ".tar.gz"),
        report_files=list_files(REPORT_DIR, ".txt")
    )


@app.route("/monitor/<monitoring_type>", methods=["POST"])
def run_monitoring(monitoring_type):
    if monitoring_type not in MONITORING_SCRIPTS:
        abort(404)

    try:
        result = run_script(MONITORING_SCRIPTS[monitoring_type])
    except subprocess.TimeoutExpired:
        flash("Monitoring script timed out.")
        return dashboard_redirect("monitoring")

    if result.returncode == 0:
        save_log(monitoring_type, result.stdout)
        flash(monitoring_type.upper() + " monitoring refreshed and saved.")
    else:
        flash("Monitoring failed: " + result.stderr[:300])

    return dashboard_redirect("monitoring")


@app.route("/monitor/all", methods=["POST"])
def run_all_monitoring():
    successful = []
    failed = []

    for monitoring_type, script_path in MONITORING_SCRIPTS.items():
        try:
            result = run_script(script_path)
        except subprocess.TimeoutExpired:
            failed.append(monitoring_type.upper() + " (timeout)")
            continue

        if result.returncode == 0:
            save_log(monitoring_type, result.stdout)
            successful.append(monitoring_type.upper())
        else:
            failed.append(monitoring_type.upper())

    if successful:
        flash(
            "Refreshed and saved: " + ", ".join(successful) + "."
        )

    if failed:
        flash(
            "Could not refresh: " + ", ".join(failed) + "."
        )

    return dashboard_redirect("monitoring")


@app.route("/service/manage", methods=["POST"])
def manage_service():
    actions = {
        "start": "1",
        "stop": "2",
        "restart": "3"
    }

    action = request.form.get("action", "")

    if action not in actions:
        abort(400)

    try:
        result = run_script(
            "scripts/services/service_manage.sh",
            input_text=actions[action] + "\n",
            timeout=30
        )
    except subprocess.TimeoutExpired:
        flash("Service action timed out.")
        return dashboard_redirect("services")

    output = (result.stdout + "\n" + result.stderr).strip()

    if (
        result.returncode != 0
        or "Failed to " in output
        or "sudo:" in output
    ):
        flash("Service action failed. Check permissions. " + output[-300:])
    else:
        flash(output[-500:] or "Service action completed.")

    return dashboard_redirect("services")


@app.route("/backup", methods=["POST"])
def run_backup():
    try:
        result = run_script(
            "scripts/backup/backup.sh",
            timeout=120
        )
    except subprocess.TimeoutExpired:
        flash("Backup process timed out.")
        return dashboard_redirect("backups")

    if result.returncode == 0:
        flash("Backup completed. See Available Backups below.")
    else:
        flash("Backup failed: " + (result.stderr or result.stdout)[-300:])

    return dashboard_redirect("backups")


@app.route("/report", methods=["POST"])
def generate_report():
    try:
        result = run_script(
            "scripts/reports/generate_report.sh",
            timeout=60
        )
    except subprocess.TimeoutExpired:
        flash("Report generation timed out.")
        return dashboard_redirect("reports")

    if result.returncode == 0:
        flash("System report generated. See Available Reports below.")
    else:
        flash(
            "Report generation failed: "
            + (result.stderr or result.stdout)[-300:]
        )

    return dashboard_redirect("reports")


@app.route("/download/<file_type>/<filename>")
def download_file(file_type, filename):
    if os.path.basename(filename) != filename:
        abort(404)

    if file_type == "backup" and filename.endswith(".tar.gz"):
        folder = BACKUP_DIR
    elif file_type == "report" and filename.endswith(".txt"):
        folder = REPORT_DIR
    else:
        abort(404)

    return send_from_directory(
        folder,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
