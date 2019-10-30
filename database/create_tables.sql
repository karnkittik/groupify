
CREATE TABLE `group` (
  group_id varchar(10) PRIMARY KEY,
  group_name varchar(20),
  max_person integer
);


CREATE TABLE member (
  username varchar(10) PRIMARY KEY,
  firstname varchar(20),
  lastname varchar(20),
  faculty varchar(20),
  year integer
);


CREATE TABLE group_member (
  group_id varchar(10) NOT NULL,
  username varchar(20) NOT NULL,
  FOREIGN KEY (group_id) REFERENCES `group`(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (username) REFERENCES member(username) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE message_private (
  from_username varchar(20) NOT NULL,
  to_username varchar(20) NOT NULL,
  time TIMESTAMP,
  message text NOT NULL,
  FOREIGN KEY (from_username) REFERENCES member(username) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (to_username) REFERENCES member(username) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE message_broadcast (
  from_username varchar(20) NOT NULL,
  time TIMESTAMP,
  message text NOT NULL,
  FOREIGN KEY (from_username) REFERENCES member(username) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE message_group (
  from_username varchar(20) NOT NULL,
  group_id varchar(10) NOT NULL,
  time TIMESTAMP,
  message text NOT NULL,
  FOREIGN KEY (from_username) REFERENCES member(username) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (group_id) REFERENCES `group`(group_id) ON DELETE CASCADE ON UPDATE CASCADE
);