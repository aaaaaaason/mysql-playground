MASTER_HOST=127.0.0.1
MASTER_PORT=33060

SLAVE_HOST=127.0.0.1
SLAVE_PORT=33061

DB_USER=root
DB_PASSWD=password

echo "${@:2}"

case $1 in 

master)
    mysql -h $MASTER_HOST -P $MASTER_PORT -u $DB_USER -p$DB_PASSWD < $2
    ;;

slave)
    mysql -h $SLAVE_HOST -P $SLAVE_PORT -u $DB_USER -p$DB_PASSWD < $2
    ;;

init)
    ./run.sh master create-replication-user.sql &&
    ./run.sh slave create-replication-user.sql &&
    ./run.sh master initialize-master-replication.sql &&
    ./run.sh slave initialize-slave-replication.sql &&
    ./run.sh master init-database.sql
    ;;

esac