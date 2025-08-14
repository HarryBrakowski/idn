"Sqlite Connection and Query Definition"
import sqlite3
import time
from src.apis.base_api import API


class SqliteApi(API):
    '''API Subclass to handle Sqlite API logic'''

    def __init__(self, path):
        '''
        :path: path to the sqlite database file
        '''
        self._path:str = path
        super().__init__()


    def _connect(self):
        try:
            conn = sqlite3.connect(self._path)
            print("successfully connected to the sqlite database")
            return conn
        
        except Exception as e:
            print("connection failed. following error occured:", e)
            raise ConnectionError from e


    def close(self):
        return super().close()


    def _table(self, table:str):
        '''
        Create a clean string storing the path to the table
        '''
        return f"{table}"



    def check_existence(self, table:str, cursor=None) -> bool:
        '''
        Rename a table. 
            - table: name of the table of interest
            - cursor: default None. Creates a new cursor instance. 
                      If called from another connection, pass the existing cursor to this argument.

        '''
        close_cursor = False

        if cursor is None:
            close_cursor = True # close cursor only if it is created within this method
            cursor = self.conn.cursor()

        # check if table exists
        try:
            cursor.execute(f"""
                SELECT 1 
                FROM sqlite_master 
                WHERE type IN ('table', 'view') 
                AND name = '{table}';
            """)
            if cursor.fetchone():
                return True
            return False

        except Exception as e:
            print(f'failed to check existence of table {table}. error: ', e)
            return None

        finally:
            if close_cursor:
                cursor.close()



    def safe_rename_table(self, new_name:str, old_name:str, cursor=None):
        '''
        Rename a table. 
            - Deletes the new_name in case this table exists.
            - Checks the existence of the old_name and renames it if it exists.
            - cursor: default None. Creates a new cursor instance. 
                      If called from another connection, pass the existing cursor to this argument.

        '''
        close_cursor = False

        if cursor is None:
            close_cursor = True # close cursor only if it is created within this method
            cursor = self.conn.cursor()

        try:
            # drop any table called new_name in case it exists
            drop_query = f'''DROP TABLE IF EXISTS {new_name};'''
            cursor.execute(drop_query)

            # check the existence of table with old_name (by fetching meta data)
            table_exists = self.check_existence(old_name, cursor)
            if table_exists:
                cursor.execute(f"ALTER TABLE {old_name} RENAME TO {new_name};")
            else:
                print(f"Table '{old_name}' does not exist. Cannot rename to '{new_name}'.")

            # commit changes
            self.conn.commit()

        except Exception as e:
            print(f'renaming table {old_name} to {new_name} failed. error: ', e)
            self.conn.rollback()
        
        finally:
            if close_cursor:
                cursor.close()


    def _query_create_table_schema(self, column_spec: list[dict], table: str):
        '''
        Query to process the frontends table schema definition 'column_spec' to
        create a valid sqlite table schema based on this input
        
        Arguments:
            :colum_spec: frontend table schema, example:
                [{'type': 'select', 'field': 'project', ..}, {..}, ..]
            :table: the target table
        '''
        # target table
        _table = self._table(table)

        # header definition
        header = []
        for spec in column_spec:
            field_name = spec.get('field')
            max_decimal_places = spec.get('maxDecimalPlaces')

            # assign the right sql data type
            match spec.get('type'):
                case 'select' | 'date' | 'text' | 'largeText':
                    sql_type = 'TEXT'
                case 'number':
                    sql_type = 'REAL' if int(max_decimal_places) > 0 else 'INTEGER'
                case 'auto_timestamp':
                    sql_type = 'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP'
                case _:
                    sql_type = 'TEXT'

            header.append(f'"{field_name}" {sql_type}')

        return f'''CREATE TABLE IF NOT EXISTS {_table} ({', '.join(header)});'''

    def initialize_empty_table(self, column_spec: list[dict], table: str, cursor=None):
        '''
        Create an empty sql table in case it does not exist yet.

        Arguments:
            :colum_spec: frontend table schema, example:
                [{'type': 'select', 'field': 'project', ..}, {..}, ..]
            :table: the target table
        '''
        
        close_cursor = False
        if cursor is None:
            close_cursor = True # close cursor only if it is created within this method
            cursor = self.conn.cursor()

        try:
            # query creation & execution
            query = self._query_create_table_schema(column_spec, table)
            cursor.execute(query)

            # commit changes
            self.conn.commit()

        except Exception as e:
            print(f'failed to create empty table "{table}". error: ', e)
            self.conn.rollback()
        
        finally:
            if close_cursor:
                cursor.close()

    def _query_write_table(self, row_data:list[dict], table: str):
        '''
        Query to write the specified row_data into a valid sql insert query
        The insert order is always matching to existing tables by defining 'col_string'
        --> thereby it is import that all rows are aligned with row[0]

        Arguments:
            :row_data: data that shall be inserted into the sql table. example:
                [{'project': 'Project A', 'department': 'Department A', ..}, {..}, ..]
            :schema: SCHEMA where the sql_table is located
            :sql_table: table_name of the sql table the df shall be inserted in
        '''
        # target table def
        _table = self._table(table)
        
        # Column Definition based on the first row_data node (=row)
        if len(row_data) > 0:
            cols = row_data[0].keys()
            cols = [f'"{col}"' for col in cols]
            col_string = ", ".join(cols)
        else:
            return None

        # Row Definition (each row is a tuple with comma separated string values
        row_strings = []
        for node in row_data:
            values = [f"'{value}'" for value in node.values()]
            row_string = f"({", ".join(values)})"
            row_strings.append(row_string)
        values_string = ", ".join(row_strings)

        # SQL Query
        return f'''
        INSERT INTO {_table} ({col_string})
        VALUES {values_string};
        '''
    
    def align_row_data_with_table(self, row_data: list[dict], table: str, cursor):
        """Ensure row_data matches existing table schema in SQLite 
            by filtering out row_data keys not existing in table (table columns)"""
        cursor.execute(f'PRAGMA table_info({self._table(table)})')
        table_info = cursor.fetchall()

        # Schema-Infos
        existing_cols = [row[1] for row in table_info]         # colum names
        defaults = {row[1]: row[4] for row in table_info}      # {col: default_value}

        aligned_data = []
        for row in row_data:
            filtered = {k: v for k, v in row.items() if k in existing_cols}
            aligned_data.append(filtered)

        return aligned_data



    def write_table(self, row_data:list[dict], column_spec:list[dict], table:str, chunksize:int=50000, append:bool=True):
        '''
        This function writes row_data to a specific table. Schema MUST align with column_spec if appnend is True.

        - key feature: it first creates a temporary dataframe and renames it afterwards in case everything was successfull
        - it uses both query functions: query_create_header / query_df_to_redshift
        - df is chunked since AWS redshift statements have size limitation of ~16 mio bytes
        
        Arguments:
            :**row_data**: data that shall be inserted into the sql table. example:
                [{'project': 'Project A', 'department': 'Department A', ..}, {..}, ..]
            :**colum_spec**: frontend table schema, example:
                [{'type': 'select', 'field': 'project', ..}, {..}, ..]
            :**table**: table_name of the sql table the df shall be inserted in
        '''
        cursor = self.conn.cursor()
        
        try:
            query_time = time.time()

            if append:
                # check if the table exists and create it if not
                if not self.check_existence(table=table, cursor=cursor):
                    query = self._query_create_table_schema(column_spec, table)
                    cursor.execute(query)
                else:
                    # ensure harmonized data structure matching the existing table
                    # important because rowData sometimes contains more data (when coming from ag grid etc.)
                    row_data = self.align_row_data_with_table(row_data, table, cursor)

                # define the table to write to
                write_to_table = table
            
            else:
                # drop temporary sql table if it exists
                cursor.execute(f'''DROP TABLE IF EXISTS temp;''')

                # create the new temporary sql table
                query = self._query_create_table_schema(column_spec, table="temp")
                cursor.execute(query)

                # define the table to write to
                write_to_table = "temp"

            # write row_data to the sql table -- chunked operation
            if len(row_data)>0:
                chunks = self.chunk_list(row_data, chunksize)
                for chunk in chunks:
                    query = self._query_write_table(chunk, table=write_to_table)
                    cursor.execute(query)

            self.conn.commit()

            if not append:
                # rename temp to the actual sql table
                cursor.execute(f'''DROP TABLE IF EXISTS {table}''')
                cursor.execute(f'''ALTER TABLE temp RENAME TO {table}; ''')
            
            # commit changes and close cursor
            self.conn.commit()
            cursor.close()

            print(f"data successfully written to {table}. Time required: " + str(round(time.time() - query_time, 2)))


        except Exception as e:
            cursor.execute(f'''DROP TABLE IF EXISTS temp;''')
            self.conn.commit()
            cursor.close()
            print(e)
