package com.restaurant.analytics.transform;

import com.restaurant.analytics.model.RestaurantOrder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class DataTransformationService {
    
    public List<RestaurantOrder> cleanAndValidateData(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(this::isValidOrder)
                .map(this::cleanOrder)
                .collect(Collectors.toList());
    }
    
    public Map<String, List<RestaurantOrder>> groupByOutlet(List<RestaurantOrder> orders) {
        return orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOutletId));
    }
    
    public Map<String, List<RestaurantOrder>> groupByCustomer(List<RestaurantOrder> orders) {
        return orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getCustomerId));
    }
    
    public Map<String, List<RestaurantOrder>> groupByTimeWindow(List<RestaurantOrder> orders, String timeWindow) {
        DateTimeFormatter formatter;
        
        switch (timeWindow.toLowerCase()) {
            case "hour":
                formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH");
                break;
            case "day":
                formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
                break;
            case "month":
                formatter = DateTimeFormatter.ofPattern("yyyy-MM");
                break;
            case "year":
                formatter = DateTimeFormatter.ofPattern("yyyy");
                break;
            default:
                formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        }
        
        return orders.stream()
                .filter(order -> order.getOrderPlaced() != null)
                .collect(Collectors.groupingBy(order -> 
                    order.getOrderPlaced().format(formatter)));
    }
    
    public List<RestaurantOrder> filterBySeason(List<RestaurantOrder> orders, String season) {
        return orders.stream()
                .filter(order -> isInSeason(order.getOrderPlaced(), season))
                .collect(Collectors.toList());
    }
    
    public List<RestaurantOrder> filterByFestival(List<RestaurantOrder> orders, String festival) {
        // Define festival periods (can be extended)
        return orders.stream()
                .filter(order -> isInFestivalPeriod(order.getOrderPlaced(), festival))
                .collect(Collectors.toList());
    }
    
    private boolean isValidOrder(RestaurantOrder order) {
        return order.getOrderId() != null && 
               order.getCustomerId() != null && 
               order.getOutletId() != null &&
               order.getOrderPlaced() != null &&
               order.getTotalPriceLkr() != null &&
               order.getTotalPriceLkr().compareTo(java.math.BigDecimal.ZERO) > 0;
    }
    
    private RestaurantOrder cleanOrder(RestaurantOrder order) {
        // Clean and normalize data
        if (order.getCustomerName() != null) {
            order.setCustomerName(order.getCustomerName().trim());
        }
        
        if (order.getOutletName() != null) {
            order.setOutletName(order.getOutletName().trim());
        }
        
        if (order.getCategory() != null) {
            order.setCategory(order.getCategory().trim());
        }
        
        if (order.getGender() != null) {
            order.setGender(normalizeGender(order.getGender()));
        }
        
        if (order.getLoyaltyGroup() != null) {
            order.setLoyaltyGroup(order.getLoyaltyGroup().trim());
        }
        
        return order;
    }
    
    private String normalizeGender(String gender) {
        if (gender == null) return null;
        
        String normalized = gender.trim().toLowerCase();
        switch (normalized) {
            case "m":
            case "male":
                return "Male";
            case "f":
            case "female":
                return "Female";
            case "other":
            case "o":
                return "Other";
            default:
                return "Other";
        }
    }
    
    private boolean isInSeason(LocalDateTime dateTime, String season) {
        if (dateTime == null) return false;
        
        int month = dateTime.getMonthValue();
        
        switch (season.toLowerCase()) {
            case "spring":
                return month >= 3 && month <= 5;
            case "summer":
                return month >= 6 && month <= 8;
            case "autumn":
            case "fall":
                return month >= 9 && month <= 11;
            case "winter":
                return month == 12 || month <= 2;
            default:
                return true; // Return all if season not recognized
        }
    }
    
    private boolean isInFestivalPeriod(LocalDateTime dateTime, String festival) {
        if (dateTime == null) return false;
        
        int month = dateTime.getMonthValue();
        int day = dateTime.getDayOfMonth();
        
        switch (festival.toLowerCase()) {
            case "christmas":
                return month == 12 && day >= 20 && day <= 31;
            case "new_year":
                return (month == 12 && day >= 25) || (month == 1 && day <= 7);
            case "valentine":
                return month == 2 && day >= 10 && day <= 20;
            case "easter":
                // Simplified Easter period (March-April)
                return (month == 3 && day >= 15) || (month == 4 && day <= 15);
            case "diwali":
                // Typically October-November
                return month == 10 || month == 11;
            case "vesak":
                // Typically May
                return month == 5;
            default:
                return true; // Return all if festival not recognized
        }
    }
}