rapidsms_db:
  mysql_database.present:
    - name: "rapidsms"

rapidsms:
  mysql_user.present:
    - host: "localhost"
    - password: "rapidsms"

rapidsms_grant:
  mysql_grants.present:
    - grant: "all privileges"
    - database: "rapidsms.*"
    - user: "rapidsms"
    - host: "localhost"
    - require:
      - mysql_database.present: rapidsms
      - mysql_user.present: rapidsms
