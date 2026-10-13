
#!/bin/bash

SERVICE="ssh"

echo "===== Service Status ====="
echo "Checking service: $SERVICE"

STATUS=$(systemctl is-active "$SERVICE" 2>/dev/null)

if [ "$STATUS" = "active" ]; then
    echo "Status: ACTIVE"
elif [ "$STATUS" = "inactive" ]; then
    echo "Status: INACTIVE"
elif [ "$STATUS" = "failed" ]; then
    echo "Status: FAILED"
else
    echo "Status: $STATUS"
    echo "Service may be missing or in another state."
fi

