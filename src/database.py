from supabase import create_client
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import json   

load_dotenv()
#If using cloud based supabase, use this

# supabase_url = os.getenv('SUPABASE_URL')
# supabase_key = os.getenv('SUPABASE_KEY')
# supabase = create_client(supabase_url, supabase_key)



# If using local based postgres, uncomment below this
conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5434'),   # IMPORTANT: docker host port
    dbname=os.getenv('POSTGRES_DB', 'postgres'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'Abcd1234'),
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()


# NEW: simple cache so we only fetch column list once per table
_COLUMN_CACHE = {}


def get_table_columns(conn, table_name):
    """
    Return list of column names for a given table in the public schema.
    Cached so we don't hit information_schema repeatedly.
    """
    if table_name in _COLUMN_CACHE:
        return _COLUMN_CACHE[table_name]

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
            ORDER BY ordinal_position
            """,
            (table_name,),
        )
        cols = [row[0] for row in cur.fetchall()]

    _COLUMN_CACHE[table_name] = cols
    return cols


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
        # NEW: build a select clause that auto-converts geom → GeoJSON when using "*"
        select_clause = self._select

        if self._select.strip() == "*":
            # Try to introspect columns for this table
            try:
                cols = get_table_columns(self.conn, self.table)
            except Exception:
                cols = None

            if cols and "geom" in cols:
                # Rebuild explicit column list, replacing geom with ST_AsGeoJSON(...)
                select_parts = []
                for col in cols:
                    if col == "geom":
                        select_parts.append('ST_AsGeoJSON("geom")::json AS geom')
                    else:
                        # quote to handle spaces / weird names like "daily rainfall total (mm)"
                        select_parts.append(f'"{col}"')
                select_clause = ", ".join(select_parts)
            else:
                # no geom column, keep "*"
                select_clause = "*"

        sql = f"SELECT {select_clause} FROM {self.table}"
        params = list(self._params)

        if self._where:
            sql += " WHERE " + " AND ".join(self._where)
        if self._limit is not None:
            sql += " LIMIT %s"
            params.append(self._limit)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        # NEW: normalize geom → always GeoJSON object
        processed_rows = []
        for row in rows:
            row = dict(row)  # RealDictRow -> plain dict

            if "geom" in row:
                val = row["geom"]

                # Case 1: already a dict (e.g. Supabase) → leave as is
                if isinstance(val, dict):
                    pass
                # Case 2: JSON text from ST_AsGeoJSON(...)::json
                elif isinstance(val, str):
                    new_geom = None

                    # Try parsing as JSON text
                    try:
                        new_geom = json.loads(val)
                    except Exception:
                        # If that fails, assume it's WKB hex from PostGIS and
                        # fall back to lat/long if available
                        if "longitude" in row and "latitude" in row:
                            new_geom = {
                                "type": "Point",
                                "coordinates": [row["longitude"], row["latitude"]],
                            }

                    if new_geom is not None:
                        row["geom"] = new_geom

            processed_rows.append(row)

        return LocalSupabaseResult(data=processed_rows, error=None)


class LocalSupabaseClient:
    def __init__(self, conn):
        self.conn = conn

    def table(self, table_name: str):
        return LocalSupabaseTable(self.conn, table_name)


supabase = LocalSupabaseClient(conn)