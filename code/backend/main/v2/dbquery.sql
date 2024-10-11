SELECT * FROM users;
SELECT * FROM products;

INSERT INTO users(username, password) VALUES ('admin', '12345');



set admin usr

sqlite3 active_data.db                                                        5 ⚙
SQLite version 3.39.2 2022-07-21 15:24:47
Enter ".help" for usage hints.
sqlite> .tables
alembic_version  products         users          
sqlite> insert into users values(1, "admin", "$2b$12$v8PguCowGIqbWkrSuOgCFeHX6m03.yWQfubQzHx5Nj548ezrOvpye", "admin");
sqlite> select * from users;
1|admin|$2b$12$v8PguCowGIqbWkrSuOgCFeHX6m03.yWQfubQzHx5Nj548ezrOvpye|admin
 
