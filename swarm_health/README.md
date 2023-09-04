### NTFY SWARM MONITORING SCRIPT ###

This script is using SSH to prompt docker for swarm status! 

~/.ssh/config example:
```
Host host1
  HostName hostname_or_ip_address
  User user_name
  IdentityFile /path/to/your/key
```

Cronjob example (add the following line to crobtab for execution):

```
* * * * * /usr/bin/python3 /home/user_name/monitoring/ntfy_scripts/swarm_health/swarm_health.py >> /home/user_name/monitoring/monitoring.log 2>&1
```

The following executes swarm_health.py script every minute, with optional logging.
Logging was used on initial script setup and it is not needed, as you will get notified if anything goes wrong.
