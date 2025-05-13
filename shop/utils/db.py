from ..singleton import DatabaseConnectionSingleton

def get_db_connection():
    """
    Wrapper to abstract away the singleton access logic.
    This follows the Law of Demeter and keeps views clean.
    """
    return DatabaseConnectionSingleton().get_connection()
