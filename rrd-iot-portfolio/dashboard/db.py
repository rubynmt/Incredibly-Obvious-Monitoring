import sqlite3


class Database:
    def __init__(self, filename, table_name='cpu_loads'):
        self.__filename = filename
        self.__table_name = table_name

    def __execute(self, query):
        """
        Convenience method that opens connection, retrieves a cursor,
        executes a query, then closes the connection.

        SHOUOLD NOT be used for queries that fetch actual data.
        """
        connection = sqlite3.connect(self.__filename)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    def __retrieve(self, query, json=False):
        """
        Convenience method that opens connection, retrieves a cursor,
        executes a query, retrieves the query results, closes the
        connection, and then returns results

        SHOULD NOT be used for actions that modify database, tables or data.
        """
        connection = sqlite3.connect(self.__filename)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        count = 0
        if json:
            # Create an array of dictionaries
            results = []
            for row in rows:
                # For each row in the rows,
                # Grab the table's field names (from SQLite) and
                # (using ZIP) associate each field name with the
                # corresponding value from  the row
                # Then append the dictionary to the results list
                results.append(dict(zip(
                    [c[0] for c in cursor.description], row)))
        else:
            # Create an "indexed" dictionary
            results = {}
            for row in rows:
                # For each row in the rows,
                # Grab the table's field names (from SQLite) and
                # (using ZIP) associate each field name with the
                # corresponding value from  the row
                # Then create a dictionary of the resulting row with a
                # unique ID for the resulting row of data.
                results[count] = dict(zip(
                    [c[0] for c in cursor.description], row))
                count += 1
        connection.close()
        return results

    def create(self):
        """
        Method that creates database table if not already exists.
        """
        query = f'CREATE TABLE IF NOT EXISTS {self.__table_name} (' \
                '    [id] INTEGER PRIMARY KEY,' \
                '    [load] DECIMAL,' \
                '    [created_at] DATETIME' \
                ')'

        self.__execute(query)

    def store(self, value):
        """
        Method that stores a single data value into the table.
        """
        query = f'INSERT INTO {self.__table_name} ' \
                f'    VALUES (null, {value}, datetime())'
        self.__execute(query)

    def get_last(self, value="10", json=False):
        """
            This method returns the last <value> items of stored data.
            For example, calling `get_last(13)` will return the last
            thirteen items of recorded data.

            :param value:   An Integer
            :param json:    A boolean identifying if results to be JSON, or a
                            Dictionary
            :return:        JSON | Dictionary
        """
        try:
            if not value.isnumeric():
                value = 10
        except AttributeError:
            value = abs(int(value))
        else:
            value = abs(int(value))

        query = f"SELECT * FROM {self.__table_name}" \
                f"    ORDER BY created_at DESC" \
                f"    LIMIT {value}"
        return self.__retrieve(query, json=json)

    def get_in_last(self, value="1", period="MINUTES", json=False):
        """
        This method returns the data that was in the last <value> <period>.
        For example, calling `get_in_last(3,"seconds")` will return the last
        three seconds of recorded data.

        :param value:   An Integer
        :param period:  A value from Seconds, Minutes, Hours, Days, Weeks,
                        Months and Years
        :param json:    A boolean identifying if results to be JSON, or a
                        Dictionary
        :return:        JSON | Dictionary
        """
        period = period.upper()
        if period not in (
                'SECONDS', 'MINUTES', 'HOURS', 'DAYS',
                'WEEKS', 'MONTHS', 'YEARS'):
            period = 'MINUTES'
        try:
            if not value.isnumeric():
                value = -1
        except AttributeError:
            value = -abs(int(value))
        else:
            value = -abs(int(value))

        query = f"SELECT * FROM {self.__table_name}" \
                f"    WHERE created_at > datetime('now', '{value} {period}')" \
                f"    ORDER BY created_at DESC"
        return self.__retrieve(query, json=json)
