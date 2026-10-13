
#!/bin/bash

# LSMMS - Linux Server Monitoring and Management System
# Purpose: Create and verify a compressed project backup

set -u

PROJECT_DIR="$HOME/lsmms"
BACKUP_DIR="$PROJECT_DIR/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/lsmms_backup_${TIMESTAMP}.tar.gz"

echo "===== LSMMS Backup System ====="

# Check whether the project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERROR: Project directory not found: $PROJECT_DIR"
    exit 1
fi

# Create the backup directory if it does not exist
if ! mkdir -p "$BACKUP_DIR"; then
    echo "ERROR: Could not create backup directory."
    exit 1
fi

echo "Project: $PROJECT_DIR"
echo "Backup:  $BACKUP_FILE"
echo "Starting backup..."

# Archive project files while excluding unnecessary directories
if tar -czf "$BACKUP_FILE" \
    --exclude='./venv' \
    --exclude='./.git' \
    --exclude='./backups' \
    --exclude='./__pycache__' \
    -C "$PROJECT_DIR" \
    .gitignore requirements.txt scripts app templates static logs; then

    echo "Backup archive created. Verifying..."

    # Verify that the archive can be listed
    if tar -tzf "$BACKUP_FILE" > /dev/null; then
        echo "SUCCESS: Backup created and verified."
        echo "Backup location: $BACKUP_FILE"
        echo "Backup size:"
        du -h "$BACKUP_FILE"
    else
        echo "ERROR: Backup verification failed."
        rm -f "$BACKUP_FILE"
        exit 1
    fi
else
    echo "ERROR: Backup creation failed."
    rm -f "$BACKUP_FILE"
    exit 1
fi

echo "===== Backup Process Completed ====="

