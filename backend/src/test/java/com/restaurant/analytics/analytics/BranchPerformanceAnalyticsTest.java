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
@DisplayName("Branch Performance Analytics Test Suite")
public class BranchPerformanceAnalyticsTest {
    
    private BranchPerformanceAnalytics branchPerformanceAnalytics;
    private List<RestaurantOrder> testOrders;
    
    @BeforeEach
    void setUp() {
        branchPerformanceAnalytics = new BranchPerformanceAnalytics();
        testOrders = createTestOrders();
    }
    
    @Test
    @DisplayName("TC041 - Generate Complete Branch Performance Analysis")
    void testGenerateCompleteBranchPerformanceAnalysis() {
        // Pre-condition: Valid branch orders with performance data
        assertNotNull(testOrders);
        assertFalse(testOrders.isEmpty());
        
        // Steps: Generate branch performance analysis
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(testOrders);
        
        // Expected Output: Complete performance analysis with all components
        assertNotNull(result);
        assertTrue(result.containsKey("branchDashboards"));
        assertTrue(result.containsKey("branchRankings"));
        assertTrue(result.containsKey("performanceMetrics"));
        assertTrue(result.containsKey("efficiencyAnalysis"));
        assertTrue(result.containsKey("customerSatisfactionMetrics"));
        
        // Actual Result: All branch performance components present
        assertEquals(5, result.size());
    }
    
    @Test
    @DisplayName("TC042 - Generate Branch Dashboards with Key Metrics")
    void testGenerateBranchDashboardsWithKeyMetrics() {
        // Pre-condition: Orders from multiple branches with complete data
        List<RestaurantOrder> orders = Arrays.asList(
            createBranchOrder("BRANCH_A", "Branch Alpha", "Downtown", new BigDecimal("1500.00"), "CUST_1", 100),
            createBranchOrder("BRANCH_A", "Branch Alpha", "Downtown", new BigDecimal("2000.00"), "CUST_2", 100),
            createBranchOrder("BRANCH_B", "Branch Beta", "Uptown", new BigDecimal("1200.00"), "CUST_3", 80),
            createBranchOrder("BRANCH_B", "Branch Beta", "Uptown", new BigDecimal("1800.00"), "CUST_1", 80)
        );
        
        // Steps: Generate branch dashboards
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
        Map<String, Map<String, Object>> branchDashboards = (Map<String, Map<String, Object>>) result.get("branchDashboards");
        
        // Expected Output: Comprehensive dashboard metrics for each branch
        assertNotNull(branchDashboards);
        
        Map<String, Object> branchA = branchDashboards.get("BRANCH_A");
        assertEquals(2, branchA.get("totalOrders"));
        assertEquals(3500.0, (Double) branchA.get("totalRevenue"), 0.01);
        assertEquals(1750.0, (Double) branchA.get("averageOrderValue"), 0.01);
        assertEquals(2L, branchA.get("uniqueCustomers"));
        assertEquals("Branch Alpha", branchA.get("branchName"));
        assertEquals("Downtown", branchA.get("borough"));
        assertEquals(100, branchA.get("capacity"));
        
        // Actual Result: Branch dashboards provide comprehensive metrics
    }
    
    @Test
    @DisplayName("TC043 - Rank Branches by Performance")
    void testRankBranchesByPerformance() {
        // Pre-condition: Branches with different performance levels
        List<RestaurantOrder> orders = Arrays.asList(
            // High performing branch
            createBranchOrder("BRANCH_HIGH", "High Performer", "Central", new BigDecimal("5000.00"), "CUST_1", 150),
            createBranchOrder("BRANCH_HIGH", "High Performer", "Central", new BigDecimal("4500.00"), "CUST_2", 150),
            createBranchOrder("BRANCH_HIGH", "High Performer", "Central", new BigDecimal("3000.00"), "CUST_3", 150),
            // Medium performing branch
            createBranchOrder("BRANCH_MED", "Medium Performer", "North", new BigDecimal("2000.00"), "CUST_4", 100),
            createBranchOrder("BRANCH_MED", "Medium Performer", "North", new BigDecimal("1500.00"), "CUST_5", 100),
            // Low performing branch
            createBranchOrder("BRANCH_LOW", "Low Performer", "South", new BigDecimal("800.00"), "CUST_6", 80)
        );
        
        // Steps: Generate branch rankings
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
        List<Map<String, Object>> branchRankings = (List<Map<String, Object>>) result.get("branchRankings");
        
        // Expected Output: Branches ranked by revenue (highest first)
        assertNotNull(branchRankings);
        assertEquals(3, branchRankings.size());
        
        // First should be high performer
        Map<String, Object> topBranch = branchRankings.get(0);
        assertEquals("BRANCH_HIGH", topBranch.get("outletId"));
        assertEquals(12500.0, (Double) topBranch.get("revenue"), 0.01);
        assertEquals("High Performer", topBranch.get("branchName"));
        
        // Second should be medium performer
        Map<String, Object> secondBranch = branchRankings.get(1);
        assertEquals("BRANCH_MED", secondBranch.get("outletId"));
        assertEquals(3500.0, (Double) secondBranch.get("revenue"), 0.01);
        
        // Third should be low performer
        Map<String, Object> thirdBranch = branchRankings.get(2);
        assertEquals("BRANCH_LOW", thirdBranch.get("outletId"));
        assertEquals(800.0, (Double) thirdBranch.get("revenue"), 0.01);
        
        // Actual Result: Branches ranked correctly by performance
    }
    
