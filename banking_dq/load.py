from sqlalchemy import text, inspect

def load_to_staging(df, table_name, engine):
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))
    df.to_sql(
        name=table_name,
        con=engine,
        schema="staging",
        if_exists="replace",
        index=False
    )

    
def load_exceptions(df, engine,business_date):
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dq"))
        if inspect(conn).has_table("exceptions", schema="dq"):
            conn.execute(text("Delete from dq.exceptions where business_date = :business_date"), 
                         {"business_date": business_date})   
    df.to_sql(
        name="exceptions",
        con=engine,
        schema="dq",
        if_exists="append",
        index=False
    )