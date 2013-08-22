kannel_db:
  mysql_database.present:
    - name: "kannel"

kannel:
  mysql_user.present:
    - host: "localhost"
    - password: "kannel"

kannel_grant:
  mysql_grants.present:
    - grant: "all privileges"
    - database: "kannel.*"
    - user: "kannel"
    - host: "localhost"

