package com.restaurant.analytics.analytics;

import com.restaurant.analytics.model.RestaurantOrder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class PeakDiningAnalytics {
    
    public Map<String, Object> generatePeakDiningAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> analysis = new HashMap<>();
        
        analysis.put("hourlyHeatmap", generateHourlyHeatmap(orders));
        analysis.put("peakHourTables", generatePeakHourTables(orders));
        analysis.put("branchSummaries", generateBranchSummaries(orders));
        analysis.put("dailyPatterns", generateDailyPatterns(orders));
        analysis.put("weeklyPatterns", generateWeeklyPatterns(orders));
        
        return analysis;
    }
    
    private Map<String, Map<Integer, Long>> generateHourlyHeatmap(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getOutletId,
                    Collectors.groupingBy(
                        order -> order.getOrderPlaced().getHour(),
                        Collectors.counting()
                    )
                ));
    }
    
    private Map<String, Object> generatePeakHourTables(List<RestaurantOrder> orders) {
        Map<String, Object> peakHours = new HashMap<>();
        
        // Overall peak hours
        Map<Integer, Long> hourlyOrders = orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    order -> order.getOrderPlaced().getHour(),
                    Collectors.counting()
                ));
        
        List<Map<String, Object>> peakHoursList = hourlyOrders.entrySet().stream()
                .sorted(Map.Entry.<Integer, Long>comparingByValue().reversed())
                .limit(5)
                .map(entry -> {
                    Map<String, Object> hourData = new HashMap<>();
                    hourData.put("hour", entry.getKey());
                    hourData.put("orderCount", entry.getValue());
                    hourData.put("timeRange", String.format("%02d:00 - %02d:59", entry.getKey(), entry.getKey()));
                    return hourData;
                })
                .collect(Collectors.toList());
        
        peakHours.put("overallPeakHours", peakHoursList);
        
        // Peak hours by outlet
        Map<String, List<Map<String, Object>>> outletPeakHours = orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> entry.getValue().stream()
                            .collect(Collectors.groupingBy(
                                order -> order.getOrderPlaced().getHour(),
                                Collectors.counting()
                            ))
                            .entrySet().stream()
                            .sorted(Map.Entry.<Integer, Long>comparingByValue().reversed())
                            .limit(3)
                            .map(hourEntry -> {
                                Map<String, Object> hourData = new HashMap<>();
                                hourData.put("hour", hourEntry.getKey());
                                hourData.put("orderCount", hourEntry.getValue());
                                return hourData;
                            })
                            .collect(Collectors.toList())
                ));
        
        peakHours.put("outletPeakHours", outletPeakHours);
        
        return peakHours;
    }
    
    private Map<String, Map<String, Object>> generateBranchSummaries(List<RestaurantOrder> orders) {
        return orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> {
                        List<RestaurantOrder> branchOrders = entry.getValue();
                        Map<String, Object> summary = new HashMap<>();
                        
                        summary.put("totalOrders", branchOrders.size());
                        summary.put("totalRevenue", branchOrders.stream()
                                .mapToDouble(order -> order.getTotalPriceLkr().doubleValue())
                                .sum());
                        summary.put("averageOrderValue", branchOrders.stream()
                                .mapToDouble(order -> order.getTotalPriceLkr().doubleValue())
                                .average().orElse(0.0));
                        summary.put("uniqueCustomers", branchOrders.stream()
                                .map(RestaurantOrder::getCustomerId)
                                .distinct().count());
                        summary.put("outletName", branchOrders.get(0).getOutletName());
                        summary.put("borough", branchOrders.get(0).getBorough());
                        
                        // Peak hour for this branch
                        Map<Integer, Long> branchHourlyOrders = branchOrders.stream()
                                .filter(order -> order.getOrderPlaced() != null)
                                .collect(Collectors.groupingBy(
                                    order -> order.getOrderPlaced().getHour(),
                                    Collectors.counting()
                                ));
                        
                        Optional<Map.Entry<Integer, Long>> peakHour = branchHourlyOrders.entrySet().stream()
                                .max(Map.Entry.comparingByValue());
                        
                        if (peakHour.isPresent()) {
                            summary.put("peakHour", peakHour.get().getKey());
                            summary.put("peakHourOrders", peakHour.get().getValue());
                        }
                        
                        return summary;
                    }
                ));
    }
    
    private Map<String, Long> generateDailyPatterns(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    order -> order.getOrderPlaced().getDayOfWeek().toString(),
                    Collectors.counting()
                ));
    }
    
    private Map<String, Map<String, Long>> generateWeeklyPatterns(List<RestaurantOrder> orders) {
        DateTimeFormatter weekFormatter = DateTimeFormatter.ofPattern("yyyy-'W'ww");
        
        return orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getOutletId,
                    Collectors.groupingBy(
                        order -> order.getOrderPlaced().format(weekFormatter),
                        Collectors.counting()
                    )
                ));
    }
}