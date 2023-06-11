#!/usr/bin/env bash

# Connection parameters
#%sql postgresql://db:db@postgres/db
dbname=db
dbuser=db
dbpass=db
dbhost=postgres


# Create an array to hold test results
declare -a test_results=()

# Function to run the tests
run_tests() {
  local expected_result=$1
  local folder=$2

  # Loop through each SQL file
  for sqlfile in $folder/*.sql
  do
    # Connect to the database, run the SQL file and capture the output
    output=$(PGPASSWORD=$dbpass psql -v ON_ERROR_STOP=1 -h $dbhost -U $dbuser -d $dbname -f $sqlfile 2>&1)


    # Check the status of the last command
    if [[ $? -eq $expected_result ]]
    then
      test_results+=("$sqlfile - Success ✅")
    else
      test_results+=("$sqlfile - Failure ❌")
      test_results+=("------")
      test_results+=("$output")
      test_results+=("------")
    fi

    echo $output > $sqlfile.log

  done
}

# Run tests
run_tests 0 pass
run_tests 3 fail

# Output test results
printf '%s\n' "${test_results[@]}"
