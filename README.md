# Automatic-data-inserter
Python script I'm using to insert .log json file whenever new one appears in directory.
Cron executes script every 5 minutes automatically searching for a new file.
In this case it searches a file which starts from 'kf' and ends with '.log', because that's a patter for files it should be looking for.

# Requirements:
```bash
  sudo apt install python3
  pip3 install mysql-connector-python
```

# Cron setup
```bash
crontab -e
*/5 * * * * /usr/bin/python3 /path/script.py 
```
