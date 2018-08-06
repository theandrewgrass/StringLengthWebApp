from flask import Flask, request, render_template
import sqlite3

class string_db:

  def __init__(self, connection):
    self.cursor = connection.cursor()
    self.string_table = 'string_table'
    self.string_key = 'string_key'
    self.string_key_type = 'TEXT'
    self.num_chars = 'num_chars'
    self.num_chars_type = 'INTEGER'

  def create_table_for_strings(self):
    # Create and name the basic table with a single column containing the primary key.
    self.cursor.execute("CREATE TABLE {table_name} ({key_name} {key_type} PRIMARY KEY)"\
	.format(table_name=self.string_table, key_name=self.string_key, key_type=self.string_key_type))

    # Add another column to the table to hold the number of characters in each string.
    self.cursor.execute("ALTER TABLE {table_name} ADD COLUMN '{col_name}' {col_type}"\
	.format(table_name=self.string_table, col_name=self.num_chars, col_type=self.num_chars_type))

  def insert_elem_into_table(self, new_key, new_key_col_value):
    self.cursor.execute("INSERT OR IGNORE INTO {table_name} ({key_col_name}, {col_name}) VALUES ('{new_key}', {new_key_col_value})"\
	.format(table_name=self.string_table, key_col_name=self.string_key, col_name=self.num_chars,\
	new_key=new_key, new_key_col_value=new_key_col_value))

def connect_to_db():
  sqlite_file = 'string_db.sqlite'
  connection = sqlite3.connect(sqlite_file)

  return connection

def commit_and_close_connection(connection):
  print("Committing changes and closing the connection...")
  connection.commit()
  connection.close()

def main():
  app = Flask(__name__)

  @app.route('/change_string', methods=['GET', 'POST'])
  def change_string():
    if request.method == 'POST':

      # Create a connection to the database and a database object.
      connection = connect_to_db()
      string_database = string_db(connection)

      try:
        string_database.create_table_for_strings()
      except:
        pass

      string_to_be_added = request.form.get('string_to_be_added')
      num_chars_in_string = len(string_to_be_added)

      string_database.insert_elem_into_table(string_to_be_added, num_chars_in_string)

      print("The string has been added to the database (unless existed previously)...")

      commit_and_close_connection(connection)
      print("Program finished. Goodbye...")

      return render_template('change_string.html', num_chars_in_string=num_chars_in_string)

    return render_template('change_string.html')

  app.run(debug=True, port=5000)


if __name__ == '__main__':
  main()
