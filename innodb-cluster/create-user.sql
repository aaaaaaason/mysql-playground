CREATE USER IF NOT EXISTS user@'%';
GRANT SELECT, INSERT, UPDATE, DELETE, SHOW DATABASES, INDEX, CREATE, ALTER ON *.* TO user@'%' IDENTIFIED BY 'password';