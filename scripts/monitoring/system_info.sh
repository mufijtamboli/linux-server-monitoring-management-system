#!/bin/bash

echo "===== LSMMS System Information ====="

echo "Hostname:"
hostname

echo "Operating System:"
cat /etc/os-release | grep PRETTY_NAME

echo "System Uptime:"
uptime -p

echo "Current Date and Time:"
date
