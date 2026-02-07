package com.restaurant.analytics.analytics;

import com.restaurant.analytics.model.RestaurantOrder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class AnomalyDetectionService {
    
    private static final double ANOMALY_THRESHOLD = 2.0; // Standard deviations
    
    public Map<String, Object> detectServiceAnomalies(List<RestaurantOrder> orders) {
        Map<String, Object> anomalies = new HashMap<>();
        
        anomalies.put("preparationTimeAnomalies", detectPreparationTimeAnomalies(orders));
        anomalies.put("orderVolumeAnomalies", detectOrderVolumeAnomalies(orders));
        anomalies.put("revenueAnomalies", detectRevenueAnomalies(orders));
        anomalies.put("customerBehaviorAnomalies", detectCustomerBehaviorAnomalies(orders));
        anomalies.put("alertLogs", generateAlertLogs(orders));
        
        return anomalies;
    }
    
    private List<Map<String, Object>> detectPreparationTimeAnomalies(List<RestaurantOrder> orders) {
        List<Map<String, Object>> anomalies = new ArrayList<>();
        
        // Calculate preparation times
        List<Long> prepTimes = orders.stream()
                .filter(order -> order.getPrepStarted() != null && order.getPrepFinished() != null)
                .map(order -> java.time.Duration.between(order.getPrepStarted(), order.getPrepFinished()).toMinutes())
                .collect(Collectors.toList());
        
        if (prepTimes.isEmpty()) return anomalies;
        
        double mean = prepTimes.stream().mapToLong(Long::longValue).average().orElse(0.0);
        double stdDev = calculateStandardDeviation(prepTimes, mean);
        
        // Find anomalous preparation times
        orders.stream()
                .filter(order -> order.getPrepStarted() != null && order.getPrepFinished() != null)
                .forEach(order -> {
                    long prepTime = java.time.Duration.between(order.getPrepStarted(), order.getPrepFinished()).toMinutes();
                    double zScore = Math.abs((prepTime - mean) / stdDev);
                    
                    if (zScore > ANOMALY_THRESHOLD) {
                        Map<String, Object> anomaly = new HashMap<>();
                        anomaly.put("orderId", order.getOrderId());
                        anomaly.put("outletId", order.getOutletId());
                        anomaly.put("preparationTime", prepTime);
                        anomaly.put("expectedTime", mean);
                        anomaly.put("zScore", zScore);
                        anomaly.put("severity", getSeverityLevel(zScore));
                        anomaly.put("timestamp", order.getPrepStarted());
                        anomaly.put("type", "PREPARATION_TIME");
                        anomalies.add(anomaly);
                    }
                });
        
        return anomalies;
    }
    
    private List<Map<String, Object>> detectOrderVolumeAnomalies(List<RestaurantOrder> orders) {
        List<Map<String, Object>> anomalies = new ArrayList<>();
        
        // Group orders by hour and outlet
        Map<String, Map<Integer, Long>> outletHourlyOrders = orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getOutletId,
                    Collectors.groupingBy(
                        order -> order.getOrderPlaced().getHour(),
                        Collectors.counting()
                    )
                ));
        
        for (Map.Entry<String, Map<Integer, Long>> outletEntry : outletHourlyOrders.entrySet()) {
            String outletId = outletEntry.getKey();
            Map<Integer, Long> hourlyOrders = outletEntry.getValue();
            
            List<Long> orderCounts = new ArrayList<>(hourlyOrders.values());
            if (orderCounts.isEmpty()) continue;
            
            double mean = orderCounts.stream().mapToLong(Long::longValue).average().orElse(0.0);
            double stdDev = calculateStandardDeviation(orderCounts, mean);
            
            for (Map.Entry<Integer, Long> hourEntry : hourlyOrders.entrySet()) {
                int hour = hourEntry.getKey();
                long orderCount = hourEntry.getValue();
                double zScore = Math.abs((orderCount - mean) / stdDev);
                
                if (zScore > ANOMALY_THRESHOLD) {
                    Map<String, Object> anomaly = new HashMap<>();
                    anomaly.put("outletId", outletId);
                    anomaly.put("hour", hour);
                    anomaly.put("orderCount", orderCount);
                    anomaly.put("expectedCount", mean);
                    anomaly.put("zScore", zScore);
                    anomaly.put("severity", getSeverityLevel(zScore));
                    anomaly.put("type", "ORDER_VOLUME");
                    anomalies.add(anomaly);
                }
            }
        }
        
        return anomalies;
    }
    
    private List<Map<String, Object>> detectRevenueAnomalies(List<RestaurantOrder> orders) {
        List<Map<String, Object>> anomalies = new ArrayList<>();
        
        // Daily revenue by outlet
        DateTimeFormatter dayFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        
        Map<String, Map<String, Double>> outletDailyRevenue = orders.stream()
                .filter(order -> order.getOrderPlaced() != null && order.getTotalPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getOutletId,
                    Collectors.groupingBy(
                        order -> order.getOrderPlaced().format(dayFormatter),
                        Collectors.summingDouble(order -> order.getTotalPriceLkr().doubleValue())
                    )
                ));
        
        for (Map.Entry<String, Map<String, Double>> outletEntry : outletDailyRevenue.entrySet()) {
            String outletId = outletEntry.getKey();
            Map<String, Double> dailyRevenue = outletEntry.getValue();
            
            List<Double> revenueValues = new ArrayList<>(dailyRevenue.values());
            if (revenueValues.isEmpty()) continue;
            
            double mean = revenueValues.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
            double stdDev = calculateStandardDeviation(revenueValues, mean);
            
            for (Map.Entry<String, Double> dayEntry : dailyRevenue.entrySet()) {
                String day = dayEntry.getKey();
                double revenue = dayEntry.getValue();
                double zScore = Math.abs((revenue - mean) / stdDev);
                
                if (zScore > ANOMALY_THRESHOLD) {
                    Map<String, Object> anomaly = new HashMap<>();
                    anomaly.put("outletId", outletId);
                    anomaly.put("date", day);
                    anomaly.put("revenue", revenue);
                    anomaly.put("expectedRevenue", mean);
                    anomaly.put("zScore", zScore);
                    anomaly.put("severity", getSeverityLevel(zScore));
                    anomaly.put("type", "REVENUE");
                    anomalies.add(anomaly);
                }
            }
        }
        
        return anomalies;
    }
    
    private List<Map<String, Object>> detectCustomerBehaviorAnomalies(List<RestaurantOrder> orders) {
        List<Map<String, Object>> anomalies = new ArrayList<>();
        
        // Detect unusual customer spending patterns
        Map<String, List<RestaurantOrder>> customerOrders = orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getCustomerId));
        
        for (Map.Entry<String, List<RestaurantOrder>> customerEntry : customerOrders.entrySet()) {
            String customerId = customerEntry.getKey();
            List<RestaurantOrder> customerOrderList = customerEntry.getValue();
            
            List<Double> orderValues = customerOrderList.stream()
                    .filter(order -> order.getTotalPriceLkr() != null)
                    .map(order -> order.getTotalPriceLkr().doubleValue())
                    .collect(Collectors.toList());
            
            if (orderValues.size() < 3) continue; // Need at least 3 orders for pattern detection
            
            double mean = orderValues.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
            double stdDev = calculateStandardDeviation(orderValues, mean);
            
            // Check for unusually high spending orders
            for (RestaurantOrder order : customerOrderList) {
                if (order.getTotalPriceLkr() != null) {
                    double orderValue = order.getTotalPriceLkr().doubleValue();
                    double zScore = Math.abs((orderValue - mean) / stdDev);
                    
                    if (zScore > ANOMALY_THRESHOLD) {
                        Map<String, Object> anomaly = new HashMap<>();
                        anomaly.put("customerId", customerId);
                        anomaly.put("orderId", order.getOrderId());
                        anomaly.put("orderValue", orderValue);
                        anomaly.put("expectedValue", mean);
                        anomaly.put("zScore", zScore);
                        anomaly.put("severity", getSeverityLevel(zScore));
                        anomaly.put("timestamp", order.getOrderPlaced());
                        anomaly.put("type", "CUSTOMER_SPENDING");
                        anomalies.add(anomaly);
                    }
                }
            }
        }
        
        return anomalies;
    }
    
    private List<Map<String, Object>> generateAlertLogs(List<RestaurantOrder> orders) {
        List<Map<String, Object>> alerts = new ArrayList<>();
        
        // Generate alerts based on various conditions
        
        // Alert for orders with very long preparation times
        orders.stream()
                .filter(order -> order.getPrepStarted() != null && order.getPrepFinished() != null)
                .forEach(order -> {
                    long prepTime = java.time.Duration.between(order.getPrepStarted(), order.getPrepFinished()).toMinutes();
                    if (prepTime > 60) { // More than 1 hour
                        Map<String, Object> alert = new HashMap<>();
                        alert.put("alertId", "PREP_TIME_" + order.getOrderId());
                        alert.put("type", "LONG_PREPARATION_TIME");
                        alert.put("severity", "HIGH");
                        alert.put("message", "Order " + order.getOrderId() + " took " + prepTime + " minutes to prepare");
                        alert.put("orderId", order.getOrderId());
                        alert.put("outletId", order.getOutletId());
                        alert.put("timestamp", order.getPrepStarted());
                        alerts.add(alert);
                    }
                });
        
        // Alert for failed orders
        orders.stream()
                .filter(order -> "Failed".equalsIgnoreCase(order.getStatus()) || 
                               "Cancelled".equalsIgnoreCase(order.getStatus()))
                .forEach(order -> {
                    Map<String, Object> alert = new HashMap<>();
                    alert.put("alertId", "FAILED_ORDER_" + order.getOrderId());
                    alert.put("type", "FAILED_ORDER");
                    alert.put("severity", "MEDIUM");
                    alert.put("message", "Order " + order.getOrderId() + " has status: " + order.getStatus());
                    alert.put("orderId", order.getOrderId());
                    alert.put("outletId", order.getOutletId());
                    alert.put("timestamp", order.getOrderPlaced());
                    alerts.add(alert);
                });
        
        // Alert for high-value orders (potential fraud detection)
        double highValueThreshold = orders.stream()
                .filter(order -> order.getTotalPriceLkr() != null)
                .mapToDouble(order -> order.getTotalPriceLkr().doubleValue())
                .max()
                .orElse(0.0) * 0.9; // Top 10% of orders
        
        orders.stream()
                .filter(order -> order.getTotalPriceLkr() != null && 
                               order.getTotalPriceLkr().doubleValue() > highValueThreshold)
                .forEach(order -> {
                    Map<String, Object> alert = new HashMap<>();
                    alert.put("alertId", "HIGH_VALUE_" + order.getOrderId());
                    alert.put("type", "HIGH_VALUE_ORDER");
                    alert.put("severity", "LOW");
                    alert.put("message", "High value order: " + order.getTotalPriceLkr() + " LKR");
                    alert.put("orderId", order.getOrderId());
                    alert.put("customerId", order.getCustomerId());
                    alert.put("timestamp", order.getOrderPlaced());
                    alerts.add(alert);
                });
        
        return alerts;
    }
    
    private double calculateStandardDeviation(List<? extends Number> values, double mean) {
        if (values.size() <= 1) return 0.0;
        
        double sumSquaredDiffs = values.stream()
                .mapToDouble(value -> Math.pow(value.doubleValue() - mean, 2))
                .sum();
        
        return Math.sqrt(sumSquaredDiffs / (values.size() - 1));
    }
    
    private String getSeverityLevel(double zScore) {
        if (zScore > 3.0) return "CRITICAL";
        else if (zScore > 2.5) return "HIGH";
        else if (zScore > 2.0) return "MEDIUM";
        else return "LOW";
    }
}