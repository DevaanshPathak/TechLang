# Database example for TechLang
# This demonstrates SQLite3 integration

# Create a users table
db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT"

# Insert some sample data
db_insert users "1, Alice, 25, alice@example.com"
db_insert users "2, Bob, 30, bob@example.com"
db_insert users "3, Charlie, 35, charlie@example.com"

# Query all users
print "All users:"
db_select "SELECT * FROM users"

# Query users older than 28
print "Users older than 28:"
db_select "SELECT name, age FROM users WHERE age > 28"

# Update a user's age
db_update "UPDATE users SET age = 26 WHERE name = 'Alice'"

# Show updated data
print "After updating Alice's age:"
db_select "SELECT * FROM users WHERE name = 'Alice'"

# Delete a user
db_delete "DELETE FROM users WHERE name = 'Charlie'"

# Show final data
print "Final user list:"
db_select "SELECT * FROM users"

# Close database connections
db_close
