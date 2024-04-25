# Remove objects from the database
psql -c "DROP table IF EXISTS donation;"
psql -c "DROP table IF EXISTS member;"
psql -c "DROP table IF EXISTS chapter;"
psql -c "DROP table IF EXISTS event;"

psql -c "DELETE FROM migratehistory;"
rm -rf migrations
rm -rf migrations.json

pem init

# Use peewee-migrate to create tables from Peewee models
pem add models.donation
pem add models.member
pem add models.chapter
pem add models.event


pem watch
pem migrate

rm -rf migrations
rm -rf migrations.json

# Load data back into database
< data.sql psql
