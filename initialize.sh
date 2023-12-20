DB_NAME="database_project"
DB_USER="Aida"
DB_PASSWORD="abcd"
DB_OWNER="Aida"

# Drop existing user if needed
sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"

# Create a new user
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

# Set ownership of the database
sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_OWNER;"

