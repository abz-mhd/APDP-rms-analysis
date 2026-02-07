package com.restaurant.analytics.analytics;

import com.restaurant.analytics.model.RestaurantOrder;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class MenuAnalytics {
    
    public Map<String, Object> generateMenuAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> analysis = new HashMap<>();
        
        analysis.put("popularItems", generatePopularItems(orders));
        analysis.put("categoryAnalysis", generateCategoryAnalysis(orders));
        analysis.put("itemCombos", generateItemCombos(orders));
        analysis.put("sankeyDiagramData", generateSankeyDiagramData(orders));
        analysis.put("spiceLevelPreferences", generateSpiceLevelPreferences(orders));
        analysis.put("vegetarianAnalysis", generateVegetarianAnalysis(orders));
        
        return analysis;
    }
    
    private List<Map<String, Object>> generatePopularItems(List<RestaurantOrder> orders) {
        Map<String, Long> itemCounts = orders.stream()
                .filter(order -> order.getMenuItemName() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getMenuItemName,
                    Collectors.counting()
                ));
        
        Map<String, Double> itemRevenue = orders.stream()
                .filter(order -> order.getMenuItemName() != null && order.getItemPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getMenuItemName,
                    Collectors.summingDouble(order -> order.getItemPriceLkr().doubleValue())
                ));
        
        return itemCounts.entrySet().stream()
                .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
                .limit(20)
                .map(entry -> {
                    Map<String, Object> item = new HashMap<>();
                    item.put("itemName", entry.getKey());
                    item.put("orderCount", entry.getValue());
                    item.put("totalRevenue", itemRevenue.getOrDefault(entry.getKey(), 0.0));
                    
                    // Get additional item details
                    Optional<RestaurantOrder> sampleOrder = orders.stream()
                            .filter(order -> entry.getKey().equals(order.getMenuItemName()))
                            .findFirst();
                    
                    if (sampleOrder.isPresent()) {
                        RestaurantOrder order = sampleOrder.get();
                        item.put("category", order.getCategory());
                        item.put("price", order.getItemPriceLkr());
                        item.put("isVegetarian", order.getIsVegetarian());
                        item.put("spiceLevel", order.getSpiceLevel());
                    }
                    
                    return item;
                })
                .collect(Collectors.toList());
    }
    
    private Map<String, Object> generateCategoryAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> categoryAnalysis = new HashMap<>();
        
        // Orders by category
        Map<String, Long> categoryOrders = orders.stream()
                .filter(order -> order.getCategory() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getCategory,
                    Collectors.counting()
                ));
        
        // Revenue by category
        Map<String, Double> categoryRevenue = orders.stream()
                .filter(order -> order.getCategory() != null && order.getItemPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getCategory,
                    Collectors.summingDouble(order -> order.getItemPriceLkr().doubleValue())
                ));
        
        // Average price by category
        Map<String, Double> categoryAvgPrice = orders.stream()
                .filter(order -> order.getCategory() != null && order.getItemPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getCategory,
                    Collectors.averagingDouble(order -> order.getItemPriceLkr().doubleValue())
                ));
        
        categoryAnalysis.put("ordersByCategory", categoryOrders);
        categoryAnalysis.put("revenueByCategory", categoryRevenue);
        categoryAnalysis.put("averagePriceByCategory", categoryAvgPrice);
        
        return categoryAnalysis;
    }
    
    private List<Map<String, Object>> generateItemCombos(List<RestaurantOrder> orders) {
        // Group orders by order ID to find items ordered together
        Map<String, List<RestaurantOrder>> orderGroups = orders.stream()
                .collect(Collectors.groupingBy(RestaurantOrder::getOrderId));
        
        Map<Set<String>, Long> comboCounts = new HashMap<>();
        
        for (List<RestaurantOrder> orderItems : orderGroups.values()) {
            if (orderItems.size() > 1) {
                Set<String> itemNames = orderItems.stream()
                        .map(RestaurantOrder::getMenuItemName)
                        .filter(Objects::nonNull)
                        .collect(Collectors.toSet());
                
                if (itemNames.size() > 1) {
                    comboCounts.merge(itemNames, 1L, Long::sum);
                }
            }
        }
        
        return comboCounts.entrySet().stream()
                .sorted(Map.Entry.<Set<String>, Long>comparingByValue().reversed())
                .limit(10)
                .map(entry -> {
                    Map<String, Object> combo = new HashMap<>();
                    combo.put("items", new ArrayList<>(entry.getKey()));
                    combo.put("frequency", entry.getValue());
                    combo.put("comboSize", entry.getKey().size());
                    return combo;
                })
                .collect(Collectors.toList());
    }
    
    private Map<String, Object> generateSankeyDiagramData(List<RestaurantOrder> orders) {
        Map<String, Object> sankeyData = new HashMap<>();
        
        // Create flow from category to specific items
        List<Map<String, Object>> flows = new ArrayList<>();
        Set<String> nodes = new HashSet<>();
        
        Map<String, Map<String, Long>> categoryToItemFlow = orders.stream()
                .filter(order -> order.getCategory() != null && order.getMenuItemName() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getCategory,
                    Collectors.groupingBy(
                        RestaurantOrder::getMenuItemName,
                        Collectors.counting()
                    )
                ));
        
        for (Map.Entry<String, Map<String, Long>> categoryEntry : categoryToItemFlow.entrySet()) {
            String category = categoryEntry.getKey();
            nodes.add(category);
            
            for (Map.Entry<String, Long> itemEntry : categoryEntry.getValue().entrySet()) {
                String item = itemEntry.getKey();
                Long count = itemEntry.getValue();
                
                nodes.add(item);
                
                Map<String, Object> flow = new HashMap<>();
                flow.put("source", category);
                flow.put("target", item);
                flow.put("value", count);
                flows.add(flow);
            }
        }
        
        sankeyData.put("nodes", nodes.stream().map(node -> {
            Map<String, Object> nodeData = new HashMap<>();
            nodeData.put("name", node);
            return nodeData;
        }).collect(Collectors.toList()));
        
        sankeyData.put("flows", flows);
        
        return sankeyData;
    }
    
    private Map<String, Long> generateSpiceLevelPreferences(List<RestaurantOrder> orders) {
        return orders.stream()
                .filter(order -> order.getSpiceLevel() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getSpiceLevel,
                    Collectors.counting()
                ));
    }
    
    private Map<String, Object> generateVegetarianAnalysis(List<RestaurantOrder> orders) {
        Map<String, Object> vegAnalysis = new HashMap<>();
        
        // Vegetarian vs Non-vegetarian distribution
        Map<Boolean, Long> vegDistribution = orders.stream()
                .filter(order -> order.getIsVegetarian() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getIsVegetarian,
                    Collectors.counting()
                ));
        
        // Revenue by vegetarian status
        Map<Boolean, Double> vegRevenue = orders.stream()
                .filter(order -> order.getIsVegetarian() != null && order.getItemPriceLkr() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getIsVegetarian,
                    Collectors.summingDouble(order -> order.getItemPriceLkr().doubleValue())
                ));
        
        // Popular vegetarian items
        List<Map<String, Object>> popularVegItems = orders.stream()
                .filter(order -> order.getIsVegetarian() != null && 
                               order.getIsVegetarian() && 
                               order.getMenuItemName() != null)
                .collect(Collectors.groupingBy(
                    RestaurantOrder::getMenuItemName,
                    Collectors.counting()
                ))
                .entrySet().stream()
                .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
                .limit(10)
                .map(entry -> {
                    Map<String, Object> item = new HashMap<>();
                    item.put("itemName", entry.getKey());
                    item.put("orderCount", entry.getValue());
                    return item;
                })
                .collect(Collectors.toList());
        
        vegAnalysis.put("distribution", vegDistribution);
        vegAnalysis.put("revenue", vegRevenue);
        vegAnalysis.put("popularVegetarianItems", popularVegItems);
        
        return vegAnalysis;
    }
}