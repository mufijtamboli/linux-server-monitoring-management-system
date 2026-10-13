#!/bin/bash

echo "===== CPU Monitoring ====="

echo "CPU Information:"
lscpu | grep "Model name"

echo "CPU Load Average:"
uptime
