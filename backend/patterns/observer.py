"""
Observer Pattern - Event notification system
Use Case: Analytics events, data changes, notifications
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


class IObserver(ABC):
    """
    Observer interface
    SOLID: Interface Segregation Principle
    """
    
    @abstractmethod
    def update(self, event: str, data: Dict[str, Any]) -> None:
        """Receive update notification"""
        pass


class ISubject(ABC):
    """
    Subject interface
    SOLID: Dependency Inversion Principle
    """
    
    @abstractmethod
    def attach(self, observer: IObserver) -> None:
        """Attach an observer"""
        pass
    
    @abstractmethod
    def detach(self, observer: IObserver) -> None:
        """Detach an observer"""
        pass
    
    @abstractmethod
    def notify(self, event: str, data: Dict[str, Any]) -> None:
        """Notify all observers"""
        pass


class AnalyticsEventManager(ISubject):
    """
    Concrete subject for analytics events
    Design Pattern: Observer pattern implementation
    """
    
    def __init__(self):
        self._observers: List[IObserver] = []
        self._event_history: List[Dict[str, Any]] = []
    
    def attach(self, observer: IObserver) -> None:
        """
        Attach observer
        Clean Code: Clear method name and purpose
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: IObserver) -> None:
        """
        Detach observer
        Clean Code: Symmetric with attach
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: str, data: Dict[str, Any]) -> None:
        """
        Notify all observers
        Clean Code: Single responsibility - just notify
        """
        event_data = {
            'event': event,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        self._event_history.append(event_data)
        
        for observer in self._observers:
            try:
                observer.update(event, data)
            except Exception as e:
                print(f"Error notifying observer: {e}")
    
    def get_event_history(self) -> List[Dict[str, Any]]:
        """Get event history"""
        return self._event_history.copy()
    
    def clear_history(self) -> None:
        """Clear event history"""
        self._event_history.clear()


class LoggingObserver(IObserver):
    """
    Concrete observer for logging
    Single Responsibility: Only handles logging
    """
    
    def __init__(self, log_file: str = None):
        self._log_file = log_file
        self._logs: List[str] = []
    
    def update(self, event: str, data: Dict[str, Any]) -> None:
        """
        Log the event
        Clean Code: Clear implementation
        """
        log_message = f"[{datetime.now().isoformat()}] Event: {event} - Data: {data}"
        self._logs.append(log_message)
        print(f"📝 LOG: {log_message}")
        
        if self._log_file:
            self._write_to_file(log_message)
    
    def _write_to_file(self, message: str) -> None:
        """Write log to file"""
        try:
            with open(self._log_file, 'a') as f:
                f.write(message + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def get_logs(self) -> List[str]:
        """Get all logs"""
        return self._logs.copy()


class MetricsObserver(IObserver):
    """
    Concrete observer for metrics collection
    Single Responsibility: Only handles metrics
    """
    
    def __init__(self):
        self._metrics: Dict[str, int] = {}
    
    def update(self, event: str, data: Dict[str, Any]) -> None:
        """
        Collect metrics
        Clean Code: Focused on metrics
        """
        # Count events
        self._metrics[event] = self._metrics.get(event, 0) + 1
        
        print(f"📊 METRICS: Event '{event}' count: {self._metrics[event]}")
    
    def get_metrics(self) -> Dict[str, int]:
        """Get all metrics"""
        return self._metrics.copy()
    
    def reset_metrics(self) -> None:
        """Reset all metrics"""
        self._metrics.clear()


class AlertObserver(IObserver):
    """
    Concrete observer for alerts
    Single Responsibility: Only handles alerts
    """
    
    def __init__(self, threshold: int = 100):
        self._threshold = threshold
        self._alerts: List[Dict[str, Any]] = []
    
    def update(self, event: str, data: Dict[str, Any]) -> None:
        """
        Check for alert conditions
        Clean Code: Clear alert logic
        """
        # Example: Alert if order count exceeds threshold
        if event == 'order_created' and data.get('count', 0) > self._threshold:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'event': event,
                'message': f"High order volume detected: {data.get('count')} orders",
                'severity': 'HIGH'
            }
            self._alerts.append(alert)
            print(f"🚨 ALERT: {alert['message']}")
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get all alerts"""
        return self._alerts.copy()
    
    def clear_alerts(self) -> None:
        """Clear all alerts"""
        self._alerts.clear()


class CacheInvalidationObserver(IObserver):
    """
    Concrete observer for cache invalidation
    Single Responsibility: Only handles cache invalidation
    """
    
    def __init__(self, cache_service: Any = None):
        self._cache_service = cache_service
        self._invalidation_count = 0
    
    def update(self, event: str, data: Dict[str, Any]) -> None:
        """
        Invalidate cache on data changes
        Clean Code: Clear cache invalidation logic
        """
        # Invalidate cache on data modification events
        if event in ['data_updated', 'data_deleted', 'data_created']:
            if self._cache_service:
                self._cache_service.clear()
            
            self._invalidation_count += 1
            print(f"🗑️  CACHE: Invalidated cache due to '{event}' event")
    
    def get_invalidation_count(self) -> int:
        """Get cache invalidation count"""
        return self._invalidation_count


# Example usage
if __name__ == "__main__":
    # Create event manager
    event_manager = AnalyticsEventManager()
    
    # Create observers
    logger = LoggingObserver()
    metrics = MetricsObserver()
    alerts = AlertObserver(threshold=50)
    
    # Attach observers
    event_manager.attach(logger)
    event_manager.attach(metrics)
    event_manager.attach(alerts)
    
    # Trigger events
    event_manager.notify('order_created', {'count': 10, 'outlet': 'OUT01'})
    event_manager.notify('order_created', {'count': 75, 'outlet': 'OUT02'})
    event_manager.notify('data_updated', {'table': 'orders'})
    
    # Check results
    print("\n📊 Metrics:", metrics.get_metrics())
    print("🚨 Alerts:", len(alerts.get_alerts()))
    print("📝 Logs:", len(logger.get_logs()))
    
    print("\n✅ Observer pattern working correctly!")
