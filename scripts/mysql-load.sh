echo "DB password is:  ${CLOUD_SQL_DATABASE_PASSWORD}"
echo
mysql -u ${CLOUD_SQL_DATABASE_USERNAME} -p --host ${CLOUD_SQL_DATABASE_HOST} < ./staging.sql
