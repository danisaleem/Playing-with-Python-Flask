
CREATE TABLE "Users" 
( 
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    "username" TEXT NOT NULL UNIQUE, 
    "email" TEXT NOT NULL UNIQUE, 
    "password_hash" TEXT NOT NULL, 
    "about_me" TEXT, 
    "last_seen" TEXT 
)

CREATE TABLE "Posts" 
( 
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    "body" TEXT, 
    "timestamp" Text, 
    "author_id" INTEGER NOT NULL, 
    FOREIGN KEY("author_id") REFERENCES "Users"("id") 
)