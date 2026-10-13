
#!/bin/bash

SERVICE="cron"

echo "===== Service Management ====="
echo "Service: $SERVICE"
echo "1. Start Service"
echo "2. Stop Service"
echo "3. Restart Service"
echo "4. Check Status"

read -r -p "Enter your choice: " choice

case "$choice" in
    1)
        if sudo systemctl start "$SERVICE"; then
            echo "$SERVICE started successfully."
        else
            echo "Failed to start $SERVICE."
        fi
        ;;
    2)
        if sudo systemctl stop "$SERVICE"; then
            echo "$SERVICE stopped successfully."
        else
            echo "Failed to stop $SERVICE."
        fi
        ;;
    3)
        if sudo systemctl restart "$SERVICE"; then
            echo "$SERVICE restarted successfully."
        else
            echo "Failed to restart $SERVICE."
        fi
        ;;
    4)
        STATUS=$(systemctl is-active "$SERVICE" 2>/dev/null)
        echo "$SERVICE status: $STATUS"
        ;;
    *)
        echo "Invalid choice! Enter 1, 2, 3 or 4."
        ;;
esac

