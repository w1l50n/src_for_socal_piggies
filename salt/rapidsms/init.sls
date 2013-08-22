/opt/pi:
    file.directory:
    - user: pi
    - group: pi
    - dir_mode: 755
    - file_mode: 644

create-rapidsms-project:
  cmd.run:
    - user: pi
    - name: "django-admin.py startproject --template=https://github.com/rapidsms/rapidsms-project-template/zipball/release-0.15.0 --extension=py,rst rapidsms_pi && sudo pip install -r rapidsms_pi/requirements/base.txt"
    - cwd: /opt/pi
    - onlyif:
      - file.missing: /opt/pi/rapidsms_pi

/opt/pi/rapidsms_pi/rapidsms_pi/settings.py:
  file.managed:
    - source: salt://rapidsms/settings.py
    - user: pi
    - group: pi

/opt/pi/rapidsms_pi/rapidsms_pi/urls.py:
  file.managed:
    - source: salt://rapidsms/urls.py
    - user: pi
    - group: pi

/opt/pi/rapidsms_pi/gunicorn_start.sh:
  file.managed:
    - source: salt://rapidsms/gunicorn_start.sh
    - user: pi
    - group: pi
    - mode: 755

/opt/pi/rapidsms_pi/logs:
    file.directory:
    - user: pi
    - group: pi
    - dir_mode: 755
    - file_mode: 644

