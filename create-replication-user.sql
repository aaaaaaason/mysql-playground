CREATE USER IF NOT EXISTS slave@`mysql-slave`;
GRANT REPLICATION SLAVE ON *.* TO slave@'%' IDENTIFIED BY 'password';