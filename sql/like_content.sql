CREATE TABLE `Like_content` (
  `id` int(11) NOT NULL,
  `username` varchar(45) NOT NULL,
  PRIMARY KEY (`id`,`username`),
  KEY `user_idx` (`username`),
  CONSTRAINT `content` FOREIGN KEY (`id`) REFERENCES `Content` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `user` FOREIGN KEY (`username`) REFERENCES `Person` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1