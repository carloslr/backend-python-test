DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  password_salt VARCHAR(255),
  login_count INTEGER NOT NULL DEFAULT 0,
  login_fail INTEGER NOT NULL DEFAULT 0,
  last_login DATETIME
);

DROP TABLE IF EXISTS todos;
CREATE TABLE todos (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  description VARCHAR(255),
  completed TINYINT DEFAULT 0,
  created_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX ix_todos_user_id ON todos(user_id); -- SQLite does not create indexes on FK's automatically as mysql does
CREATE INDEX ix_todos_completed ON todos(completed);