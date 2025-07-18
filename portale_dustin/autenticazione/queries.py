from .crate_client import crate_db


#query di test su tabelle di sistema di crate
SUMMITS_QUERY = """
    SELECT country, mountain, coordinates, height 
    FROM sys.summits 
    ORDER BY country
"""

def get_summits():
    """Restituisce tutti i summit"""
    return crate_db.execute_query(SUMMITS_QUERY)

def get_summits_by_country(country):
    """Restituisce i summit per paese"""
    query = """
        SELECT mountain, coordinates, height 
        FROM sys.summits 
        WHERE country = :country
        ORDER BY height DESC
    """
    return crate_db.execute_query(query, {'country': country})