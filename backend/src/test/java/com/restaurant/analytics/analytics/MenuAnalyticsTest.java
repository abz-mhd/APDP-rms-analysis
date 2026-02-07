package com.restaurant.analytics.analytics;

import com.restaurant.analytics.model.RestaurantOrder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.boot.test.context.SpringBootTest;

import java.math.BigDecimal;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@DisplayName("Menu Analytics Test Suite")
public class MenuAnalyticsTest {
    
    private MenuAnalytics menuAnalytics;
    private List<RestaurantOrder> testOrders;
    
    @BeforeEach
    void setUp() {
        menuAnalytics = new MenuAnalytics();
        testOrders = createTestOrders();
    }
    
    @Test
    @DisplayName("TC021 - Generate Complete Menu Analysis")
    void testGenerateCompleteMenuAnalysis() {
        // Pre-condition: Valid menu orders with item details
        assertNotNull(testOrders);
        assertFalse(testOrders.isEmpty());
        
        // Steps: Generate menu analysis
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(testOrders);
        
        // Expected Output: Complete menu analysis with all components
        assertNotNull(result);
        assertTrue(result.containsKey("popularItems"));
        assertTrue(result.containsKey("categoryAnalysis"));
        assertTrue(result.containsKey("itemCombos"));
        assertTrue(result.containsKey("sankeyDiagramData"));
        assertTrue(result.containsKey("spiceLevelPreferences"));
        assertTrue(result.containsKey("vegetarianAnalysis"));
        
        // Actual Result: All menu analysis components present
        assertEquals(6, result.size());
    }
    
    @Test
    @DisplayName("TC022 - Identify Popular Menu Items")
    void testIdentifyPopularMenuItems() {
        // Pre-condition: Orders with different menu items and frequencies
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithMenuItem("Chicken Curry", "Main Course", new BigDecimal("1500.00")),
            createOrderWithMenuItem("Chicken Curry", "Main Course", new BigDecimal("1500.00")),
            createOrderWithMenuItem("Fried Rice", "Main Course", new BigDecimal("1200.00")),
            createOrderWithMenuItem("Ice Cream", "Dessert", new BigDecimal("500.00")),
            createOrderWithMenuItem("Chicken Curry", "Main Course", new BigDecimal("1500.00"))
        );
        
        // Steps: Analyze popular items
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        List<Map<String, Object>> popularItems = (List<Map<String, Object>>) result.get("popularItems");
        
        // Expected Output: Chicken Curry should be most popular (3 orders)
        assertNotNull(popularItems);
        assertFalse(popularItems.isEmpty());
        
        Map<String, Object> mostPopular = popularItems.get(0);
        assertEquals("Chicken Curry", mostPopular.get("itemName"));
        assertEquals(3L, mostPopular.get("orderCount"));
        assertEquals(4500.0, (Double) mostPopular.get("totalRevenue"), 0.01);
        
