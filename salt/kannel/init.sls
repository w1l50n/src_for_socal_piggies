kannel:
  pkg:
    - installed

kannel-dev:
  pkg:
    - installed

kannel-extras:
  pkg:
    - installed

usb-modeswitch:
  pkg:
    - installed

/etc/kannel/kannel.conf:
  file.managed:
    - source: salt://kannel/kannel.conf
    - mode: 644

/etc/default/kannel:
  file.managed:
    - source: salt://kannel/default
    - mode: 644

kannel-user:
  user.present:
    - name: kannel
    - groups:
      - dialout
    - require:
      - pkg: kannel

