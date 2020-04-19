
CREATE TABLE Users (
	username	TEXT NOT NULL UNIQUE,
	email	TEXT,
	password_hash	TEXT NOT NULL,
	about_me	TEXT,
	last_seen	TEXT,
	PRIMARY KEY("username")
);

CREATE TABLE post ( 
    id INTEGER NOT NULL UNIQUE, 
    body TEXT, 
    timestamp Text, 
    user_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) 
    REFERENCES user (id) 
    )