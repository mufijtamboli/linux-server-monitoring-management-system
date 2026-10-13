
#!/bin/bash

# LSMMS - Complete System Report

PROJECT_DIR="$HOME/lsmms"
REPORT_DIR="$PROJECT_DIR/reports"
BACKUP_DIR="$PROJECT_DIR/backups"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="$REPORT_DIR/system_report_${TIMESTAMP}.txt"

echo "===== LSMMS System Report ====="

# Ensure required folders exist
mkdir -p "$REPORT_DIR" "$BACKUP_DIR"

# Report header
echo "LSMMS SYSTEM REPORT" > "$REPORT_FILE"
echo "Generated on: $(date)" >> "$REPORT_FILE"
echo "================================" >> "$REPORT_FILE"

# System information
echo "" >> "$REPORT_FILE"
echo "===== SYSTEM INFORMATION =====" >> "$REPORT_FILE"
bash "$PROJECT_DIR/scripts/monitoring/system_info.sh" >> "$REPORT_FILE" 2>&1

# CPU information
echo "" >> "$REPORT_FILE"
echo "===== CPU INFORMATION =====" >> "$REPORT_FILE"
bash "$PROJECT_DIR/scripts/monitoring/cpu_monitor.sh" >> "$REPORT_FILE" 2>&1

# RAM information
echo "" >> "$REPORT_FILE"
echo "===== RAM INFORMATION =====" >> "$REPORT_FILE"
bash "$PROJECT_DIR/scripts/monitoring/ram_monitor.sh" >> "$REPORT_FILE" 2>&1

# Disk information
echo "" >> "$REPORT_FILE"
echo "===== DISK INFORMATION =====" >> "$REPORT_FILE"
bash "$PROJECT_DIR/scripts/monitoring/disk_monitor.sh" >> "$REPORT_FILE" 2>&1

# SSH service status
echo "" >> "$REPORT_FILE"
echo "===== SSH SERVICE STATUS =====" >> "$REPORT_FILE"
bash "$PROJECT_DIR/scripts/services/service_status.sh" >> "$REPORT_FILE" 2>&1

# Cron service status
echo "" >> "$REPORT_FILE"
echo "===== CRON SERVICE STATUS =====" >> "$REPORT_FILE"
CRON_STATUS=$(systemctl is-active cron 2>/dev/null)

if [ -z "$CRON_STATUS" ]; then
    CRON_STATUS="unknown"
fi

echo "Cron Status: $CRON_STATUS" >> "$REPORT_FILE"

# Backup summary
echo "" >> "$REPORT_FILE"
echo "===== BACKUP SUMMARY =====" >> "$REPORT_FILE"

BACKUP_COUNT=$(find "$BACKUP_DIR" -maxdepth 1 -type f -name '*.tar.gz' | wc -l)

echo "Total Backup Archives: $BACKUP_COUNT" >> "$REPORT_FILE"

LATEST_BACKUP=$(find "$BACKUP_DIR" -maxdepth 1 -type f -name '*.tar.gz' -printf '%T@ %f\n' | sort -nr | head -n 1 | cut -d' ' -f2-)

if [ -n "$LATEST_BACKUP" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$LATEST_BACKUP" | cut -f1)
    echo "Latest Backup: $LATEST_BACKUP" >> "$REPORT_FILE"
    echo "Latest Backup Size: $BACKUP_SIZE" >> "$REPORT_FILE"
else
    echo "Latest Backup: None available" >> "$REPORT_FILE"
fi

# Verify the report
if [ -s "$REPORT_FILE" ]; then
    echo "SUCCESS: System report generated."
    echo "Report location: $REPORT_FILE"
    echo "Report size:"
    du -h "$REPORT_FILE"
else
    echo "ERROR: Report could not be generated."
    exit 1
fi

echo "===== Report Process Completed ====="
