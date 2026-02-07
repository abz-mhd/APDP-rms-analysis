package com.restaurant.analytics.analytics;

import com.restaurant.analytics.model.RestaurantOrder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.boot.test.context.SpringBootTest;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@DisplayName("Customer Analytics Test Suite")
public class CustomerAnalyticsTest {
    
    private CustomerAnalytics customerAnalytics;
    private List<RestaurantOrder> testOrders;
    
    @BeforeEach
    void setUp() {
        customerAnalytics = new CustomerAnalytics();
        testOrders = createTestOrders();
    }
    
    @Test
    @DisplayName("TC011 - Generate Customer Demographics Analysis")
    void testGenerateCustomerDemographicsAnalysis() {
        // Pre-condition: Valid customer orders with demographic data
        assertNotNull(testOrders);
        assertFalse(testOrders.isEmpty());
        
        // Steps: Generate demographics analysis
        Map<String, Object> result = customerAnalytics.generateCustomerDemographicsAnalysis(testOrders);
        
        // Expected Output: Complete demographics analysis with all components
        assertNotNull(result);
        assertTrue(result.containsKey("ageDistribution"));
        assertTrue(result.containsKey("genderDistribution"));
        assertTrue(result.containsKey("loyaltyGroupAnalysis"));
        assertTrue(result.containsKey("customerSegmentation"));
        assertTrue(result.containsKey("spendingPatterns"));
        
        // Actual Result: All demographic analysis components present
        assertEquals(5, result.size());
    }
    
    @Test
    @DisplayName("TC012 - Calculate Age Distribution Correctly")
    void testCalculateAgeDistributionCorrectly() {
        // Pre-condition: Orders with customers of different ages
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithAge("CUST1", 22),  // 18-24 group
            createOrderWithAge("CUST2", 30),  // 25-34 group
            createOrderWithAge("CUST3", 45),  // 45-54 group
            createOrderWithAge("CUST4", 25)   // 25-34 group
        );
        
        // Steps: Generate age distribution analysis
        Map<String, Object> result = customerAnalytics.generateCustomerDemographicsAnalysis(orders);
        Map<String, Long> ageDistribution = (Map<String, Long>) result.get("ageDistribution");
        
        // Expected Output: Correct age group counts
        assertEquals(1L, ageDistribution.get("18-24"));
        assertEquals(2L, ageDistribution.get("25-34"));
        assertEquals(1L, ageDistribution.get("45-54"));
        
