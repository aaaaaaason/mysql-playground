SET SQL_LOG_BIN=0;

CREATE USER IF NOT EXISTS repl@'%';

-- https://zhuanlan.zhihu.com/p/111665735
ALTER USER repl@'%' IDENTIFIED WITH sha256_password BY 'password';

GRANT REPLICATION SLAVE ON *.* TO repl@'%' ;
GRANT BACKUP_ADMIN ON *.* TO repl@'%';
FLUSH PRIVILEGES;

SET SQL_LOG_BIN=1;