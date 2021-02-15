// https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster-from-group-replication.html
var cluster = dba.createCluster('mycluster', {adoptFromGR: true});
