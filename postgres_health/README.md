### POSTGRES MONITORING SCRIPT ###

This script is monitoring postgres using patroni service!

Cronjob example:

```
* * * * * /usr/bin/python3 /home/user_name/monitoring/ntfy_scripts/postgres_health/postgres_health.py
```
