CREATE TABLE `group` (
  group_id varchar(10) PRIMARY KEY,
  group_name varchar(20),
  max_person integer
);

INSERT INTO `group`(group_id, group_name, max_person) VALUES ("0", "", 0);

CREATE TABLE `user` (
  username varchar(10) PRIMARY KEY,
  firstname varchar(20),
  lastname varchar(20),
  faculty varchar(20),
  year integer,
  group_id varchar(10) DEFAULT "0" NOT NULL,
  FOREIGN KEY (group_id) REFERENCES `group`(group_id) ON DELETE SET DEFAULT
);

CREATE TABLE self (
  username varchar(10),
  is_admin boolean DEFAULT 0,
  is_member boolean DEFAULT 0,
  FOREIGN KEY (username) REFERENCES `user`(username) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE message_private (
  from_username varchar(20) NOT NULL,
  to_username varchar(20) NOT NULL,
  time TIMESTAMP,
  message text NOT NULL,
  FOREIGN KEY (from_username) REFERENCES `user`(username) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (to_username) REFERENCES `user`(username) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE message_broadcast (
  from_username varchar(20) NOT NULL,
  time TIMESTAMP,
  message text NOT NULL,
  FOREIGN KEY (from_username) REFERENCES `user`(username) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE message_group (
  from_username varchar(20) NOT NULL,
  group_id varchar(10) NOT NULL,
  time TIMESTAMP,
  message text NOT NULL,
  FOREIGN KEY (from_username) REFERENCES `user`(username) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (group_id) REFERENCES `group`(group_id) ON DELETE CASCADE ON UPDATE CASCADE
);