DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(40) UNIQUE NOT NULL,
	password VARCHAR(255) NOT NULL,

	PRIMARY KEY(id)
);

