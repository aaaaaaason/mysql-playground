MASTER_HOST=127.0.0.1
MASTER_PORT=33060

SLAVE_HOST=127.0.0.1
SLAVE_PORT=33061

DB_USER=root
DB_PASSWD=password

case $1 in 

create-replication-user)
    mysql -h $MASTER_HOST -P $MASTER_PORT -u $DB_USER -p$DB_PASSWD < \
    create-replication-user.sql
    ;;

initialize-replication)
    mysql -h $SLAVE_HOST -P $SLAVE_PORT -u $DB_USER -p$DB_PASSWD < \
    initialize_replication.sql
    ;;

init-database)
    mysql -h $MASTER_HOST -P $MASTER_PORT -u $DB_USER -p$DB_PASSWD < \
    init-database.sql
    ;;

*)
    ./run.sh create-replication-user &&
    ./run.sh initialize-replication &&
    ./run.sh init-database
    ;;

esac