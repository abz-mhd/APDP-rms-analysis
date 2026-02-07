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
@DisplayName("Peak Dining Analytics Test Suite")
public class PeakDiningAnalyticsTest {
    
    private PeakDiningAnalytics peakDiningAnalytics;
    private List<RestaurantOrder> testOrders;
    
    @BeforeEach
    void setUp() {
        peakDiningAnalytics = new PeakDiningAnalytics();
        testOrders = createTestOrders();
    }
    
    @Test
    @DisplayName("TC031 - Generate Complete Peak Dining Analysis")
    void testGenerateCompletePeakDiningAnalysis() {
        // Pre-condition: Valid orders with time and outlet data
        assertNotNull(testOrders);
        assertFalse(testOrders.isEmpty());
        
        // Steps: Generate peak dining analysis
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(testOrders);
        
        // Expected Output: Complete analysis with all time-based components
        assertNotNull(result);
        assertTrue(result.containsKey("hourlyHeatmap"));
        assertTrue(result.containsKey("peakHourTables"));
        assertTrue(result.containsKey("branchSummaries"));
        assertTrue(result.containsKey("dailyPatterns"));
        assertTrue(result.containsKey("weeklyPatterns"));
        
        // Actual Result: All peak dining analysis components present
        assertEquals(5, result.size());
    }
    
    @Test
    @DisplayName("TC032 - Generate Hourly Heatmap Data")
    void testGenerateHourlyHeatmapData() {
        // Pre-condition: Orders at different hours and outlets
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithHourAndOutlet(12, "OUTLET_A"), // Lunch hour
            createOrderWithHourAndOutlet(12, "OUTLET_A"), // Same hour, same outlet
            createOrderWithHourAndOutlet(19, "OUTLET_A"), // Dinner hour
            createOrderWithHourAndOutlet(12, "OUTLET_B"), // Lunch hour, different outlet
            createOrderWithHourAndOutlet(20, "OUTLET_B")  // Evening hour
        );
        
        // Steps: Generate hourly heatmap
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
        Map<String, Map<Integer, Long>> hourlyHeatmap = (Map<String, Map<Integer, Long>>) result.get("hourlyHeatmap");
        
        // Expected Output: Correct hour-outlet distribution
        assertNotNull(hourlyHeatmap);
        assertEquals(2L, hourlyHeatmap.get("OUTLET_A").get(12)); // 2 orders at hour 12
        assertEquals(1L, hourlyHeatmap.get("OUTLET_A").get(19)); // 1 order at hour 19
        assertEquals(1L, hourlyHeatmap.get("OUTLET_B").get(12)); // 1 order at hour 12
        assertEquals(1L, hourlyHeatmap.get("OUTLET_B").get(20)); // 1 order at hour 20
        
