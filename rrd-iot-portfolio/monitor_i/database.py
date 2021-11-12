import sqlite3

class Db:
    def __init__(self, filename):
        self.__filename = filename
        self.__table_name = 'cpu_loads'

    def __execute(self, query):
        """Helper function that opens database connection, performs query, then closes.
        """
        connection = sqlite3.connect(self.__filename)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    def create(self):
        """Create a new database using the filename stored in this class.

        If the database already exists, it will print the error and continue.
        """
        self.__execute('CREATE TABLE IF NOT EXISTS ' + self.__table_name +
                       '([id] INTEGER PRIMARY KEY,'
                       '[load] DECIMAL, '
                       '[created_at] DATETIME)')

    def store_cpu_load(self, cpu_load):
        """Store a single CPU load value in the database.

        :param cpu_load: The cpu load value to store in the database.
        """
        self.__execute('INSERT INTO ' + self.__table_name +
                       '(id, load, created_at) '
                       f'VALUES (null, {cpu_load}, datetime())')
