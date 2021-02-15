CREATE DATABASE IF NOT EXISTS `replication-test`;

USE `replication-test`;

CREATE TABLE IF NOT EXISTS test1 (
    id varchar(64) NOT NULL,
    field1 varchar(512) DEFAULT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO test1 (id, field1) VALUES ('1', 'v1'), ('2', 'v2'), ('3', 'v3');