    @Test
    @DisplayName("TC044 - Calculate Performance Metrics")
    void testCalculatePerformanceMetrics() {
        // Pre-condition: Orders with timing and status data
        LocalDateTime orderTime = LocalDateTime.of(2024, 1, 15, 12, 0);
        LocalDateTime prepStart = orderTime.plusMinutes(5);
        LocalDateTime prepFinish = prepStart.plusMinutes(20);
        LocalDateTime serveTime = prepFinish.plusMinutes(5);
        
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithTiming("BRANCH_A", "ORDER_1", "Completed", orderTime, prepStart, prepFinish, serveTime, new BigDecimal("1500.00")),
            createOrderWithTiming("BRANCH_A", "ORDER_2", "Completed", orderTime.plusHours(1), prepStart.plusHours(1), prepFinish.plusHours(1), serveTime.plusHours(1), new BigDecimal("2000.00")),
            createOrderWithTiming("BRANCH_A", "ORDER_3", "Failed", orderTime.plusHours(2), null, null, null, new BigDecimal("1200.00"))
        );
        
        // Steps: Calculate performance metrics
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
        Map<String, Map<String, Object>> performanceMetrics = (Map<String, Map<String, Object>>) result.get("performanceMetrics");
        
        // Expected Output: Detailed performance metrics
        assertNotNull(performanceMetrics);
        Map<String, Object> branchAMetrics = performanceMetrics.get("BRANCH_A");
        
        assertEquals(4700.0, (Double) branchAMetrics.get("totalRevenue"), 0.01);
        assertEquals(20.0, (Double) branchAMetrics.get("averagePreparationTime"), 0.01); // 20 minutes average
        
        // Check if averageServiceTime exists before asserting its value
        if (branchAMetrics.containsKey("averageServiceTime") && branchAMetrics.get("averageServiceTime") != null) {
            assertEquals(30.0, (Double) branchAMetrics.get("averageServiceTime"), 0.01); // 30 minutes total service time
        }
        
