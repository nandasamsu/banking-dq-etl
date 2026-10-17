from sqlalchemy import text, inspect
    
def load_exceptions(df, engine,business_date):
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dq"))
        if inspect(conn).has_table("exceptions", schema="dq"):
            conn.execute(text("Delete from dq.exceptions where business_date = :business_date"), 
                         {"business_date": business_date})   
        df.to_sql(
            name="exceptions",
            con=conn,
            schema="dq",
            if_exists="append",
            index=False
        )

def load_table(df, table_name, engine, schema="staging"):
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        conn.execute(text(f"DROP TABLE IF EXISTS {schema}.{table_name} CASCADE"))
        df.to_sql(name=table_name, 
                  con=conn, 
                  schema=schema, 
                  if_exists="replace", 
                  index=False)

def run_sql_file(path, engine):
    sql = open(path).read()
    with engine.begin() as conn:
        for statement in sql.split(";"):
            if statement.strip():
                conn.execute(text(statement))