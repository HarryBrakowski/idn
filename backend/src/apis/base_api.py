'''
Base Class Definition for APIs handling Database Queries etc.
'''
from abc import ABC, abstractmethod
import pandas as pd



class QueryExecutionError(Exception):
    """
    Custom exception with detailed error message.
    """
    def __init__(self, query):
        message = f"Query execution failed. Affected query: {query}"
        super().__init__(message)



class API(ABC):
    """
    Trait-like base class defining the structure of any data related API
    
    Rules:
        - environment variables must be initialized already when calling an API subclass
        - it is crucial to implemented following base methods when creating a new subclass
            - _connect()
            - _table()
            - close()
    """

    def __init__(self):
        self.conn = self._connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    @abstractmethod
    def _connect(self):
        '''Connection handling'''
        pass


    @abstractmethod
    def _table(self, **kwargs):
        '''
        Process **kwargs to return a valid string defining the source or target table.
        **kwargs specifies the required elements:
            example databricks: catalog="", schema="", table=""
        '''
        pass


    @abstractmethod
    def close(self):
        '''Close Connection'''
        if self.conn is None:
            print("no connection object to close. connection during object initialization probably failed.")
            return None
        
        self.conn.close()
        print("connection is closed successfully")
        return "OK"

    def delete_table(self, cursor=None, **kwargs):
        '''
        Delete a table from the database.
        - cursor: default None. Creates a new cursor instance. 
                  If called from another connection, pass the existing cursor to this argument.
        - **kwargs: specifies the table location, defined via _table() (mandatory class specific impl)
        '''
        close_cursor = False
        if cursor is None:
            cursor = self.conn.cursor()
            close_cursor = True

        # query definition
        _table = self._table(**kwargs)
        drop_query = f'''DROP TABLE IF EXISTS {_table};'''

        # query execution
        try:
            cursor.execute(drop_query)
        except Exception as e:
            print(f"Failed to delete table {_table}. Error: {e}")
            raise QueryExecutionError(drop_query) 
        
        # close cursor if it was created in this method
        finally:
            if close_cursor:
                cursor.close()

    def get_table(
        self,
        columns: list[str] | None = None,
        limit: int | None = None,
        sql_filter: str | None = None,
        **kwargs
    ) -> pd.DataFrame:
        '''
        Get a table and convert it to a pandas df.

        Arguments:
            :limit: optional - max. no of rows to fetch
            :columns: optional - list of columns to get -- ignore if all columns needed
            :sql filter: optional - sql string specifying filter criteria etc. -- example: WHERE id=='U0012'
            :**kwargs: specify the kwargs from self._table -- example: catalog="", schema="", table=""
        '''
        # query definition
        src_table = self._table(**kwargs)
        columns = ", ".join(columns) if columns else "*"
        limit_suffix = f' LIMIT {limit}' if limit else ""
        sql_filter = f' {sql_filter}' if sql_filter else ""

        query = f"""SELECT {columns} FROM {src_table}{sql_filter}{limit_suffix};"""

        # query execution
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)

                # define the pandas dataframe
                header = [tuple_[0].title().lower() for tuple_ in cursor.description]
                df = pd.DataFrame.from_records(cursor.fetchall(), columns=header, coerce_float=False)

                cursor.close()
                return df
            except Exception as e:
                print('failed to get table: ', src_table, 'Error: ', e)
                return None

        else:
            print(f"No cursor object available. Query execution impossible. Failed to get table {src_table}")
            raise ConnectionError


    def write_table(self, df:pd.DataFrame, chunksize:int=50000, **kwargs):
        '''
        Default Implementation: write pandas df to sql database.

        Arguments:
            :df: source dataframe that shall be inserted into a specific database schema
            :chunksize: max row number per write-iteration
            :kwargs: specifies the table location, defined via _table() (mandatory class specific impl)
        '''
        pass



    def chunk_df(self, df: pd.DataFrame, chunksize: int) -> list[pd.DataFrame]:
        """
        Splits a pandas dataframe into multiple chunks, depending on the chunksize (=maximum row-number)
        """      
        rows = df.shape[0]
        n_chunks = rows//chunksize +1
        chunks = []

        if df.empty:
            print("DataFrame is empty. No chunks created.")
            return chunks
        
        if n_chunks == 1:
            return [df]
        
        for i in range(n_chunks):
            start = i * chunksize
            end = start + chunksize
            chunk = df.iloc[start:end]
            if not chunk.empty:
                chunks.append(chunk)
        return chunks

    def chunk_list(self, l: list, chunksize: int) -> list[list]:
        """
        Splits a pandas dataframe into multiple chunks, depending on the chunksize (=maximum row-number)
        """      
        rows = len(l)
        n_chunks = rows//chunksize +1
        chunks = []

        if rows==0:
            print("list is empty. No chunks created.")
            return chunks
        
        if n_chunks == 1:
            return [l]
        
        for i in range(n_chunks):
            start = i * chunksize
            end = start + chunksize
            chunk = l[start:end]
            if len(chunk)>0:
                chunks.append(chunk)
        return chunks
