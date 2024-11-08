import sqlite3

def filters_to_query(filters: dict, logic = "AND"):
    '''
    Converts dictionary of `filters` into `sqlite` query
    '''
    query_filters = ""

    if filters != None:
        filters_list = []

        for field, condition in filters.items():
            query = f'{field} = "{condition}"'
            filters_list.append(query)
        
        query_filters = "where " + f" {logic}".join(filters_list)
    return query_filters

class Database:
    def __init__(self, path: str):
        '''
        Loads the database from the `path`
        '''
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
    
    def create(self, table: str, data: dict):
        '''
        Appends `data` into the database at `table`
        '''
        fields = []
        values = []

        for key, value in data.items():
            fields.append(key)
            values.append(value)

        marks = ', '.join(['?'] * len(fields))

        fields = ', '.join(fields)
        values = tuple(values)

        self.cursor.execute(f"INSERT INTO {table}({fields}) VALUES({marks})", values)
        self.connection.commit()
    
    def update(self, table: str, data: dict, filters: dict = None, logic: str = "AND"):
        '''
        Replace value in the `table` with `data`
        \n`filters` - if not null, replaces only where the specified value is equal to filter
        '''
        query_filters = filters_to_query(filters, logic)

        for key, value in data.items():
            self.cursor.execute(f"UPDATE {table} SET {key} = ? {query_filters}", (value,))
        
        self.connection.commit()

    def read(self, table: str, filters: dict = None, logic: str = "AND") -> dict | list[dict] | None:
        '''
        Returns data as a dictionary. If filters can't be satisfied, returns `None`
        \n`filters` - if not null, returns a single row, else returns the whole table
        '''
        query_filters = filters_to_query(filters, logic)

        self.cursor.execute(f"SELECT * FROM {table} {query_filters}")

        keys = [description[0] for description in self.cursor.description]
        if filters:
            values = self.cursor.fetchone()
            if not values:
                return None
            return dict(zip(keys, values))
        
        values = self.cursor.fetchall()
        return [dict(zip(keys, row)) for row in values]

    def delete(self, table: str, filters: dict, logic: str = "AND"):
        '''
        Removes data in `table`
        \n`filters` - removes only those where the specified key is equal to filter
        '''
        query_filters = filters_to_query(filters, logic)

        self.cursor.execute(f"DELETE FROM {table} {query_filters}")
        self.connection.commit()