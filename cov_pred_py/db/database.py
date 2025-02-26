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
    
    def get_execution_trace(self, signature):
        self.open_cur()
        self.cur.execute("SELECT * FROM trace.trace_in_source LEFT JOIN trace.trace_in_test ON trace.trace_in_source.test_trace_id = trace.trace_in_test.test_trace_id WHERE signature = %s", (signature,))
        traces = self.cur.fetchall()
        self.close_cur()
        return traces
    
    def get_signatures(self, registry_id):
        self.open_cur()
        self.cur.execute("SELECT DISTINCT signature FROM trace.trace_in_test WHERE registry_id = %s", (registry_id,))
        signatures = self.cur.fetchall()
        return signatures
    
    def get_log(self, signature, registry_id):
        self.open_cur()
        self.cur.execute("SELECT log.log_statement.statement FROM log.log_statement LEFT JOIN log.logs_in_test ON log.log_statement.test_method_id = log.logs_in_test.test_method_id WHERE signature = %s AND registry_id = %s", (signature, registry_id))
        logs = self.cur.fetchall()
        return logs
    
    def open_cur(self):
        self.cur = self.conn.cursor()

    def close_cur(self):
        self.cur.close()
    
    def close_conn(self):
        self.conn.close()