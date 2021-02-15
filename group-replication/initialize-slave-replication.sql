CHANGE MASTER TO MASTER_USER='repl', MASTER_PASSWORD='password' FOR CHANNEL 'group_replication_recovery';

-- INSTALL PLUGIN group_replication SONAME 'group_replication.so';

-- https://www.programmersought.com/article/4511201866/
RESET MASTER;

START GROUP_REPLICATION USER='repl', PASSWORD='password';


