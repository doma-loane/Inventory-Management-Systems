from app.extensions import db

def run_query(sql_query):
    """
    Run a raw SQL query and return the results.
    :param sql_query: The SQL query string
    :return: Query results
    """
    try:
        result = db.session.execute(sql_query)
        db.session.commit()  # Commit if the query modifies data
        return result.fetchall()  # Use .fetchall() for SELECT queries
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        raise RuntimeError(f"Failed to execute query: {e}")