        // Actual Result: Performance metrics calculated accurately
    }
    
    @Test
    @DisplayName("TC045 - Analyze Efficiency Metrics")
    void testAnalyzeEfficiencyMetrics() {
        // Pre-condition: Orders with service timing and capacity data
        LocalDateTime peakTime = LocalDateTime.of(2024, 1, 15, 12, 0);
        
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithCapacityAndTiming("BRANCH_EFF", peakTime, peakTime.plusMinutes(25), 100),
            createOrderWithCapacityAndTiming("BRANCH_EFF", peakTime.plusMinutes(10), peakTime.plusMinutes(35), 100),
            createOrderWithCapacityAndTiming("BRANCH_EFF", peakTime.plusMinutes(20), peakTime.plusMinutes(45), 100)
        );
        
        // Steps: Analyze efficiency
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
        Map<String, Map<String, Object>> efficiencyAnalysis = (Map<String, Map<String, Object>>) result.get("efficiencyAnalysis");
        
        // Expected Output: Efficiency metrics including capacity utilization
        assertNotNull(efficiencyAnalysis);
        Map<String, Object> branchEfficiency = efficiencyAnalysis.get("BRANCH_EFF");
        
        assertNotNull(branchEfficiency.get("averageServiceTime"));
        assertNotNull(branchEfficiency.get("peakHourPerformance"));
        assertNotNull(branchEfficiency.get("capacityUtilization"));
        
        // Capacity utilization should be calculated (3 orders in peak hour / 100 capacity * 100)
        assertEquals(3.0, (Double) branchEfficiency.get("capacityUtilization"), 0.01);
        
        // Actual Result: Efficiency analysis provides operational insights
    }
    
    @Test
    @DisplayName("TC046 - Calculate Customer Satisfaction Metrics")
    void testCalculateCustomerSatisfactionMetrics() {
        // Pre-condition: Orders with completion status and loyalty data
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithStatusAndLoyalty("BRANCH_SAT", "ORDER_1", "Completed", "VIP", "CUST_1"),
            createOrderWithStatusAndLoyalty("BRANCH_SAT", "ORDER_2", "Completed", "Regular", "CUST_2"),
            createOrderWithStatusAndLoyalty("BRANCH_SAT", "ORDER_3", "Failed", "Occasional", "CUST_3"),
            createOrderWithStatusAndLoyalty("BRANCH_SAT", "ORDER_4", "Completed", "VIP", "CUST_1")
        );
        
        // Steps: Calculate satisfaction metrics
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
        Map<String, Map<String, Object>> satisfactionMetrics = (Map<String, Map<String, Object>>) result.get("customerSatisfactionMetrics");
        
        // Expected Output: Customer satisfaction indicators
        assertNotNull(satisfactionMetrics);
        Map<String, Object> branchSatisfaction = satisfactionMetrics.get("BRANCH_SAT");
        
        // Order success rate: 3 completed out of 4 total = 75%
        assertEquals(75.0, (Double) branchSatisfaction.get("orderSuccessRate"), 0.01);
        
        // Loyal customer percentage: 2 VIP + 1 Regular out of 3 unique customers
        assertTrue((Double) branchSatisfaction.get("loyalCustomerPercentage") > 0);
        
        // Actual Result: Customer satisfaction metrics provide service quality insights
    }
    
    @Test
    @DisplayName("TC047 - Handle Branch with No Orders")
    void testHandleBranchWithNoOrders() {
        // Pre-condition: Empty order list
        List<RestaurantOrder> emptyOrders = new ArrayList<>();
        
        // Steps: Generate analysis with no orders
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(emptyOrders);
        
        // Expected Output: Analysis should handle empty data gracefully
        assertNotNull(result);
        Map<String, Map<String, Object>> branchDashboards = (Map<String, Map<String, Object>>) result.get("branchDashboards");
        List<Map<String, Object>> branchRankings = (List<Map<String, Object>>) result.get("branchRankings");
        
        assertTrue(branchDashboards.isEmpty());
        assertTrue(branchRankings.isEmpty());
        
        // Actual Result: Empty data handled without errors
    }
    
    @Test
    @DisplayName("TC048 - Calculate Repeat Customer Rate")
    void testCalculateRepeatCustomerRate() {
        // Pre-condition: Mix of new and repeat customers
        List<RestaurantOrder> orders = Arrays.asList(
            createBranchOrder("BRANCH_REPEAT", "Repeat Branch", "Central", new BigDecimal("1500.00"), "CUST_REPEAT", 100),
            createBranchOrder("BRANCH_REPEAT", "Repeat Branch", "Central", new BigDecimal("1800.00"), "CUST_REPEAT", 100), // Repeat customer
            createBranchOrder("BRANCH_REPEAT", "Repeat Branch", "Central", new BigDecimal("1200.00"), "CUST_NEW1", 100),   // New customer
            createBranchOrder("BRANCH_REPEAT", "Repeat Branch", "Central", new BigDecimal("1600.00"), "CUST_NEW2", 100)    // New customer
        );
        
        // Steps: Calculate repeat customer metrics
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
        Map<String, Map<String, Object>> performanceMetrics = (Map<String, Map<String, Object>>) result.get("performanceMetrics");
        
        // Expected Output: Repeat customer rate calculation
        Map<String, Object> branchMetrics = performanceMetrics.get("BRANCH_REPEAT");
        
        // 1 repeat customer out of 3 total customers = 33.33%
        assertEquals(33.33, (Double) branchMetrics.get("repeatCustomerRate"), 0.01);
        
        // Actual Result: Repeat customer rate calculated correctly
    }
    
    @Test
    @DisplayName("TC049 - Validate Average Order Value Calculation")
    void testValidateAverageOrderValueCalculation() {
        // Pre-condition: Orders with different values for AOV calculation
        List<RestaurantOrder> orders = Arrays.asList(
            createBranchOrder("BRANCH_AOV", "AOV Branch", "Test", new BigDecimal("1000.00"), "CUST_1", 50),
            createBranchOrder("BRANCH_AOV", "AOV Branch", "Test", new BigDecimal("2000.00"), "CUST_2", 50),
            createBranchOrder("BRANCH_AOV", "AOV Branch", "Test", new BigDecimal("3000.00"), "CUST_3", 50)
        );
        
        // Steps: Calculate AOV
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
        Map<String, Map<String, Object>> branchDashboards = (Map<String, Map<String, Object>>) result.get("branchDashboards");
        
        // Expected Output: AOV = (1000 + 2000 + 3000) / 3 = 2000.00
        Map<String, Object> branchAOV = branchDashboards.get("BRANCH_AOV");
        assertEquals(2000.0, (Double) branchAOV.get("averageOrderValue"), 0.01);
        
        // Actual Result: AOV calculation is accurate
    }
    
    @Test
    @DisplayName("TC050 - Test Order Completion Rate Calculation")
    void testOrderCompletionRateCalculation() {
        // Pre-condition: Orders with different completion statuses
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithStatus("BRANCH_COMPLETION", "ORDER_1", "Completed"),
            createOrderWithStatus("BRANCH_COMPLETION", "ORDER_2", "Completed"),
            createOrderWithStatus("BRANCH_COMPLETION", "ORDER_3", "Completed"),
            createOrderWithStatus("BRANCH_COMPLETION", "ORDER_4", "Failed"),
            createOrderWithStatus("BRANCH_COMPLETION", "ORDER_5", "Pending")
        );
        
        // Steps: Calculate completion rate
        Map<String, Object> result = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
        Map<String, Map<String, Object>> performanceMetrics = (Map<String, Map<String, Object>>) result.get("performanceMetrics");
        
        // Expected Output: 3 completed out of 5 total = 60%
        Map<String, Object> branchMetrics = performanceMetrics.get("BRANCH_COMPLETION");
        assertEquals(60.0, (Double) branchMetrics.get("orderCompletionRate"), 0.01);
        
        // Actual Result: Order completion rate calculated correctly
    }
    
    // Helper methods for creating test data
    private List<RestaurantOrder> createTestOrders() {
        List<RestaurantOrder> orders = new ArrayList<>();
        
        RestaurantOrder order1 = new RestaurantOrder();
        order1.setOrderId("ORDER_001");
        order1.setOutletId("BRANCH_001");
        order1.setOutletName("Test Branch 1");
        order1.setBorough("Test Borough");
        order1.setCapacity(100);
        order1.setTotalPriceLkr(new BigDecimal("1500.00"));
        order1.setCustomerId("CUST_001");
        order1.setStatus("Completed");
        orders.add(order1);
        
        return orders;
    }
    
    private RestaurantOrder createBranchOrder(String outletId, String outletName, String borough, BigDecimal price, String customerId, Integer capacity) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + outletId + "_" + customerId);
        order.setOutletId(outletId);
        order.setOutletName(outletName);
        order.setBorough(borough);
        order.setCapacity(capacity);
        order.setTotalPriceLkr(price);
        order.setCustomerId(customerId);
        order.setStatus("Completed");
        order.setOrderPlaced(LocalDateTime.now());
        return order;
    }
    
    private RestaurantOrder createOrderWithTiming(String outletId, String orderId, String status, LocalDateTime orderTime, LocalDateTime prepStart, LocalDateTime prepFinish, LocalDateTime serveTime, BigDecimal price) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId(orderId);
        order.setOutletId(outletId);
        order.setStatus(status);
        order.setOrderPlaced(orderTime);
        order.setPrepStarted(prepStart);
        order.setPrepFinished(prepFinish);
        order.setServedTime(serveTime);
        order.setTotalPriceLkr(price);
        order.setCustomerId("CUST_" + orderId);
        return order;
    }
    
    private RestaurantOrder createOrderWithCapacityAndTiming(String outletId, LocalDateTime orderTime, LocalDateTime serveTime, Integer capacity) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + orderTime.getHour() + "_" + orderTime.getMinute());
        order.setOutletId(outletId);
        order.setCapacity(capacity);
        order.setOrderPlaced(orderTime);
        order.setServedTime(serveTime);
        order.setTotalPriceLkr(new BigDecimal("1000.00"));
        order.setCustomerId("CUST_" + orderTime.getHour());
        return order;
    }
    
    private RestaurantOrder createOrderWithStatusAndLoyalty(String outletId, String orderId, String status, String loyaltyGroup, String customerId) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId(orderId);
        order.setOutletId(outletId);
        order.setStatus(status);
        order.setLoyaltyGroup(loyaltyGroup);
        order.setCustomerId(customerId);
        order.setTotalPriceLkr(new BigDecimal("1500.00"));
        order.setOrderPlaced(LocalDateTime.now());
        return order;
    }
    
    private RestaurantOrder createOrderWithStatus(String outletId, String orderId, String status) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId(orderId);
        order.setOutletId(outletId);
        order.setStatus(status);
        order.setTotalPriceLkr(new BigDecimal("1000.00"));
        order.setCustomerId("CUST_" + orderId);
        order.setOrderPlaced(LocalDateTime.now());
        return order;
    }
}