supervisor:
  pkg.installed

/etc/supervisor/conf.d/rapidsms.conf:
  file.managed:
    - source: salt://supervisor/rapidsms.conf
    - mode: 644
    - require:
      - pkg: supervisor

/etc/supervisor/conf.d/rapidsms_celery.conf:
  file.managed:
    - source: salt://supervisor/rapidsms_celery.conf
    - mode: 644
    - require:
      - pkg: supervisor

/etc/supervisor/conf.d/rapidsms_celerybeat.conf:
  file.managed:
    - source: salt://supervisor/rapidsms_celerybeat.conf
    - mode: 644
    - require:
      - pkg: supervisor

