echo "DB password is:  ${CLOUD_SQL_DATABASE_PASSWORD}"
echo
mysqldump --column-statistics=0  -u ${CLOUD_SQL_DATABASE_USERNAME} -p --host ${CLOUD_SQL_DATABASE_HOST} --databases db_demo --set-gtid-purged=OFF > staging.sql;

