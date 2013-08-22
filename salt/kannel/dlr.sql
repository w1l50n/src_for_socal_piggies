DROP TABLE IF EXISTS dlr;
CREATE TABLE dlr (
  id int(11) auto_increment,
  smsc varchar(40),
  ts varchar(40),
  destination varchar(40),
  source varchar(40),
  service varchar(40),
  url varchar(255),
  mask int(10),
  status int(10),
  boxc varchar(40),
  KEY id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
