package com.restaurant.analytics.analytics;

import com.restaurant.analytics.model.RestaurantOrder;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class CustomerAnalytics {
    
    public Map<String, Object> generateCustomerDemographicsAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> analysis = new HashMap<>();
        
        analysis.put("ageDistribution", generateAgeDistribution(orders));
        analysis.put("genderDistribution", generateGenderDistribution(orders));
        analysis.put("loyaltyGroupAnalysis", generateLoyaltyGroupAnalysis(orders));
        analysis.put("customerSegmentation", generateCustomerSegmentation(orders));
        analysis.put("spendingPatterns", generateSpendingPatterns(orders));
        
        return analysis;
    }
    
    public Map<String, Object> generateSeasonalBehaviorAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> analysis = new HashMap<>();
        
        analysis.put("seasonalRetention", generateSeasonalRetention(orders));
        analysis.put("loyaltyIndex", generateLoyaltyIndex(orders));
        analysis.put("seasonalSpending", generateSeasonalSpending(orders));
        analysis.put("customerLifecycle", generateCustomerLifecycle(orders));
        
        return analysis;
    }
    
    private Map<String, Long> generateAgeDistribution(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getAge() != null)
                .collect(Collectors.groupingBy(
                    order -> getAgeGroup(order.getAge()),
                    Collectors.counting()
                ));
    }
    
    private Map<String, Long> generateGenderDistribution(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getGender() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getGender,
                    Collectors.counting()
                ));
    }
    
    private Map<String, Object> generateLoyaltyGroupAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> loyaltyAnalysis = new HashMap<>();
        
        // Distribution by loyalty group
        Map<String, Long> loyaltyDistribution = orders.stream()
                .filter(order -> order.getLoyaltyGroup() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getLoyaltyGroup,
                    Collectors.counting()
                ));
        
        // Average spending by loyalty group
        Map<String, Double> loyaltySpending = orders.stream()
                .filter(order -> order.getLoyaltyGroup() != null && order.getTotalPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getLoyaltyGroup,
                    Collectors.averagingDouble(order -> order.getTotalPriceLkr().doubleValue())
                ));
        
        loyaltyAnalysis.put("distribution", loyaltyDistribution);
        loyaltyAnalysis.put("averageSpending", loyaltySpending);
        
        return loyaltyAnalysis;
    }
    
    private Map<String, Object> generateCustomerSegmentation(List<RestaurantOrder> orders) {
        Map<String, List<RestaurantOrder>> customerOrders = orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getCustomerId));
        
        Map<String, Object> segmentation = new HashMap<>();
        
        // RFM Analysis (Recency, Frequency, Monetary)
        List<Map<String, Object>> rfmAnalysis = customerOrders.entrySet().stream()
                .map(entry -> {
                    String customerId = entry.getKey();
                    List<RestaurantOrder> customerOrderList = entry.getValue();
                    
                    Map<String, Object> rfm = new HashMap<>();
                    rfm.put("customerId", customerId);
                    
                    // Recency (days since last order)
                    LocalDateTime lastOrder = customerOrderList.stream()
                            .map(RestaurantOrder::getOrderPlaced)
                            .filter(Objects::nonNull)
                            .max(LocalDateTime::compareTo)
                            .orElse(null);
                    
                    if (lastOrder != null) {
                        long recency = ChronoUnit.DAYS.between(lastOrder, LocalDateTime.now());
                        rfm.put("recency", recency);
                    }
                    
                    // Frequency (number of orders)
                    rfm.put("frequency", customerOrderList.size());
                    
                    // Monetary (total spending)
                    double totalSpending = customerOrderList.stream()
                            .mapToDouble(order -> order.getTotalPriceLkr().doubleValue())
                            .sum();
                    rfm.put("monetary", totalSpending);
                    
                    // Customer segment
                    rfm.put("segment", determineCustomerSegment(customerOrderList));
                    
                    return rfm;
                })
                .collect(Collectors.toList());
        
        segmentation.put("rfmAnalysis", rfmAnalysis);
        
        // Segment distribution
        Map<String, Long> segmentDistribution = rfmAnalysis.stream()
                .collect(Collectors.groupingBy(
                    rfm -> (String) rfm.get("segment"),
                    Collectors.counting()
                ));
        
        segmentation.put("segmentDistribution", segmentDistribution);
        
        return segmentation;
    }
    
    private Map<String, Object> generateSpendingPatterns(List<RestaurantOrder> orders) {
        Map<String, Object> patterns = new HashMap<>();
        
        // Spending by age group
        Map<String, Double> spendingByAge = orders.stream()
                .filter(order -> order.getAge() != null && order.getTotalPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    order -> getAgeGroup(order.getAge()),
                    Collectors.averagingDouble(order -> order.getTotalPriceLkr().doubleValue())
                ));
        
        // Spending by gender
        Map<String, Double> spendingByGender = orders.stream()
                .filter(order -> order.getGender() != null && order.getTotalPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getGender,
                    Collectors.averagingDouble(order -> order.getTotalPriceLkr().doubleValue())
                ));
        
        patterns.put("spendingByAge", spendingByAge);
        patterns.put("spendingByGender", spendingByGender);
        
        return patterns;
    }
    
    private Map<String, Object> generateSeasonalRetention(List<RestaurantOrder> orders) {
        Map<String, Object> retention = new HashMap<>();
        
        // Group orders by season and customer
        Map<String, Set<String>> seasonalCustomers = orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(
                    order -> getSeason(order.getOrderPlaced()),
                    Collectors.mapping(RestaurantOrder::getCustomerId, Collectors.toSet())
                ));
        
        retention.put("seasonalCustomers", seasonalCustomers);
        
        // Calculate retention rates between seasons
        Map<String, Double> retentionRates = new HashMap<>();
        List<String> seasons = Arrays.asList("Spring", "Summer", "Autumn", "Winter");
        
        for (int i = 0; i < seasons.size() - 1; i++) {
            String currentSeason = seasons.get(i);
            String nextSeason = seasons.get(i + 1);
            
            Set<String> currentCustomers = seasonalCustomers.getOrDefault(currentSeason, new HashSet<>());
            Set<String> nextCustomers = seasonalCustomers.getOrDefault(nextSeason, new HashSet<>());
            
            if (!currentCustomers.isEmpty()) {
                long retainedCustomers = currentCustomers.stream()
                        .mapToLong(customer -> nextCustomers.contains(customer) ? 1 : 0)
                        .sum();
                
                double retentionRate = (double) retainedCustomers / currentCustomers.size() * 100;
                retentionRates.put(currentSeason + " to " + nextSeason, retentionRate);
            }
        }
        
        retention.put("retentionRates", retentionRates);
        
        return retention;
    }
    
    private Map<String, Object> generateLoyaltyIndex(List<RestaurantOrder> orders) {
        Map<String, List<RestaurantOrder>> customerOrders = orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getCustomerId));
        
        Map<String, Object> loyaltyIndex = new HashMap<>();
        
        List<Map<String, Object>> customerLoyalty = customerOrders.entrySet().stream()
                .map(entry -> {
                    String customerId = entry.getKey();
                    List<RestaurantOrder> customerOrderList = entry.getValue();
                    
                    Map<String, Object> loyalty = new HashMap<>();
                    loyalty.put("customerId", customerId);
                    loyalty.put("orderCount", customerOrderList.size());
                    
                    // Calculate loyalty score based on frequency and consistency
                    double loyaltyScore = calculateLoyaltyScore(customerOrderList);
                    loyalty.put("loyaltyScore", loyaltyScore);
                    loyalty.put("loyaltyTier", getLoyaltyTier(loyaltyScore));
                    
                    return loyalty;
                })
                .collect(Collectors.toList());
        
        loyaltyIndex.put("customerLoyalty", customerLoyalty);
        
        // Loyalty tier distribution
        Map<String, Long> tierDistribution = customerLoyalty.stream()
                .collect(Collectors.groupingBy(
                    loyalty -> (String) loyalty.get("loyaltyTier"),
                    Collectors.counting()
                ));
        
        loyaltyIndex.put("tierDistribution", tierDistribution);
        
        return loyaltyIndex;
    }
    
    private Map<String, Double> generateSeasonalSpending(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getOrderPlaced() != null && order.getTotalPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    order -> getSeason(order.getOrderPlaced()),
                    Collectors.averagingDouble(order -> order.getTotalPriceLkr().doubleValue())
                ));
    }
    
    private Map<String, Object> generateCustomerLifecycle(List<RestaurantOrder> orders) {
        Map<String, List<RestaurantOrder>> customerOrders = orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getCustomerId));
        
        Map<String, Object> lifecycle = new HashMap<>();
        
        List<Map<String, Object>> customerLifecycles = customerOrders.entrySet().stream()
                .map(entry -> {
                    List<RestaurantOrder> customerOrderList = entry.getValue();
                    
                    Map<String, Object> customerLifecycle = new HashMap<>();
                    customerLifecycle.put("customerId", entry.getKey());
                    
                    // First and last order dates
                    LocalDateTime firstOrder = customerOrderList.stream()
                            .map(RestaurantOrder::getOrderPlaced)
                            .filter(Objects::nonNull)
                            .min(LocalDateTime::compareTo)
                            .orElse(null);
                    
                    LocalDateTime lastOrder = customerOrderList.stream()
                            .map(RestaurantOrder::getOrderPlaced)
                            .filter(Objects::nonNull)
                            .max(LocalDateTime::compareTo)
                            .orElse(null);
                    
                    if (firstOrder != null && lastOrder != null) {
                        long customerLifespanDays = ChronoUnit.DAYS.between(firstOrder, lastOrder);
                        customerLifecycle.put("lifespanDays", customerLifespanDays);
                        customerLifecycle.put("firstOrderDate", firstOrder);
                        customerLifecycle.put("lastOrderDate", lastOrder);
                    }
                    
                    return customerLifecycle;
                })
                .collect(Collectors.toList());
        
        lifecycle.put("customerLifecycles", customerLifecycles);
        
        return lifecycle;
    }
    
    private String getAgeGroup(Integer age) {
        if (age < 25) return "18-24";
        else if (age < 35) return "25-34";
        else if (age < 45) return "35-44";
        else if (age < 55) return "45-54";
        else if (age < 65) return "55-64";
        else return "65+";
    }
    
    private String getSeason(LocalDateTime dateTime) {
        int month = dateTime.getMonthValue();
        if (month >= 3 && month <= 5) return "Spring";
        else if (month >= 6 && month <= 8) return "Summer";
        else if (month >= 9 && month <= 11) return "Autumn";
        else return "Winter";
    }
    
    private String determineCustomerSegment(List<RestaurantOrder> customerOrders) {
        int frequency = customerOrders.size();
        double totalSpending = customerOrders.stream()
                .mapToDouble(order -> order.getTotalPriceLkr().doubleValue())
                .sum();
        
        if (frequency >= 10 && totalSpending >= 10000) return "VIP";
        else if (frequency >= 5 && totalSpending >= 5000) return "Loyal";
        else if (frequency >= 3) return "Regular";
        else return "Occasional";
    }
    
    private double calculateLoyaltyScore(List<RestaurantOrder> customerOrders) {
        // Simple loyalty score based on frequency and recency
        int frequency = customerOrders.size();
        
        LocalDateTime lastOrder = customerOrders.stream()
                .map(RestaurantOrder::getOrderPlaced)
                .filter(Objects::nonNull)
                .max(LocalDateTime::compareTo)
                .orElse(null);
        
        if (lastOrder == null) return 0.0;
        
        long daysSinceLastOrder = ChronoUnit.DAYS.between(lastOrder, LocalDateTime.now());
        double recencyScore = Math.max(0, 100 - daysSinceLastOrder);
        double frequencyScore = Math.min(100, frequency * 10);
        
        return (recencyScore + frequencyScore) / 2;
    }
    
    private String getLoyaltyTier(double loyaltyScore) {
        if (loyaltyScore >= 80) return "Platinum";
        else if (loyaltyScore >= 60) return "Gold";
        else if (loyaltyScore >= 40) return "Silver";
        else return "Bronze";
    }
}