from supabase import create_client
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor


load_dotenv()
#If using cloud based supabase, use this

# supabase_url = os.getenv('SUPABASE_URL')
# supabase_key = os.getenv('SUPABASE_KEY')
# supabase = create_client(supabase_url, supabase_key)



#If using local based postgres, uncomment below this
conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5434'),   # IMPORTANT: docker host port
    dbname=os.getenv('POSTGRES_DB', 'postgres'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'Abcd1234'),
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()




class LocalSupabaseResult:
    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error


class LocalSupabaseTable:
    def __init__(self, conn, table):
        self.conn = conn
        self.table = table
        self._select = "*"
        self._where = []
        self._params = []
        self._limit = None
        self._update_values = None   # track UPDATE payload

    def select(self, columns="*"):
        self._select = columns
        return self

    def eq(self, column, value):
        self._where.append(f"{column} = %s")
        self._params.append(value)
        return self

    def limit(self, n):
        self._limit = int(n)
        return self

    def update(self, values: dict):
        """Mimic supabase.table(...).update({...})"""
        self._update_values = values
        return self

    def execute(self):
        # If it's an UPDATE
        if self._update_values is not None:
            set_clauses = []
            params = []

            for col, val in self._update_values.items():
                set_clauses.append(f"{col} = %s")
                params.append(val)

            sql = f"UPDATE {self.table} SET " + ", ".join(set_clauses)

            if self._where:
                sql += " WHERE " + " AND ".join(self._where)
                params.extend(self._params)

            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                self.conn.commit()
                # return how many rows were touched, similar-ish to Supabase
                return LocalSupabaseResult(
                    data={"rowcount": cur.rowcount},
                    error=None
                )

        # Otherwise treat it as a SELECT
        sql = f"SELECT {self._select} FROM {self.table}"
        params = list(self._params)

        if self._where:
            sql += " WHERE " + " AND ".join(self._where)
        if self._limit is not None:
            sql += " LIMIT %s"
            params.append(self._limit)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        return LocalSupabaseResult(data=rows, error=None)


class LocalSupabaseClient:
    def __init__(self, conn):
        self.conn = conn

    def table(self, table_name: str):
        return LocalSupabaseTable(self.conn, table_name)


supabase = LocalSupabaseClient(conn)