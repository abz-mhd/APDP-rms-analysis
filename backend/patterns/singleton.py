"""
Singleton Pattern - Ensure only one instance exists
Use Case: Configuration, Logger, Database Connection
"""

from threading import Lock
from typing import Dict, Any


class SingletonMeta(type):
    """
    Thread-safe Singleton metaclass
    Design Pattern: Singleton with thread safety
    """
    
    _instances: Dict[type, Any] = {}
    _lock: Lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        """
        Thread-safe singleton implementation
        Clean Code: Double-checked locking pattern
        """
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        
        return cls._instances[cls]


class ConfigurationManager(metaclass=SingletonMeta):
    """
    Singleton configuration manager
    Use Case: Global application configuration
    """
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._config: Dict[str, Any] = {}
            self._initialized = True
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self._config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()
    
    def load_from_dict(self, config: Dict[str, Any]) -> None:
        """Load configuration from dictionary"""
        self._config.update(config)
    
    def clear(self) -> None:
        """Clear all configuration"""
        self._config.clear()


class ApplicationLogger(metaclass=SingletonMeta):
    """
    Singleton logger
    Use Case: Centralized logging
    """
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._logs: list = []
            self._log_level = 'INFO'
            self._initialized = True
    
    def set_level(self, level: str) -> None:
        """Set logging level"""
        self._log_level = level.upper()
    
    def info(self, message: str) -> None:
        """Log info message"""
        self._log('INFO', message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self._log('WARNING', message)
    
    def error(self, message: str, exception: Exception = None) -> None:
        """Log error message"""
        error_msg = f"{message}"
        if exception:
            error_msg += f" - {str(exception)}"
        self._log('ERROR', error_msg)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self._log('DEBUG', message)
    
    def _log(self, level: str, message: str) -> None:
        """Internal logging method"""
        from datetime import datetime
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        
        self._logs.append(log_entry)
        
        # Print to console
        print(f"[{log_entry['timestamp']}] {level}: {message}")
    
    def get_logs(self, level: str = None) -> list:
        """Get logs, optionally filtered by level"""
        if level:
            return [log for log in self._logs if log['level'] == level.upper()]
        return self._logs.copy()
    
    def clear_logs(self) -> None:
        """Clear all logs"""
        self._logs.clear()


class DatabaseConnectionPool(metaclass=SingletonMeta):
    """
    Singleton database connection pool
    Use Case: Manage database connections
    """
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._connections: Dict[str, Any] = {}
            self._max_connections = 10
            self._initialized = True
    
    def get_connection(self, connection_id: str) -> Any:
        """Get or create connection"""
        if connection_id not in self._connections:
            if len(self._connections) >= self._max_connections:
                raise RuntimeError("Maximum connections reached")
            
            # Create new connection (placeholder)
            self._connections[connection_id] = {
                'id': connection_id,
                'created_at': __import__('datetime').datetime.now(),
                'active': True
            }
        
        return self._connections[connection_id]
    
    def release_connection(self, connection_id: str) -> None:
        """Release connection"""
        if connection_id in self._connections:
            self._connections[connection_id]['active'] = False
    
    def close_all(self) -> None:
        """Close all connections"""
        self._connections.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        active = sum(1 for conn in self._connections.values() if conn.get('active', False))
        return {
            'total_connections': len(self._connections),
            'active_connections': active,
            'max_connections': self._max_connections
        }


# Example usage
if __name__ == "__main__":
    # Test Singleton pattern
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    
    config1.set('app_name', 'RestaurantIQ')
    
    # Both instances should be the same
    assert config1 is config2
    assert config2.get('app_name') == 'RestaurantIQ'
    
    print("✅ Singleton pattern working correctly!")
    
    # Test Logger
    logger1 = ApplicationLogger()
    logger2 = ApplicationLogger()
    
    logger1.info("Test message")
    
    assert logger1 is logger2
    assert len(logger2.get_logs()) > 0
    
    print("✅ Singleton logger working correctly!")