        // Actual Result: Hourly heatmap data structured correctly
    }
    
    @Test
    @DisplayName("TC033 - Identify Peak Hours Correctly")
    void testIdentifyPeakHoursCorrectly() {
        // Pre-condition: Orders concentrated at specific hours
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithHour(12), // Lunch peak
            createOrderWithHour(12),
            createOrderWithHour(12),
            createOrderWithHour(19), // Dinner peak
            createOrderWithHour(19),
            createOrderWithHour(14), // Off-peak
            createOrderWithHour(20)  // Late dinner
        );
        
        // Steps: Identify peak hours
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
        Map<String, Object> peakHourTables = (Map<String, Object>) result.get("peakHourTables");
        List<Map<String, Object>> overallPeakHours = (List<Map<String, Object>>) peakHourTables.get("overallPeakHours");
        
        // Expected Output: Hour 12 should be top peak (3 orders), hour 19 second (2 orders)
        assertNotNull(overallPeakHours);
        assertFalse(overallPeakHours.isEmpty());
        
        Map<String, Object> topPeakHour = overallPeakHours.get(0);
        assertEquals(12, topPeakHour.get("hour"));
        assertEquals(3L, topPeakHour.get("orderCount"));
        assertEquals("12:00 - 12:59", topPeakHour.get("timeRange"));
        
        // Actual Result: Peak hours identified and ranked correctly
    }
    
    @Test
    @DisplayName("TC034 - Generate Branch Performance Summaries")
    void testGenerateBranchPerformanceSummaries() {
        // Pre-condition: Orders from multiple branches with complete data
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithBranchDetails("OUTLET_A", "Branch A", "Downtown", new BigDecimal("1500.00"), "CUST_1"),
            createOrderWithBranchDetails("OUTLET_A", "Branch A", "Downtown", new BigDecimal("2000.00"), "CUST_2"),
            createOrderWithBranchDetails("OUTLET_B", "Branch B", "Uptown", new BigDecimal("1200.00"), "CUST_3"),
            createOrderWithBranchDetails("OUTLET_B", "Branch B", "Uptown", new BigDecimal("1800.00"), "CUST_1")
        );
        
        // Steps: Generate branch summaries
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
        Map<String, Map<String, Object>> branchSummaries = (Map<String, Map<String, Object>>) result.get("branchSummaries");
        
        // Expected Output: Comprehensive branch performance data
        assertNotNull(branchSummaries);
        
        Map<String, Object> branchA = branchSummaries.get("OUTLET_A");
        assertEquals(2, branchA.get("totalOrders"));
        assertEquals(3500.0, (Double) branchA.get("totalRevenue"), 0.01);
        assertEquals(1750.0, (Double) branchA.get("averageOrderValue"), 0.01);
        assertEquals(2L, branchA.get("uniqueCustomers"));
        assertEquals("Branch A", branchA.get("outletName"));
        assertEquals("Downtown", branchA.get("borough"));
        
        // Actual Result: Branch summaries provide comprehensive metrics
    }
    
    @Test
    @DisplayName("TC035 - Analyze Daily Patterns")
    void testAnalyzeDailyPatterns() {
        // Pre-condition: Orders from different days of the week
        LocalDateTime monday = LocalDateTime.of(2024, 1, 15, 12, 0); // Monday
        LocalDateTime tuesday = LocalDateTime.of(2024, 1, 16, 12, 0); // Tuesday
        LocalDateTime wednesday = LocalDateTime.of(2024, 1, 17, 12, 0); // Wednesday
        
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithDateTime(monday),
            createOrderWithDateTime(monday),
            createOrderWithDateTime(tuesday),
            createOrderWithDateTime(wednesday),
            createOrderWithDateTime(wednesday),
            createOrderWithDateTime(wednesday)
        );
        
        // Steps: Analyze daily patterns
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
        Map<String, Long> dailyPatterns = (Map<String, Long>) result.get("dailyPatterns");
        
        // Expected Output: Monday = 2, Tuesday = 1, Wednesday = 3 orders
        assertEquals(2L, dailyPatterns.get("MONDAY"));
        assertEquals(1L, dailyPatterns.get("TUESDAY"));
        assertEquals(3L, dailyPatterns.get("WEDNESDAY"));
        
        // Actual Result: Daily patterns calculated accurately
    }
    
    @Test
    @DisplayName("TC036 - Generate Weekly Patterns by Outlet")
    void testGenerateWeeklyPatternsByOutlet() {
        // Pre-condition: Orders from different weeks and outlets
        LocalDateTime week1 = LocalDateTime.of(2024, 1, 15, 12, 0); // Week 3 of 2024
        LocalDateTime week2 = LocalDateTime.of(2024, 1, 22, 12, 0); // Week 4 of 2024
        
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithDateTimeAndOutlet(week1, "OUTLET_A"),
            createOrderWithDateTimeAndOutlet(week1, "OUTLET_A"),
            createOrderWithDateTimeAndOutlet(week2, "OUTLET_A"),
            createOrderWithDateTimeAndOutlet(week1, "OUTLET_B"),
            createOrderWithDateTimeAndOutlet(week2, "OUTLET_B"),
            createOrderWithDateTimeAndOutlet(week2, "OUTLET_B")
        );
        
        // Steps: Generate weekly patterns
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
        Map<String, Map<String, Long>> weeklyPatterns = (Map<String, Map<String, Long>>) result.get("weeklyPatterns");
        
        // Expected Output: Weekly distribution by outlet
        assertNotNull(weeklyPatterns);
        assertTrue(weeklyPatterns.containsKey("OUTLET_A"));
        assertTrue(weeklyPatterns.containsKey("OUTLET_B"));
        
        Map<String, Long> outletAWeeks = weeklyPatterns.get("OUTLET_A");
        Map<String, Long> outletBWeeks = weeklyPatterns.get("OUTLET_B");
        
        // Verify week patterns exist
        assertFalse(outletAWeeks.isEmpty());
        assertFalse(outletBWeeks.isEmpty());
        
        // Actual Result: Weekly patterns tracked by outlet
    }
    
    @Test
    @DisplayName("TC037 - Handle Peak Hours with No Orders")
    void testHandlePeakHoursWithNoOrders() {
        // Pre-condition: Empty order list
        List<RestaurantOrder> emptyOrders = new ArrayList<>();
        
        // Steps: Generate analysis with no orders
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(emptyOrders);
        
        // Expected Output: Analysis should handle empty data gracefully
        assertNotNull(result);
        Map<String, Map<Integer, Long>> hourlyHeatmap = (Map<String, Map<Integer, Long>>) result.get("hourlyHeatmap");
        Map<String, Object> peakHourTables = (Map<String, Object>) result.get("peakHourTables");
        
        assertTrue(hourlyHeatmap.isEmpty());
        assertNotNull(peakHourTables);
        
        // Actual Result: Empty data handled without errors
    }
    
    @Test
    @DisplayName("TC038 - Calculate Peak Hours by Individual Outlet")
    void testCalculatePeakHoursByIndividualOutlet() {
        // Pre-condition: Different peak hours for different outlets
        List<RestaurantOrder> orders = Arrays.asList(
            // Outlet A peaks at hour 12
            createOrderWithHourAndOutlet(12, "OUTLET_A"),
            createOrderWithHourAndOutlet(12, "OUTLET_A"),
            createOrderWithHourAndOutlet(12, "OUTLET_A"),
            createOrderWithHourAndOutlet(19, "OUTLET_A"),
            // Outlet B peaks at hour 19
            createOrderWithHourAndOutlet(19, "OUTLET_B"),
            createOrderWithHourAndOutlet(19, "OUTLET_B"),
            createOrderWithHourAndOutlet(19, "OUTLET_B"),
            createOrderWithHourAndOutlet(12, "OUTLET_B")
        );
        
        // Steps: Analyze outlet-specific peak hours
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
        Map<String, Object> peakHourTables = (Map<String, Object>) result.get("peakHourTables");
        Map<String, List<Map<String, Object>>> outletPeakHours = (Map<String, List<Map<String, Object>>>) peakHourTables.get("outletPeakHours");
        
        // Expected Output: Different peak hours for each outlet
        assertNotNull(outletPeakHours);
        
        List<Map<String, Object>> outletAPeaks = outletPeakHours.get("OUTLET_A");
        List<Map<String, Object>> outletBPeaks = outletPeakHours.get("OUTLET_B");
        
        assertNotNull(outletAPeaks);
        assertNotNull(outletBPeaks);
        
        // Outlet A's top peak should be hour 12
        Map<String, Object> outletATopPeak = outletAPeaks.get(0);
        assertEquals(12, outletATopPeak.get("hour"));
        assertEquals(3L, outletATopPeak.get("orderCount"));
        
        // Outlet B's top peak should be hour 19
        Map<String, Object> outletBTopPeak = outletBPeaks.get(0);
        assertEquals(19, outletBTopPeak.get("hour"));
        assertEquals(3L, outletBTopPeak.get("orderCount"));
        
        // Actual Result: Outlet-specific peak hours identified correctly
    }
    
    @Test
    @DisplayName("TC039 - Validate Branch Summary Peak Hour Detection")
    void testValidateBranchSummaryPeakHourDetection() {
        // Pre-condition: Orders with clear peak hour pattern for a branch
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithHourAndOutlet(13, "OUTLET_TEST"), // Peak hour
            createOrderWithHourAndOutlet(13, "OUTLET_TEST"),
            createOrderWithHourAndOutlet(13, "OUTLET_TEST"),
            createOrderWithHourAndOutlet(13, "OUTLET_TEST"),
            createOrderWithHourAndOutlet(18, "OUTLET_TEST"), // Secondary hour
            createOrderWithHourAndOutlet(18, "OUTLET_TEST")
        );
        
        // Steps: Check branch summary peak hour detection
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
        Map<String, Map<String, Object>> branchSummaries = (Map<String, Map<String, Object>>) result.get("branchSummaries");
        
        // Expected Output: Branch summary should identify hour 13 as peak
        Map<String, Object> testOutletSummary = branchSummaries.get("OUTLET_TEST");
        assertNotNull(testOutletSummary);
        assertEquals(13, testOutletSummary.get("peakHour"));
        assertEquals(4L, testOutletSummary.get("peakHourOrders"));
        
        // Actual Result: Peak hour detection in branch summary is accurate
    }
    
    @Test
    @DisplayName("TC040 - Handle Orders with Null DateTime Values")
    void testHandleOrdersWithNullDateTimeValues() {
        // Pre-condition: Mix of orders with and without datetime
        RestaurantOrder orderWithNullTime = new RestaurantOrder();
        orderWithNullTime.setOrderId("ORDER_NULL_TIME");
        orderWithNullTime.setOrderPlaced(null);
        orderWithNullTime.setOutletId("OUTLET_A");
        orderWithNullTime.setTotalPriceLkr(new BigDecimal("1000.00"));
        
        List<RestaurantOrder> orders = Arrays.asList(
            orderWithNullTime,
            createOrderWithHour(12),
            createOrderWithHour(13)
        );
        
        // Steps: Generate analysis with null datetime values
        Map<String, Object> result = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
        
        // Expected Output: Analysis should ignore null datetime and process valid ones
        assertNotNull(result);
        Map<String, Map<Integer, Long>> hourlyHeatmap = (Map<String, Map<Integer, Long>>) result.get("hourlyHeatmap");
        
        // Should only contain entries for valid datetime orders
        assertFalse(hourlyHeatmap.isEmpty());
        
        // Actual Result: Null datetime values handled gracefully
    }
    
    // Helper methods for creating test data
    private List<RestaurantOrder> createTestOrders() {
        List<RestaurantOrder> orders = new ArrayList<>();
        
        RestaurantOrder order1 = new RestaurantOrder();
        order1.setOrderId("ORDER_001");
        order1.setOutletId("OUTLET_001");
        order1.setOrderPlaced(LocalDateTime.of(2024, 1, 15, 12, 30));
        order1.setTotalPriceLkr(new BigDecimal("1500.00"));
        order1.setCustomerId("CUST_001");
        orders.add(order1);
        
        RestaurantOrder order2 = new RestaurantOrder();
        order2.setOrderId("ORDER_002");
        order2.setOutletId("OUTLET_002");
        order2.setOrderPlaced(LocalDateTime.of(2024, 1, 15, 19, 45));
        order2.setTotalPriceLkr(new BigDecimal("2000.00"));
        order2.setCustomerId("CUST_002");
        orders.add(order2);
        
        return orders;
    }
    
    private RestaurantOrder createOrderWithHour(int hour) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_HOUR_" + hour);
        order.setOrderPlaced(LocalDateTime.of(2024, 1, 15, hour, 0));
        order.setOutletId("OUTLET_DEFAULT");
        order.setTotalPriceLkr(new BigDecimal("1000.00"));
        return order;
    }
    
    private RestaurantOrder createOrderWithHourAndOutlet(int hour, String outletId) {
        RestaurantOrder order = createOrderWithHour(hour);
        order.setOutletId(outletId);
        order.setOrderId("ORDER_" + outletId + "_" + hour);
        return order;
    }
    
    private RestaurantOrder createOrderWithBranchDetails(String outletId, String outletName, String borough, BigDecimal price, String customerId) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + outletId + "_" + customerId);
        order.setOutletId(outletId);
        order.setOutletName(outletName);
        order.setBorough(borough);
        order.setTotalPriceLkr(price);
        order.setCustomerId(customerId);
        order.setOrderPlaced(LocalDateTime.of(2024, 1, 15, 12, 0));
        return order;
    }
    
    private RestaurantOrder createOrderWithDateTime(LocalDateTime dateTime) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId("ORDER_" + dateTime.getDayOfYear());
        order.setOrderPlaced(dateTime);
        order.setOutletId("OUTLET_DEFAULT");
        order.setTotalPriceLkr(new BigDecimal("1000.00"));
        return order;
    }
    
    private RestaurantOrder createOrderWithDateTimeAndOutlet(LocalDateTime dateTime, String outletId) {
        RestaurantOrder order = createOrderWithDateTime(dateTime);
        order.setOutletId(outletId);
        order.setOrderId("ORDER_" + outletId + "_" + dateTime.getDayOfYear());
        return order;
    }
}