        // Actual Result: Popular items ranked correctly by frequency
    }
    
    @Test
    @DisplayName("TC023 - Analyze Menu Categories")
    void testAnalyzeMenuCategories() {
        // Pre-condition: Orders from different menu categories
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithMenuItem("Chicken Curry", "Main Course", new BigDecimal("1500.00")),
            createOrderWithMenuItem("Fried Rice", "Main Course", new BigDecimal("1200.00")),
            createOrderWithMenuItem("Ice Cream", "Dessert", new BigDecimal("500.00")),
            createOrderWithMenuItem("Cake", "Dessert", new BigDecimal("800.00")),
            createOrderWithMenuItem("Soup", "Appetizer", new BigDecimal("600.00"))
        );
        
        // Steps: Generate category analysis
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        Map<String, Object> categoryAnalysis = (Map<String, Object>) result.get("categoryAnalysis");
        Map<String, Long> ordersByCategory = (Map<String, Long>) categoryAnalysis.get("ordersByCategory");
        Map<String, Double> revenueByCategory = (Map<String, Double>) categoryAnalysis.get("revenueByCategory");
        
        // Expected Output: Main Course = 2 orders, Dessert = 2 orders, Appetizer = 1 order
        assertEquals(2L, ordersByCategory.get("Main Course"));
        assertEquals(2L, ordersByCategory.get("Dessert"));
        assertEquals(1L, ordersByCategory.get("Appetizer"));
        
        assertEquals(2700.0, revenueByCategory.get("Main Course"), 0.01);
        assertEquals(1300.0, revenueByCategory.get("Dessert"), 0.01);
        assertEquals(600.0, revenueByCategory.get("Appetizer"), 0.01);
        
        // Actual Result: Category analysis provides comprehensive breakdown
    }
    
    @Test
    @DisplayName("TC024 - Detect Item Combinations")
    void testDetectItemCombinations() {
        // Pre-condition: Orders with multiple items (same order ID)
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithItems("ORDER1", "Chicken Curry", "Main Course"),
            createOrderWithItems("ORDER1", "Rice", "Side Dish"),
            createOrderWithItems("ORDER1", "Ice Cream", "Dessert"),
            createOrderWithItems("ORDER2", "Chicken Curry", "Main Course"),
            createOrderWithItems("ORDER2", "Rice", "Side Dish"),
            createOrderWithItems("ORDER3", "Fish Curry", "Main Course")
        );
        
        // Steps: Analyze item combinations
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        List<Map<String, Object>> itemCombos = (List<Map<String, Object>>) result.get("itemCombos");
        
        // Expected Output: Chicken Curry + Rice + Ice Cream combo should be detected
        assertNotNull(itemCombos);
        assertFalse(itemCombos.isEmpty());
        
        // Find the combo with highest frequency
        Map<String, Object> topCombo = itemCombos.get(0);
        assertEquals(1L, topCombo.get("frequency"));
        assertTrue(((List<String>) topCombo.get("items")).contains("Chicken Curry"));
        assertTrue(((List<String>) topCombo.get("items")).contains("Rice"));
        
        // Actual Result: Item combinations identified correctly
    }
    
    @Test
    @DisplayName("TC025 - Generate Sankey Diagram Data")
    void testGenerateSankeyDiagramData() {
        // Pre-condition: Orders with category to item relationships
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithMenuItem("Chicken Curry", "Main Course", new BigDecimal("1500.00")),
            createOrderWithMenuItem("Fish Curry", "Main Course", new BigDecimal("1600.00")),
            createOrderWithMenuItem("Ice Cream", "Dessert", new BigDecimal("500.00")),
            createOrderWithMenuItem("Cake", "Dessert", new BigDecimal("800.00"))
        );
        
        // Steps: Generate Sankey diagram data
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        Map<String, Object> sankeyData = (Map<String, Object>) result.get("sankeyDiagramData");
        List<Map<String, Object>> nodes = (List<Map<String, Object>>) sankeyData.get("nodes");
        List<Map<String, Object>> flows = (List<Map<String, Object>>) sankeyData.get("flows");
        
        // Expected Output: Nodes for categories and items, flows between them
        assertNotNull(nodes);
        assertNotNull(flows);
        assertTrue(nodes.size() >= 6); // 2 categories + 4 items
        assertEquals(4, flows.size()); // 4 category-to-item flows
        
        // Verify flow structure
        Map<String, Object> firstFlow = flows.get(0);
        assertTrue(firstFlow.containsKey("source"));
        assertTrue(firstFlow.containsKey("target"));
        assertTrue(firstFlow.containsKey("value"));
        
        // Actual Result: Sankey diagram data structured correctly
    }
    
    @Test
    @DisplayName("TC026 - Analyze Spice Level Preferences")
    void testAnalyzeSpiceLevelPreferences() {
        // Pre-condition: Orders with different spice levels
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithSpiceLevel("Mild"),
            createOrderWithSpiceLevel("Medium"),
            createOrderWithSpiceLevel("Hot"),
            createOrderWithSpiceLevel("Medium"),
            createOrderWithSpiceLevel("Mild"),
            createOrderWithSpiceLevel("Mild")
        );
        
        // Steps: Analyze spice level preferences
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        Map<String, Long> spiceLevelPreferences = (Map<String, Long>) result.get("spiceLevelPreferences");
        
        // Expected Output: Mild = 3, Medium = 2, Hot = 1
        assertEquals(3L, spiceLevelPreferences.get("Mild"));
        assertEquals(2L, spiceLevelPreferences.get("Medium"));
        assertEquals(1L, spiceLevelPreferences.get("Hot"));
        
        // Actual Result: Spice level preferences calculated accurately
    }
    
    @Test
    @DisplayName("TC027 - Analyze Vegetarian vs Non-Vegetarian Preferences")
    void testAnalyzeVegetarianPreferences() {
        // Pre-condition: Orders with vegetarian and non-vegetarian items
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithVegetarian("Vegetable Curry", true, new BigDecimal("1200.00")),
            createOrderWithVegetarian("Chicken Curry", false, new BigDecimal("1500.00")),
            createOrderWithVegetarian("Dal Curry", true, new BigDecimal("1000.00")),
            createOrderWithVegetarian("Fish Curry", false, new BigDecimal("1600.00")),
            createOrderWithVegetarian("Vegetable Fried Rice", true, new BigDecimal("1100.00"))
        );
        
        // Steps: Analyze vegetarian preferences
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        Map<String, Object> vegAnalysis = (Map<String, Object>) result.get("vegetarianAnalysis");
        Map<Boolean, Long> vegDistribution = (Map<Boolean, Long>) vegAnalysis.get("distribution");
        Map<Boolean, Double> vegRevenue = (Map<Boolean, Double>) vegAnalysis.get("revenue");
        
        // Expected Output: 3 vegetarian, 2 non-vegetarian orders
        assertEquals(3L, vegDistribution.get(true));
        assertEquals(2L, vegDistribution.get(false));
        
        assertEquals(3300.0, vegRevenue.get(true), 0.01); // Vegetarian revenue
        assertEquals(3100.0, vegRevenue.get(false), 0.01); // Non-vegetarian revenue
        
        // Actual Result: Vegetarian analysis provides detailed insights
    }
    
    @Test
    @DisplayName("TC028 - Handle Menu Items with Null Values")
    void testHandleMenuItemsWithNullValues() {
        // Pre-condition: Orders with some null menu item data
        RestaurantOrder orderWithNulls = new RestaurantOrder();
        orderWithNulls.setOrderId("ORDER_NULL");
        orderWithNulls.setMenuItemName(null);
        orderWithNulls.setCategory(null);
        orderWithNulls.setItemPriceLkr(null);
        
        List<RestaurantOrder> orders = Arrays.asList(
            orderWithNulls,
            createOrderWithMenuItem("Chicken Curry", "Main Course", new BigDecimal("1500.00"))
        );
        
        // Steps: Generate analysis with null values
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        
        // Expected Output: Analysis should handle nulls gracefully
        assertNotNull(result);
        List<Map<String, Object>> popularItems = (List<Map<String, Object>>) result.get("popularItems");
        assertEquals(1, popularItems.size()); // Only non-null item counted
        assertEquals("Chicken Curry", popularItems.get(0).get("itemName"));
        
        // Actual Result: Null values handled without errors
    }
    
    @Test
    @DisplayName("TC029 - Calculate Average Category Prices")
    void testCalculateAverageCategoryPrices() {
        // Pre-condition: Orders with items from same category at different prices
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithMenuItem("Chicken Curry", "Main Course", new BigDecimal("1500.00")),
            createOrderWithMenuItem("Fish Curry", "Main Course", new BigDecimal("1600.00")),
            createOrderWithMenuItem("Beef Curry", "Main Course", new BigDecimal("1700.00")),
            createOrderWithMenuItem("Ice Cream", "Dessert", new BigDecimal("500.00")),
            createOrderWithMenuItem("Cake", "Dessert", new BigDecimal("700.00"))
        );
        
        // Steps: Calculate average prices by category
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        Map<String, Object> categoryAnalysis = (Map<String, Object>) result.get("categoryAnalysis");
        Map<String, Double> avgPriceByCategory = (Map<String, Double>) categoryAnalysis.get("averagePriceByCategory");
        
        // Expected Output: Main Course avg = 1600.00, Dessert avg = 600.00
        assertEquals(1600.0, avgPriceByCategory.get("Main Course"), 0.01);
        assertEquals(600.0, avgPriceByCategory.get("Dessert"), 0.01);
        
        // Actual Result: Average category prices calculated correctly
    }
    
    @Test
    @DisplayName("TC030 - Identify Popular Vegetarian Items")
    void testIdentifyPopularVegetarianItems() {
        // Pre-condition: Mix of vegetarian and non-vegetarian items
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithVegetarian("Vegetable Curry", true, new BigDecimal("1200.00")),
            createOrderWithVegetarian("Vegetable Curry", true, new BigDecimal("1200.00")),
            createOrderWithVegetarian("Dal Curry", true, new BigDecimal("1000.00")),
            createOrderWithVegetarian("Chicken Curry", false, new BigDecimal("1500.00")),
            createOrderWithVegetarian("Vegetable Curry", true, new BigDecimal("1200.00"))
        );
        
        // Steps: Identify popular vegetarian items
        Map<String, Object> result = menuAnalytics.generateMenuAnalysis(orders);
        Map<String, Object> vegAnalysis = (Map<String, Object>) result.get("vegetarianAnalysis");
        List<Map<String, Object>> popularVegItems = (List<Map<String, Object>>) vegAnalysis.get("popularVegetarianItems");
        
        // Expected Output: Vegetable Curry should be most popular vegetarian item
        assertNotNull(popularVegItems);
        assertFalse(popularVegItems.isEmpty());
        
        Map<String, Object> topVegItem = popularVegItems.get(0);
        assertEquals("Vegetable Curry", topVegItem.get("itemName"));
        assertEquals(3L, topVegItem.get("orderCount"));
        
        // Actual Result: Popular vegetarian items identified correctly
    }
    
    // Helper methods for creating test data
    private List<RestaurantOrder> createTestOrders() {
        List<RestaurantOrder> orders = new ArrayList<>();
        
        RestaurantOrder order1 = new RestaurantOrder();
        order1.setOrderId("ORDER_001");
        order1.setMenuItemName("Chicken Curry");
        order1.setCategory("Main Course");
        order1.setItemPriceLkr(new BigDecimal("1500.00"));
        order1.setIsVegetarian(false);
        order1.setSpiceLevel("Medium");
        orders.add(order1);
        
        RestaurantOrder order2 = new RestaurantOrder();
        order2.setOrderId("ORDER_002");
        order2.setMenuItemName("Vegetable Curry");
        order2.setCategory("Main Course");
        order2.setItemPriceLkr(new BigDecimal("1200.00"));
        order2.setIsVegetarian(true);
        order2.setSpiceLevel("Mild");
        orders.add(order2);
        
        return orders;
    }
    
    private RestaurantOrder createOrderWithMenuItem(String itemName, String category, BigDecimal price) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + itemName.replaceAll(" ", "_"));
        order.setMenuItemName(itemName);
        order.setCategory(category);
        order.setItemPriceLkr(price);
        return order;
    }
    
    private RestaurantOrder createOrderWithItems(String orderId, String itemName, String category) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId(orderId);
        order.setMenuItemName(itemName);
        order.setCategory(category);
        order.setItemPriceLkr(new BigDecimal("1000.00"));
        return order;
    }
    
    private RestaurantOrder createOrderWithSpiceLevel(String spiceLevel) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + spiceLevel);
        order.setMenuItemName("Test Item");
        order.setSpiceLevel(spiceLevel);
        return order;
    }
    
    private RestaurantOrder createOrderWithVegetarian(String itemName, boolean isVegetarian, BigDecimal price) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + itemName.replaceAll(" ", "_"));
        order.setMenuItemName(itemName);
        order.setIsVegetarian(isVegetarian);
        order.setItemPriceLkr(price);
        return order;
    }
}