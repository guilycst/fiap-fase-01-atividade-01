#!/bin/bash

# Usage: ./run_insert.sh <database_file> <number_of_times>
# Example: ./run_insert.sh my_database.db 5

# Database file
DB_FILE=$1

# Number of times to run the query
NUM_TIMES=$2

# SQL query to create table if it doesn't exist
CREATE_TABLE_QUERY="CREATE TABLE IF NOT EXISTS your_table_name (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  column1 TEXT NOT NULL,
  column2 TEXT NOT NULL
);"

# SQL query to insert data
INSERT_QUERY="INSERT INTO your_table_name (column1, column2) VALUES ('value1', 'value2');"

# Create the table if it doesn't exist
sqlite3 $DB_FILE "$CREATE_TABLE_QUERY"

# Run the insert query the specified number of times
for ((i=1; i<=NUM_TIMES; i++))
do
  echo "Running insert query $i/$NUM_TIMES"
  sqlite3 $DB_FILE "$INSERT_QUERY"
done

echo "Done."
