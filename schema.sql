
CREATE TABLE Users (
	username	TEXT NOT NULL UNIQUE,
	email	TEXT,
	password_hash	TEXT NOT NULL,
	about_me	TEXT,
	last_seen	TEXT,
	PRIMARY KEY("username")
);

CREATE TABLE "Posts" ( 
    "id" INTEGER NOT NULL UNIQUE, 
    "body" TEXT, 
    "timestamp" Text, 
    "username" TEXT, 
    PRIMARY KEY("id"), 
    FOREIGN KEY("username") REFERENCES "Users"("username") 
    )