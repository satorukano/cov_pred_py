import psycopg2
from sortedcontainers import SortedSet
import json
from dotenv import load_dotenv
load_dotenv()

import os

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST =  os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    
    def get_execution_trace(self, test_trace_id):
        self.open_cur()
        self.cur.execute("SELECT * FROM trace.trace_in_source WHERE test_trace_id = %s", (test_trace_id,))
        traces = self.cur.fetchall()
        self.close_cur()
        return traces
    
    def get_trace_ids(self, registry_id):
        self.open_cur()
        self.cur.execute("SELECT test_trace_id FROM trace.trace_in_test WHERE registry_id = %s", (registry_id,))
        trace_ids = self.cur.fetchall()
        return trace_ids
    
    def open_cur(self):
        self.cur = self.conn.cursor()

    def close_cur(self):
        self.cur.close()
    
    def close_conn(self):
        self.conn.close()