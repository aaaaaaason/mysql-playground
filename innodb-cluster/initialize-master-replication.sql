CHANGE MASTER TO MASTER_USER='repl', MASTER_PASSWORD='password' FOR CHANNEL 'group_replication_recovery';
-- INSTALL PLUGIN group_replication SONAME 'group_replication.so';
SET GLOBAL group_replication_bootstrap_group = ON;
START GROUP_REPLICATION USER='rpl_user', PASSWORD='password';
SET GLOBAL group_replication_bootstrap_group = OFF;

