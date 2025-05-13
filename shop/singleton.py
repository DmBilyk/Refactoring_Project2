import threading


class DatabaseConnectionSingleton:
    """
    Thread-safe Singleton for managing database connection state.
    Note: In Django, real DB management is handled by the ORM.
    """

    _instance = None
    _lock = threading.Lock()  # ensures thread-safety

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # double-checked locking
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize_connection()
        return cls._instance

    def _initialize_connection(self):
        """
        Simulates initializing database connection settings.
        """
        self.is_connected = True
        self.connection_pool_size = 10
        self.timeout = 30

    def get_connection(self):
        """
        Simulates returning the current database connection.
        """
        if not self.is_connected:
            self._initialize_connection()
        return self

    def close_connection(self):
        """
        Simulates closing the database connection.
        """
        self.is_connected = False

    def __repr__(self):
        return (f"<DatabaseConnectionSingleton connected={self.is_connected} "
                f"pool_size={self.connection_pool_size} timeout={self.timeout}>")
