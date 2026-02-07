package com.restaurant.analytics.analytics;

import com.restaurant.analytics.model.RestaurantOrder;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class RevenueAnalytics {
    
    public Map<String, Object> generateRevenueAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> analysis = new HashMap<>();
        
        analysis.put("ticketCounting", generateTicketCounting(orders));
        analysis.put("revenueSummary", generateRevenueSummary(orders));
        analysis.put("dailyRevenue", generateDailyRevenue(orders));
        analysis.put("monthlyRevenue", generateMonthlyRevenue(orders));
        analysis.put("outletRevenue", generateOutletRevenue(orders));
        analysis.put("paymentMethodAnalysis", generatePaymentMethodAnalysis(orders));
        analysis.put("averageOrderValue", generateAverageOrderValue(orders));
        
        return analysis;
    }
    
    private Map<String, Object> generateTicketCounting(List<RestaurantOrder> orders) {
        Map<String, Object> ticketData = new HashMap<>();
        
        // Total unique orders
        long totalOrders = orders.stream()
                .map(RestaurantOrder::getOrderId)
                .distinct()
                .count();
        
        // Orders by status
        Map<String, Long> ordersByStatus = orders.stream()
                .filter(order -> order.getStatus() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getStatus,
                    Collectors.mapping(RestaurantOrder::getOrderId, Collectors.toSet())
                ))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> (long) entry.getValue().size()
                ));
        
        // Average items per order
        Map<String, Integer> orderItemCounts = orders.stream()
                .filter(order -> order.getNumItems() != null)
                .collect(Collectors.toMap(
                    RestaurantOrder::getOrderId,
                    RestaurantOrder::getNumItems,
                    (existing, replacement) -> existing
                ));
        
        double avgItemsPerOrder = orderItemCounts.values().stream()
                .mapToInt(Integer::intValue)
                .average()
                .orElse(0.0);
        
        ticketData.put("totalOrders", totalOrders);
        ticketData.put("ordersByStatus", ordersByStatus);
        ticketData.put("averageItemsPerOrder", avgItemsPerOrder);
        ticketData.put("totalItems", orders.size());
        
        return ticketData;
    }
    
    private Map<String, Object> generateRevenueSummary(List<RestaurantOrder> orders) {
        Map<String, Object> summary = new HashMap<>();
        
        // Total revenue
        double totalRevenue = orders.stream()
                .filter(order -> order.getTotalPriceLkr() != null)
                .mapToDouble(order -> order.getTotalPriceLkr().doubleValue())
                .sum();
        
        // Unique orders for accurate calculations
        Map<String, RestaurantOrder> uniqueOrders = orders.stream()
                .filter(order -> order.getTotalPriceLkr() != null)
                .collect(Collectors.toMap(
                    RestaurantOrder::getOrderId,
                    order -> order,
                    (existing, replacement) -> existing
                ));
        
        double reconciledRevenue = uniqueOrders.values().stream()
                .mapToDouble(order -> order.getTotalPriceLkr().doubleValue())
                .sum();
        
        // Average order value
        double avgOrderValue = uniqueOrders.isEmpty() ? 0.0 : 
                reconciledRevenue / uniqueOrders.size();
        
        // Revenue growth (if we have time-series data)
        Map<String, Double> monthlyRevenue = generateMonthlyRevenue(orders);
        List<String> sortedMonths = monthlyRevenue.keySet().stream()
                .sorted()
                .collect(Collectors.toList());
        
        Double growthRate = null;
        if (sortedMonths.size() >= 2) {
            String firstMonth = sortedMonths.get(0);
            String lastMonth = sortedMonths.get(sortedMonths.size() - 1);
            double firstMonthRevenue = monthlyRevenue.get(firstMonth);
            double lastMonthRevenue = monthlyRevenue.get(lastMonth);
            
            if (firstMonthRevenue > 0) {
                growthRate = ((lastMonthRevenue - firstMonthRevenue) / firstMonthRevenue) * 100;
            }
        }
        
        summary.put("totalRevenue", totalRevenue);
        summary.put("reconciledRevenue", reconciledRevenue);
        summary.put("averageOrderValue", avgOrderValue);
        summary.put("totalOrders", uniqueOrders.size());
        summary.put("revenueGrowthRate", growthRate);
        
        return summary;
    }
    
    private Map<String, Double> generateDailyRevenue(List<RestaurantOrder> orders) {
        DateTimeFormatter dayFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        
        Map<String, Set<String>> dailyOrders = orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    order -> order.getOrderPlaced().format(dayFormatter),
                    Collectors.mapping(RestaurantOrder::getOrderId, Collectors.toSet())
                ));
        
        Map<String, Double> dailyRevenue = new HashMap<>();
        
        for (Map.Entry<String, Set<String>> entry : dailyOrders.entrySet()) {
            String day = entry.getKey();
            Set<String> orderIds = entry.getValue();
            
            double dayRevenue = orders.stream()
                    .filter(order -> orderIds.contains(order.getOrderId()) && 
                                   order.getTotalPriceLkr() != null)
                    .collect(Collectors.toMap(
                        RestaurantOrder::getOrderId,
                        RestaurantOrder::getTotalPriceLkr,
                        (existing, replacement) -> existing
                    ))
                    .values().stream()
                    .mapToDouble(BigDecimal::doubleValue)
                    .sum();
            
            dailyRevenue.put(day, dayRevenue);
        }
        
        return dailyRevenue;
    }
    
    private Map<String, Double> generateMonthlyRevenue(List<RestaurantOrder> orders) {
        DateTimeFormatter monthFormatter = DateTimeFormatter.ofPattern("yyyy-MM");
        
        Map<String, Set<String>> monthlyOrders = orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    order -> order.getOrderPlaced().format(monthFormatter),
                    Collectors.mapping(RestaurantOrder::getOrderId, Collectors.toSet())
                ));
        
        Map<String, Double> monthlyRevenue = new HashMap<>();
        
        for (Map.Entry<String, Set<String>> entry : monthlyOrders.entrySet()) {
            String month = entry.getKey();
            Set<String> orderIds = entry.getValue();
            
            double monthRevenue = orders.stream()
                    .filter(order -> orderIds.contains(order.getOrderId()) && 
                                   order.getTotalPriceLkr() != null)
                    .collect(Collectors.toMap(
                        RestaurantOrder::getOrderId,
                        RestaurantOrder::getTotalPriceLkr,
                        (existing, replacement) -> existing
                    ))
                    .values().stream()
                    .mapToDouble(BigDecimal::doubleValue)
                    .sum();
            
            monthlyRevenue.put(month, monthRevenue);
        }
        
        return monthlyRevenue;
    }
    
    private Map<String, Object> generateOutletRevenue(List<RestaurantOrder> orders) {
        Map<String, Set<String>> outletOrders = orders.stream()
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getOutletId,
                    Collectors.mapping(RestaurantOrder::getOrderId, Collectors.toSet())
                ));
        
        return outletOrders.entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> {
                        String outletId = entry.getKey();
                        Set<String> orderIds = entry.getValue();
                        
                        List<RestaurantOrder> outletOrderList = orders.stream()
                                .filter(order -> outletId.equals(order.getOutletId()))
                                .collect(Collectors.toList());
                        
                        Map<String, Object> outletData = new HashMap<>();
                        
                        // Revenue calculation
                        double revenue = orders.stream()
                                .filter(order -> orderIds.contains(order.getOrderId()) && 
                                               order.getTotalPriceLkr() != null)
                                .collect(Collectors.toMap(
                                    RestaurantOrder::getOrderId,
                                    RestaurantOrder::getTotalPriceLkr,
                                    (existing, replacement) -> existing
                                ))
                                .values().stream()
                                .mapToDouble(BigDecimal::doubleValue)
                                .sum();
                        
                        outletData.put("revenue", revenue);
                        outletData.put("orderCount", orderIds.size());
                        outletData.put("averageOrderValue", orderIds.isEmpty() ? 0.0 : revenue / orderIds.size());
                        
                        // Outlet details
                        if (!outletOrderList.isEmpty()) {
                            RestaurantOrder sampleOrder = outletOrderList.get(0);
                            outletData.put("outletName", sampleOrder.getOutletName());
                            outletData.put("borough", sampleOrder.getBorough());
                            outletData.put("capacity", sampleOrder.getCapacity());
                        }
                        
                        return outletData;
                    }
                ));
    }
    
    private Map<String, Object> generatePaymentMethodAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> paymentAnalysis = new HashMap<>();
        
        // Orders by payment method
        Map<String, Long> paymentMethodOrders = orders.stream()
                .filter(order -> order.getPaymentMethod() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getPaymentMethod,
                    Collectors.mapping(RestaurantOrder::getOrderId, Collectors.toSet())
                ))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> (long) entry.getValue().size()
                ));
        
        // Revenue by payment method
        Map<String, Double> paymentMethodRevenue = new HashMap<>();
        
        for (String paymentMethod : paymentMethodOrders.keySet()) {
            double revenue = orders.stream()
                    .filter(order -> paymentMethod.equals(order.getPaymentMethod()) && 
                                   order.getTotalPriceLkr() != null)
                    .collect(Collectors.toMap(
                        RestaurantOrder::getOrderId,
                        RestaurantOrder::getTotalPriceLkr,
                        (existing, replacement) -> existing
                    ))
                    .values().stream()
                    .mapToDouble(BigDecimal::doubleValue)
                    .sum();
            
            paymentMethodRevenue.put(paymentMethod, revenue);
        }
        
        paymentAnalysis.put("ordersByPaymentMethod", paymentMethodOrders);
        paymentAnalysis.put("revenueByPaymentMethod", paymentMethodRevenue);
        
        return paymentAnalysis;
    }
    
    private Map<String, Object> generateAverageOrderValue(List<RestaurantOrder> orders) {
        Map<String, Object> aovAnalysis = new HashMap<>();
        
        // Overall AOV
        Map<String, BigDecimal> uniqueOrderValues = orders.stream()
                .filter(order -> order.getTotalPriceLkr() != null)
                .collect(Collectors.toMap(
                    RestaurantOrder::getOrderId,
                    RestaurantOrder::getTotalPriceLkr,
                    (existing, replacement) -> existing
                ));
        
        double overallAOV = uniqueOrderValues.values().stream()
                .mapToDouble(BigDecimal::doubleValue)
                .average()
                .orElse(0.0);
        
        // AOV by outlet
        Map<String, Double> aovByOutlet = orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> entry.getValue().stream()
                            .filter(order -> order.getTotalPriceLkr() != null)
                            .collect(Collectors.toMap(
                                RestaurantOrder::getOrderId,
                                RestaurantOrder::getTotalPriceLkr,
                                (existing, replacement) -> existing
                            ))
                            .values().stream()
                            .mapToDouble(BigDecimal::doubleValue)
                            .average()
                            .orElse(0.0)
                ));
        
        // AOV by customer segment
        Map<String, Double> aovByLoyalty = orders.stream()
                .filter(order -> order.getLoyaltyGroup() != null && order.getTotalPriceLkr() != null)
                .collect(Collectors.groupingBy(RestaurantOrder::getLoyaltyGroup))
                .entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> entry.getValue().stream()
                            .collect(Collectors.toMap(
                                RestaurantOrder::getOrderId,
                                RestaurantOrder::getTotalPriceLkr,
                                (existing, replacement) -> existing
                            ))
                            .values().stream()
                            .mapToDouble(BigDecimal::doubleValue)
                            .average()
                            .orElse(0.0)
                ));
        
        aovAnalysis.put("overallAOV", overallAOV);
        aovAnalysis.put("aovByOutlet", aovByOutlet);
        aovAnalysis.put("aovByLoyaltyGroup", aovByLoyalty);
        
        return aovAnalysis;
    }
}