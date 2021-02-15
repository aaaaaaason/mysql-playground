MASTER_HOST=127.0.0.1
MASTER_PORT=3306

SLAVE_HOST=127.0.0.1
SLAVE_PORT=3307

DB_USER=root
DB_PASSWD=password

echo "${@:2}"

case $1 in 

restart)
    docker-compose down && docker-compose up -d
    ;;

master)
    mysql -h $MASTER_HOST -P $MASTER_PORT -u $DB_USER -p$DB_PASSWD < $2
    ;;

slave)
    mysql -h $SLAVE_HOST -P $SLAVE_PORT -u $DB_USER -p$DB_PASSWD < $2
    ;;

mysqlsh-master)
    # https://dev.mysql.com/doc/refman/8.0/en/mysql-shell-tutorial-javascript-shell.html
    # https://dev.mysql.com/doc/mysql-shell/8.0/en/mysqlsh.html
    mysqlsh -h $MASTER_HOST -P $MASTER_PORT -u $DB_USER -p$DB_PASSWD < $2
    ;;

init)
    ./run.sh master create-replication-user.sql &&
    ./run.sh slave create-replication-user.sql &&
    ./run.sh master initialize-master-replication.sql &&
    ./run.sh slave initialize-slave-replication.sql &&
    ./run.sh mysqlsh-master create-cluster.js &&
    docker restart mysql-router &&
    ./run.sh master init-database.sql
    ;;

esac