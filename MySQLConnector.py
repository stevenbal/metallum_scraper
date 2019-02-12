import mysql.connector

class MySQLConnector:
    """
    Class that establishes a connection with a MySQL database and allows
    for the insertion of data to that database (will overwrite duplicates)
    """

    def __init__(self, host, user, passwd, database):
        """
        Description:    initializer for the database connector

        Input:
        -host:          str, the name of the host for the database
        -user:          str, the username to access the database
        -passwd:        str, the password of said user
        -database:      str, the database to be connected to
        """
        self.db = mysql.connector.connect(
                    host = host,
                    user = user,
                    passwd = passwd,
                    database = database
                )
        self.cursor = self.db.cursor()

    def write_to_database(self, table, colnames, data):
        """
        Description:    function that inserts the specified data into the
                        specified table, overwriting duplicate rows
        
        Input:
        -table:         str, the name of the table in which the data is to be
                        inserted
        -colnames:      list, the names of the columns for which data will be
                        inserted (length must match the length of each datarow)
        -data:          list, contains the rows of data which are to be inserted
        """
        query = f'INSERT INTO {table} ('
        columns = ', '.join(colnames)
        values = ', '.join(['%s'] * len(colnames))
        duplicates = 'ON DUPLICATE KEY UPDATE '
        duplicate_values = ', '.join([f'{col} = VALUES({col})' for col in colnames])
        
        sql = query + columns + ') VALUES(' + values + ') ' + duplicates + duplicate_values
        self.cursor.executemany(sql, data)
        self.db.commit()

    def close(self):
        """
        Description:    closes the cursor and the database connection
        """
        self.cursor.close()
        self.db.close()
