import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Copies data into staging tables on Redshift
    from S3.
    Parameters:
    - cur: cursor object that allows Python to execute 
    Redshift commands in a database session
    - conn: connection created to the database
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Inserts data from staging tables to analytic
    tables on Redshift.
    Parameters:
    - cur: cursor object that allows Python to execute 
    Redshift commands in a database session
    - conn: connection created to the database
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Connects to the redshift cluster then copys data
    into staging tables and inserts data into redshift
    tables.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()