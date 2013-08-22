nginx:
  pkg:
    - installed
  service:
    - running
    - require:
      - pkg: nginx

/etc/nginx/sites-available/rapidsms:
  file.managed:
    - source: salt://nginx/rapidsms

/etc/nginx/sites-enabled/rapidsms:
  file.symlink:
    - target: /etc/nginx/sites-available/rapidsms
    - require:
      - file.exists: /etc/nginx/sites-available/rapidsms

