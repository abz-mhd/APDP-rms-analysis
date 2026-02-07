package com.restaurant.analytics.analytics;

import com.restaurant.analytics.model.RestaurantOrder;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class BranchPerformanceAnalytics {
    
    public Map<String, Object> generateBranchPerformanceAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> analysis = new HashMap<>();
        
        analysis.put("branchDashboards", generateBranchDashboards(orders));
        analysis.put("branchRankings", generateBranchRankings(orders));
        analysis.put("performanceMetrics", generatePerformanceMetrics(orders));
        analysis.put("efficiencyAnalysis", generateEfficiencyAnalysis(orders));
        analysis.put("customerSatisfactionMetrics", generateCustomerSatisfactionMetrics(orders));
        
        return analysis;
    }
    
    private Map<String, Map<String, Object>> generateBranchDashboards(List<RestaurantOrder> orders) {
        return orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> {
                        String outletId = entry.getKey();
                        List<RestaurantOrder> branchOrders = entry.getValue();
                        
                        Map<String, Object> dashboard = new HashMap<>();
                        
                        // Basic metrics
                        dashboard.put("totalOrders", branchOrders.size());
                        dashboard.put("totalRevenue", calculateTotalRevenue(branchOrders));
                        dashboard.put("averageOrderValue", calculateAverageOrderValue(branchOrders));
                        dashboard.put("uniqueCustomers", branchOrders.stream()
                                .map(RestaurantOrder::getCustomerId)
                                .distinct().count());
                        
                        // Branch details
                        if (!branchOrders.isEmpty()) {
                            RestaurantOrder sample = branchOrders.get(0);
                            dashboard.put("branchName", sample.getOutletName());
                            dashboard.put("borough", sample.getBorough());
                            dashboard.put("capacity", sample.getCapacity());
                        }
                        
                        return dashboard;
                    }
                ));
    }  
  
    private List<Map<String, Object>> generateBranchRankings(List<RestaurantOrder> orders) {
        Map<String, List<RestaurantOrder>> branchOrders = orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId));
        
        return branchOrders.entrySet().stream()
                .map(entry -> {
                    String outletId = entry.getKey();
                    List<RestaurantOrder> branchOrderList = entry.getValue();
                    
                    Map<String, Object> ranking = new HashMap<>();
                    ranking.put("outletId", outletId);
                    ranking.put("revenue", calculateTotalRevenue(branchOrderList));
                    ranking.put("orderCount", branchOrderList.size());
                    ranking.put("averageOrderValue", calculateAverageOrderValue(branchOrderList));
                    ranking.put("customerCount", branchOrderList.stream()
                            .map(RestaurantOrder::getCustomerId)
                            .distinct().count());
                    
                    if (!branchOrderList.isEmpty()) {
                        RestaurantOrder sample = branchOrderList.get(0);
                        ranking.put("branchName", sample.getOutletName());
                        ranking.put("borough", sample.getBorough());
                    }
                    
                    return ranking;
                })
                .sorted((a, b) -> Double.compare((Double) b.get("revenue"), (Double) a.get("revenue")))
                .collect(Collectors.toList());
    }
    
    private Map<String, Map<String, Object>> generatePerformanceMetrics(List<RestaurantOrder> orders) {
        return orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> {
                        List<RestaurantOrder> branchOrders = entry.getValue();
                        Map<String, Object> metrics = new HashMap<>();
                        
                        // Revenue metrics
                        metrics.put("totalRevenue", calculateTotalRevenue(branchOrders));
                        metrics.put("averageOrderValue", calculateAverageOrderValue(branchOrders));
                        
                        // Operational metrics
                        metrics.put("averagePreparationTime", calculateAveragePreparationTime(branchOrders));
                        metrics.put("orderCompletionRate", calculateOrderCompletionRate(branchOrders));
                        
                        // Customer metrics
                        metrics.put("customerRetentionRate", calculateCustomerRetentionRate(branchOrders));
                        metrics.put("repeatCustomerRate", calculateRepeatCustomerRate(branchOrders));
                        
                        return metrics;
                    }
                ));
    }
    
    private Map<String, Map<String, Object>> generateEfficiencyAnalysis(List<RestaurantOrder> orders) {
        return orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> {
                        List<RestaurantOrder> branchOrders = entry.getValue();
                        Map<String, Object> efficiency = new HashMap<>();
                        
                        // Service efficiency
                        efficiency.put("averageServiceTime", calculateAverageServiceTime(branchOrders));
                        efficiency.put("peakHourPerformance", calculatePeakHourPerformance(branchOrders));
                        
                        // Capacity utilization
                        if (!branchOrders.isEmpty()) {
                            Integer capacity = branchOrders.get(0).getCapacity();
                            if (capacity != null) {
                                efficiency.put("capacityUtilization", calculateCapacityUtilization(branchOrders, capacity));
                            }
                        }
                        
                        return efficiency;
                    }
                ));
    }
    
    private Map<String, Map<String, Object>> generateCustomerSatisfactionMetrics(List<RestaurantOrder> orders) {
        return orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> {
                        List<RestaurantOrder> branchOrders = entry.getValue();
                        Map<String, Object> satisfaction = new HashMap<>();
                        
                        // Order success rate
                        satisfaction.put("orderSuccessRate", calculateOrderSuccessRate(branchOrders));
                        
                        // Customer loyalty indicators
                        satisfaction.put("loyalCustomerPercentage", calculateLoyalCustomerPercentage(branchOrders));
                        
                        return satisfaction;
                    }
                ));
    }
    
    // Helper methods
    private double calculateTotalRevenue(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getTotalPriceLkr() != null)
                .collect(Collectors.toMap(
                    RestaurantOrder::getOrderId,
                    RestaurantOrder::getTotalPriceLkr,
                    (existing, replacement) -> existing
                ))
                .values().stream()
                .mapToDouble(BigDecimal::doubleValue)
                .sum();
    }
    
    private double calculateAverageOrderValue(List<RestaurantOrder> orders) {
        Map<String, BigDecimal> uniqueOrders = orders.stream()
                .filter(order -> order.getTotalPriceLkr() != null)
                .collect(Collectors.toMap(
                    RestaurantOrder::getOrderId,
                    RestaurantOrder::getTotalPriceLkr,
                    (existing, replacement) -> existing
                ));
        
        return uniqueOrders.isEmpty() ? 0.0 : 
                uniqueOrders.values().stream()
                        .mapToDouble(BigDecimal::doubleValue)
                        .average()
                        .orElse(0.0);
    }
    
    private double calculateAveragePreparationTime(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getPrepStarted() != null && order.getPrepFinished() != null)
                .mapToLong(order -> java.time.Duration.between(order.getPrepStarted(), order.getPrepFinished()).toMinutes())
                .average()
                .orElse(0.0);
    }
    
    private double calculateOrderCompletionRate(List<RestaurantOrder> orders) {
        long totalOrders = orders.stream()
                .map(RestaurantOrder::getOrderId)
                .distinct()
                .count();
        
        long completedOrders = orders.stream()
                .filter(order -> "Completed".equalsIgnoreCase(order.getStatus()))
                .map(RestaurantOrder::getOrderId)
                .distinct()
                .count();
        
        return totalOrders == 0 ? 0.0 : (double) completedOrders / totalOrders * 100;
    }
    
    private double calculateCustomerRetentionRate(List<RestaurantOrder> orders) {
        // Simplified retention calculation
        Set<String> allCustomers = orders.stream()
                .map(RestaurantOrder::getCustomerId)
                .collect(Collectors.toSet());
        
        Map<String, Long> customerOrderCounts = orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getCustomerId, Collectors.counting()));
        
        long repeatCustomers = customerOrderCounts.values().stream()
                .mapToLong(count -> count > 1 ? 1 : 0)
                .sum();
        
        return allCustomers.isEmpty() ? 0.0 : (double) repeatCustomers / allCustomers.size() * 100;
    }
    
    private double calculateRepeatCustomerRate(List<RestaurantOrder> orders) {
        return calculateCustomerRetentionRate(orders); // Same calculation for this context
    }
    
    private double calculateAverageServiceTime(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getOrderPlaced() != null && order.getServedTime() != null)
                .mapToLong(order -> java.time.Duration.between(order.getOrderPlaced(), order.getServedTime()).toMinutes())
                .average()
                .orElse(0.0);
    }
    
    private Map<String, Object> calculatePeakHourPerformance(List<RestaurantOrder> orders) {
        Map<Integer, Long> hourlyOrders = orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    order -> order.getOrderPlaced().getHour(),
                    Collectors.counting()
                ));
        
        Optional<Map.Entry<Integer, Long>> peakHour = hourlyOrders.entrySet().stream()
                .max(Map.Entry.comparingByValue());
        
        Map<String, Object> peakPerformance = new HashMap<>();
        if (peakHour.isPresent()) {
            peakPerformance.put("peakHour", peakHour.get().getKey());
            peakPerformance.put("peakHourOrders", peakHour.get().getValue());
        }
        
        return peakPerformance;
    }
    
    private double calculateCapacityUtilization(List<RestaurantOrder> orders, Integer capacity) {
        if (capacity == null || capacity == 0) return 0.0;
        
        // Simplified capacity utilization based on peak hour orders
        long maxHourlyOrders = orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    order -> order.getOrderPlaced().getHour(),
                    Collectors.counting()
                ))
                .values().stream()
                .mapToLong(Long::longValue)
                .max()
                .orElse(0L);
        
        return (double) maxHourlyOrders / capacity * 100;
    }
    
    private double calculateOrderSuccessRate(List<RestaurantOrder> orders) {
        return calculateOrderCompletionRate(orders); // Same calculation
    }
    
    private double calculateLoyalCustomerPercentage(List<RestaurantOrder> orders) {
        Set<String> allCustomers = orders.stream()
                .map(RestaurantOrder::getCustomerId)
                .collect(Collectors.toSet());
        
        long loyalCustomers = orders.stream()
                .filter(order -> "Regular".equalsIgnoreCase(order.getLoyaltyGroup()) || 
                               "VIP".equalsIgnoreCase(order.getLoyaltyGroup()))
                .map(RestaurantOrder::getCustomerId)
                .distinct()
                .count();
        
        return allCustomers.isEmpty() ? 0.0 : (double) loyalCustomers / allCustomers.size() * 100;
    }
}