mysql:
  pkg:
    - installed
    - name: mysql-server
    - service:
      - running

mysql-client:
  pkg:
    - installed

libmysqlclient-dev:
  pkg:
    - installed

/etc/salt/minion:
  file.append:
    - text:
      - "mysql.default_file: '/etc/mysql/debian.cnf'"