        // Actual Result: Age distribution calculated accurately
    }
    
    @Test
    @DisplayName("TC013 - Analyze Gender Distribution")
    void testAnalyzeGenderDistribution() {
        // Pre-condition: Orders with gender information
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithGender("CUST1", "Male"),
            createOrderWithGender("CUST2", "Female"),
            createOrderWithGender("CUST3", "Male"),
            createOrderWithGender("CUST4", "Female"),
            createOrderWithGender("CUST5", "Female")
        );
        
        // Steps: Analyze gender distribution
        Map<String, Object> result = customerAnalytics.generateCustomerDemographicsAnalysis(orders);
        Map<String, Long> genderDistribution = (Map<String, Long>) result.get("genderDistribution");
        
        // Expected Output: 2 Male, 3 Female customers
        assertEquals(2L, genderDistribution.get("Male"));
        assertEquals(3L, genderDistribution.get("Female"));
        
        // Actual Result: Gender distribution is accurate
    }
    
    @Test
    @DisplayName("TC014 - Calculate Loyalty Group Analysis")
    void testCalculateLoyaltyGroupAnalysis() {
        // Pre-condition: Orders with loyalty group data
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithLoyalty("CUST1", "VIP", new BigDecimal("5000.00")),
            createOrderWithLoyalty("CUST2", "Regular", new BigDecimal("2000.00")),
            createOrderWithLoyalty("CUST3", "VIP", new BigDecimal("4500.00")),
            createOrderWithLoyalty("CUST4", "Occasional", new BigDecimal("1000.00"))
        );
        
        // Steps: Analyze loyalty groups
        Map<String, Object> result = customerAnalytics.generateCustomerDemographicsAnalysis(orders);
        Map<String, Object> loyaltyAnalysis = (Map<String, Object>) result.get("loyaltyGroupAnalysis");
        Map<String, Long> loyaltyDistribution = (Map<String, Long>) loyaltyAnalysis.get("distribution");
        Map<String, Double> loyaltySpending = (Map<String, Double>) loyaltyAnalysis.get("averageSpending");
        
        // Expected Output: Correct loyalty group distribution and spending
        assertEquals(2L, loyaltyDistribution.get("VIP"));
        assertEquals(1L, loyaltyDistribution.get("Regular"));
        assertEquals(1L, loyaltyDistribution.get("Occasional"));
        
        assertEquals(4750.0, loyaltySpending.get("VIP"), 0.01);
        assertEquals(2000.0, loyaltySpending.get("Regular"), 0.01);
        
        // Actual Result: Loyalty analysis is comprehensive and accurate
    }
    
    @Test
    @DisplayName("TC015 - Generate Customer Segmentation RFM Analysis")
    void testGenerateCustomerSegmentationRFMAnalysis() {
        // Pre-condition: Multiple orders per customer for RFM calculation
        LocalDateTime now = LocalDateTime.now();
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithCustomerAndDate("CUST1", now.minusDays(5), new BigDecimal("1500.00")),
            createOrderWithCustomerAndDate("CUST1", now.minusDays(10), new BigDecimal("2000.00")),
            createOrderWithCustomerAndDate("CUST2", now.minusDays(30), new BigDecimal("1000.00"))
        );
        
        // Steps: Generate customer segmentation
        Map<String, Object> result = customerAnalytics.generateCustomerDemographicsAnalysis(orders);
        Map<String, Object> segmentation = (Map<String, Object>) result.get("customerSegmentation");
        List<Map<String, Object>> rfmAnalysis = (List<Map<String, Object>>) segmentation.get("rfmAnalysis");
        
        // Expected Output: RFM analysis for each customer
        assertNotNull(rfmAnalysis);
        assertEquals(2, rfmAnalysis.size());
        
        // Find CUST1 analysis
        Map<String, Object> cust1Analysis = rfmAnalysis.stream()
                .filter(rfm -> "CUST1".equals(rfm.get("customerId")))
                .findFirst()
                .orElse(null);
        
        assertNotNull(cust1Analysis);
        assertEquals(2, cust1Analysis.get("frequency"));
        assertEquals(3500.0, (Double) cust1Analysis.get("monetary"), 0.01);
        
        // Actual Result: RFM analysis provides detailed customer insights
    }
    
    @Test
    @DisplayName("TC016 - Generate Seasonal Behavior Analysis")
    void testGenerateSeasonalBehaviorAnalysis() {
        // Pre-condition: Orders from different seasons
        LocalDateTime spring = LocalDateTime.of(2024, 4, 15, 12, 0);
        LocalDateTime summer = LocalDateTime.of(2024, 7, 15, 12, 0);
        LocalDateTime autumn = LocalDateTime.of(2024, 10, 15, 12, 0);
        
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithCustomerAndDate("CUST1", spring, new BigDecimal("1500.00")),
            createOrderWithCustomerAndDate("CUST1", summer, new BigDecimal("2000.00")),
            createOrderWithCustomerAndDate("CUST2", autumn, new BigDecimal("1800.00"))
        );
        
        // Steps: Generate seasonal behavior analysis
        Map<String, Object> result = customerAnalytics.generateSeasonalBehaviorAnalysis(orders);
        
        // Expected Output: Seasonal analysis with retention and spending data
        assertNotNull(result);
        assertTrue(result.containsKey("seasonalRetention"));
        assertTrue(result.containsKey("loyaltyIndex"));
        assertTrue(result.containsKey("seasonalSpending"));
        assertTrue(result.containsKey("customerLifecycle"));
        
        // Actual Result: Comprehensive seasonal behavior analysis
        assertEquals(4, result.size());
    }
    
    @Test
    @DisplayName("TC017 - Calculate Spending Patterns by Demographics")
    void testCalculateSpendingPatternsByDemographics() {
        // Pre-condition: Orders with age and gender data
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithDemographics("CUST1", 25, "Male", new BigDecimal("2000.00")),
            createOrderWithDemographics("CUST2", 30, "Male", new BigDecimal("2500.00")),
            createOrderWithDemographics("CUST3", 28, "Female", new BigDecimal("1800.00")),
            createOrderWithDemographics("CUST4", 35, "Female", new BigDecimal("2200.00"))
        );
        
        // Steps: Analyze spending patterns
        Map<String, Object> result = customerAnalytics.generateCustomerDemographicsAnalysis(orders);
        Map<String, Object> spendingPatterns = (Map<String, Object>) result.get("spendingPatterns");
        Map<String, Double> spendingByGender = (Map<String, Double>) spendingPatterns.get("spendingByGender");
        
        // Expected Output: Average spending by gender
        assertEquals(2250.0, spendingByGender.get("Male"), 0.01);
        assertEquals(2000.0, spendingByGender.get("Female"), 0.01);
        
        // Actual Result: Spending patterns calculated correctly
    }
    
    @Test
    @DisplayName("TC018 - Handle Empty Customer Data")
    void testHandleEmptyCustomerData() {
        // Pre-condition: Empty customer order list
        List<RestaurantOrder> emptyOrders = new ArrayList<>();
        
        // Steps: Generate analysis with empty data
        Map<String, Object> result = customerAnalytics.generateCustomerDemographicsAnalysis(emptyOrders);
        
        // Expected Output: Analysis should handle empty data gracefully
        assertNotNull(result);
        Map<String, Long> ageDistribution = (Map<String, Long>) result.get("ageDistribution");
        Map<String, Long> genderDistribution = (Map<String, Long>) result.get("genderDistribution");
        
        assertTrue(ageDistribution.isEmpty());
        assertTrue(genderDistribution.isEmpty());
        
        // Actual Result: Empty data handled without errors
    }
    
    @Test
    @DisplayName("TC019 - Calculate Customer Loyalty Index")
    void testCalculateCustomerLoyaltyIndex() {
        // Pre-condition: Customers with varying order frequencies
        LocalDateTime now = LocalDateTime.now();
        List<RestaurantOrder> orders = Arrays.asList(
            // High frequency customer
            createOrderWithCustomerAndDate("CUST_HIGH", now.minusDays(1), new BigDecimal("1000.00")),
            createOrderWithCustomerAndDate("CUST_HIGH", now.minusDays(5), new BigDecimal("1200.00")),
            createOrderWithCustomerAndDate("CUST_HIGH", now.minusDays(10), new BigDecimal("1100.00")),
            // Low frequency customer
            createOrderWithCustomerAndDate("CUST_LOW", now.minusDays(60), new BigDecimal("2000.00"))
        );
        
        // Steps: Generate loyalty index analysis
        Map<String, Object> result = customerAnalytics.generateSeasonalBehaviorAnalysis(orders);
        Map<String, Object> loyaltyIndex = (Map<String, Object>) result.get("loyaltyIndex");
        List<Map<String, Object>> customerLoyalty = (List<Map<String, Object>>) loyaltyIndex.get("customerLoyalty");
        
        // Expected Output: Different loyalty scores for different customers
        assertNotNull(customerLoyalty);
        assertEquals(2, customerLoyalty.size());
        
        // High frequency customer should have higher loyalty score
        Map<String, Object> highFreqCustomer = customerLoyalty.stream()
                .filter(loyalty -> "CUST_HIGH".equals(loyalty.get("customerId")))
                .findFirst()
                .orElse(null);
        
        assertNotNull(highFreqCustomer);
        assertEquals(3, highFreqCustomer.get("orderCount"));
        
        // Actual Result: Loyalty index reflects customer behavior patterns
    }
    
    @Test
    @DisplayName("TC020 - Analyze Customer Lifecycle Patterns")
    void testAnalyzeCustomerLifecyclePatterns() {
        // Pre-condition: Customers with orders spanning different time periods
        LocalDateTime firstOrder = LocalDateTime.of(2024, 1, 1, 12, 0);
        LocalDateTime lastOrder = LocalDateTime.of(2024, 6, 1, 12, 0);
        
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithCustomerAndDate("CUST_LONG", firstOrder, new BigDecimal("1500.00")),
            createOrderWithCustomerAndDate("CUST_LONG", firstOrder.plusDays(30), new BigDecimal("1800.00")),
            createOrderWithCustomerAndDate("CUST_LONG", lastOrder, new BigDecimal("2000.00"))
        );
        
        // Steps: Generate customer lifecycle analysis
        Map<String, Object> result = customerAnalytics.generateSeasonalBehaviorAnalysis(orders);
        Map<String, Object> lifecycle = (Map<String, Object>) result.get("customerLifecycle");
        List<Map<String, Object>> customerLifecycles = (List<Map<String, Object>>) lifecycle.get("customerLifecycles");
        
        // Expected Output: Customer lifespan calculation
        assertNotNull(customerLifecycles);
        assertEquals(1, customerLifecycles.size());
        
        Map<String, Object> customerLifecycle = customerLifecycles.get(0);
        assertEquals("CUST_LONG", customerLifecycle.get("customerId"));
        // Allow for slight variation in day calculation due to leap years
        Long lifespanDays = (Long) customerLifecycle.get("lifespanDays");
        assertTrue(lifespanDays >= 151 && lifespanDays <= 152); // Days between Jan 1 and Jun 1
        
        // Actual Result: Customer lifecycle analysis provides temporal insights
    }
    
    // Helper methods for creating test data
    private List<RestaurantOrder> createTestOrders() {
        List<RestaurantOrder> orders = new ArrayList<>();
        
        RestaurantOrder order1 = new RestaurantOrder();
        order1.setOrderId("ORDER_001");
        order1.setCustomerId("CUST_001");
        order1.setAge(28);
        order1.setGender("Male");
        order1.setLoyaltyGroup("Regular");
        order1.setTotalPriceLkr(new BigDecimal("1500.00"));
        order1.setOrderPlaced(LocalDateTime.now().minusDays(1));
        orders.add(order1);
        
        RestaurantOrder order2 = new RestaurantOrder();
        order2.setOrderId("ORDER_002");
        order2.setCustomerId("CUST_002");
        order2.setAge(35);
        order2.setGender("Female");
        order2.setLoyaltyGroup("VIP");
        order2.setTotalPriceLkr(new BigDecimal("2500.00"));
        order2.setOrderPlaced(LocalDateTime.now().minusDays(2));
        orders.add(order2);
        
        return orders;
    }
    
    private RestaurantOrder createOrderWithAge(String customerId, int age) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + customerId);
        order.setCustomerId(customerId);
        order.setAge(age);
        order.setTotalPriceLkr(new BigDecimal("1000.00"));
        return order;
    }
    
    private RestaurantOrder createOrderWithGender(String customerId, String gender) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + customerId);
        order.setCustomerId(customerId);
        order.setGender(gender);
        order.setTotalPriceLkr(new BigDecimal("1000.00"));
        return order;
    }
    
    private RestaurantOrder createOrderWithLoyalty(String customerId, String loyaltyGroup, BigDecimal price) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + customerId);
        order.setCustomerId(customerId);
        order.setLoyaltyGroup(loyaltyGroup);
        order.setTotalPriceLkr(price);
        return order;
    }
    
    private RestaurantOrder createOrderWithCustomerAndDate(String customerId, LocalDateTime orderDate, BigDecimal price) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + customerId + "_" + orderDate.getDayOfYear());
        order.setCustomerId(customerId);
        order.setOrderPlaced(orderDate);
        order.setTotalPriceLkr(price);
        return order;
    }
    
    private RestaurantOrder createOrderWithDemographics(String customerId, int age, String gender, BigDecimal price) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + customerId);
        order.setCustomerId(customerId);
        order.setAge(age);
        order.setGender(gender);
        order.setTotalPriceLkr(price);
        return order;
    }
}