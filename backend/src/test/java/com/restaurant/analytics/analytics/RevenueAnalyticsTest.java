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
@DisplayName("Revenue Analytics Test Suite")
public class RevenueAnalyticsTest {
    
    private RevenueAnalytics revenueAnalytics;
    private List<RestaurantOrder> testOrders;
    
    @BeforeEach
    void setUp() {
        revenueAnalytics = new RevenueAnalytics();
        testOrders = createTestOrders();
    }
    
    @Test
    @DisplayName("TC001 - Generate Revenue Analysis with Valid Orders")
    void testGenerateRevenueAnalysisWithValidOrders() {
        // Pre-condition: Valid list of restaurant orders exists
        assertNotNull(testOrders);
        assertFalse(testOrders.isEmpty());
        
        // Steps: Call generateRevenueAnalysis method
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(testOrders);
        
        // Expected Output: Complete revenue analysis with all components
        assertNotNull(result);
        assertTrue(result.containsKey("ticketCounting"));
        assertTrue(result.containsKey("revenueSummary"));
        assertTrue(result.containsKey("dailyRevenue"));
        assertTrue(result.containsKey("monthlyRevenue"));
        assertTrue(result.containsKey("outletRevenue"));
        assertTrue(result.containsKey("paymentMethodAnalysis"));
        assertTrue(result.containsKey("averageOrderValue"));
        
        // Actual Result: All expected keys present in analysis
        assertEquals(7, result.size());
    }
    
    @Test
    @DisplayName("TC002 - Calculate Total Revenue Correctly")
    void testCalculateTotalRevenueCorrectly() {
        // Pre-condition: Orders with known total prices
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithPrice("ORDER1", new BigDecimal("1500.00")),
            createOrderWithPrice("ORDER2", new BigDecimal("2500.00")),
            createOrderWithPrice("ORDER3", new BigDecimal("1000.00"))
        );
        
        // Steps: Generate revenue analysis
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(orders);
        Map<String, Object> revenueSummary = (Map<String, Object>) result.get("revenueSummary");
        
        // Expected Output: Total revenue should be 5000.00
        Double totalRevenue = (Double) revenueSummary.get("reconciledRevenue");
        assertEquals(5000.0, totalRevenue, 0.01);
        
        // Actual Result: Revenue calculation matches expected value
    }
    
    @Test
    @DisplayName("TC003 - Handle Empty Order List")
    void testHandleEmptyOrderList() {
        // Pre-condition: Empty order list
        List<RestaurantOrder> emptyOrders = new ArrayList<>();
        
        // Steps: Generate analysis with empty list
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(emptyOrders);
        
        // Expected Output: Analysis should handle empty list gracefully
        assertNotNull(result);
        Map<String, Object> revenueSummary = (Map<String, Object>) result.get("revenueSummary");
        assertEquals(0.0, (Double) revenueSummary.get("totalRevenue"));
        assertEquals(0.0, (Double) revenueSummary.get("averageOrderValue"));
        
        // Actual Result: Empty list handled without errors
    }
    
    @Test
    @DisplayName("TC004 - Calculate Average Order Value")
    void testCalculateAverageOrderValue() {
        // Pre-condition: Orders with varying prices
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithPrice("ORDER1", new BigDecimal("1000.00")),
            createOrderWithPrice("ORDER2", new BigDecimal("2000.00")),
            createOrderWithPrice("ORDER3", new BigDecimal("3000.00"))
        );
        
        // Steps: Calculate AOV analysis
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(orders);
        Map<String, Object> aovAnalysis = (Map<String, Object>) result.get("averageOrderValue");
        
        // Expected Output: AOV should be 2000.00
        Double overallAOV = (Double) aovAnalysis.get("overallAOV");
        assertEquals(2000.0, overallAOV, 0.01);
        
        // Actual Result: AOV calculation is accurate
    }
    
    @Test
    @DisplayName("TC005 - Group Orders by Payment Method")
    void testGroupOrdersByPaymentMethod() {
        // Pre-condition: Orders with different payment methods
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithPayment("ORDER1", "Credit Card", new BigDecimal("1500.00")),
            createOrderWithPayment("ORDER2", "Cash", new BigDecimal("1000.00")),
            createOrderWithPayment("ORDER3", "Credit Card", new BigDecimal("2000.00"))
        );
        
        // Steps: Analyze payment methods
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(orders);
        Map<String, Object> paymentAnalysis = (Map<String, Object>) result.get("paymentMethodAnalysis");
        Map<String, Long> ordersByPayment = (Map<String, Long>) paymentAnalysis.get("ordersByPaymentMethod");
        
        // Expected Output: 2 Credit Card orders, 1 Cash order
        assertEquals(2L, ordersByPayment.get("Credit Card"));
        assertEquals(1L, ordersByPayment.get("Cash"));
        
        // Actual Result: Payment method grouping works correctly
    }
    
    @Test
    @DisplayName("TC006 - Generate Daily Revenue Breakdown")
    void testGenerateDailyRevenueBreakdown() {
        // Pre-condition: Orders from different days
        LocalDateTime day1 = LocalDateTime.of(2024, 1, 15, 12, 0);
        LocalDateTime day2 = LocalDateTime.of(2024, 1, 16, 12, 0);
        
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithDateTime("ORDER1", day1, new BigDecimal("1500.00")),
            createOrderWithDateTime("ORDER2", day1, new BigDecimal("1000.00")),
            createOrderWithDateTime("ORDER3", day2, new BigDecimal("2000.00"))
        );
        
        // Steps: Generate daily revenue analysis
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(orders);
        Map<String, Double> dailyRevenue = (Map<String, Double>) result.get("dailyRevenue");
        
        // Expected Output: Day 1 = 2500.00, Day 2 = 2000.00
        assertEquals(2500.0, dailyRevenue.get("2024-01-15"), 0.01);
        assertEquals(2000.0, dailyRevenue.get("2024-01-16"), 0.01);
        
        // Actual Result: Daily revenue breakdown is accurate
    }
    
    @Test
    @DisplayName("TC007 - Handle Null Values in Orders")
    void testHandleNullValuesInOrders() {
        // Pre-condition: Orders with null price values
        RestaurantOrder orderWithNullPrice = new RestaurantOrder();
        orderWithNullPrice.setOrderId("ORDER_NULL");
        orderWithNullPrice.setTotalPriceLkr(null);
        orderWithNullPrice.setOutletId("DEFAULT_OUTLET"); // Add outlet ID
        
        List<RestaurantOrder> orders = Arrays.asList(
            orderWithNullPrice,
            createOrderWithPrice("ORDER1", new BigDecimal("1500.00"))
        );
        
        // Steps: Process orders with null values
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(orders);
        
        // Expected Output: Analysis should ignore null values and process valid ones
        assertNotNull(result);
        Map<String, Object> revenueSummary = (Map<String, Object>) result.get("revenueSummary");
        assertEquals(1500.0, (Double) revenueSummary.get("reconciledRevenue"), 0.01);
        
        // Actual Result: Null values handled gracefully
    }
    
    @Test
    @DisplayName("TC008 - Calculate Monthly Revenue Trends")
    void testCalculateMonthlyRevenueTrends() {
        // Pre-condition: Orders from different months
        LocalDateTime jan = LocalDateTime.of(2024, 1, 15, 12, 0);
        LocalDateTime feb = LocalDateTime.of(2024, 2, 15, 12, 0);
        
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithDateTime("ORDER1", jan, new BigDecimal("3000.00")),
            createOrderWithDateTime("ORDER2", feb, new BigDecimal("4000.00"))
        );
        
        // Steps: Generate monthly revenue analysis
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(orders);
        Map<String, Double> monthlyRevenue = (Map<String, Double>) result.get("monthlyRevenue");
        
        // Expected Output: January = 3000.00, February = 4000.00
        assertEquals(3000.0, monthlyRevenue.get("2024-01"), 0.01);
        assertEquals(4000.0, monthlyRevenue.get("2024-02"), 0.01);
        
        // Actual Result: Monthly revenue trends calculated correctly
    }
    
    @Test
    @DisplayName("TC009 - Analyze Revenue by Outlet")
    void testAnalyzeRevenueByOutlet() {
        // Pre-condition: Orders from different outlets
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithOutlet("ORDER1", "OUTLET_A", new BigDecimal("2000.00")),
            createOrderWithOutlet("ORDER2", "OUTLET_B", new BigDecimal("1500.00")),
            createOrderWithOutlet("ORDER3", "OUTLET_A", new BigDecimal("1000.00"))
        );
        
        // Steps: Analyze outlet revenue
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(orders);
        Map<String, Object> outletRevenue = (Map<String, Object>) result.get("outletRevenue");
        
        // Expected Output: Outlet A = 3000.00, Outlet B = 1500.00
        Map<String, Object> outletAData = (Map<String, Object>) outletRevenue.get("OUTLET_A");
        Map<String, Object> outletBData = (Map<String, Object>) outletRevenue.get("OUTLET_B");
        
        assertEquals(3000.0, (Double) outletAData.get("revenue"), 0.01);
        assertEquals(1500.0, (Double) outletBData.get("revenue"), 0.01);
        
        // Actual Result: Outlet revenue analysis is accurate
    }
    
    @Test
    @DisplayName("TC010 - Calculate Ticket Counting Metrics")
    void testCalculateTicketCountingMetrics() {
        // Pre-condition: Orders with different statuses and item counts
        List<RestaurantOrder> orders = Arrays.asList(
            createOrderWithStatus("ORDER1", "Completed", 3),
            createOrderWithStatus("ORDER2", "Pending", 2),
            createOrderWithStatus("ORDER3", "Completed", 4)
        );
        
        // Steps: Generate ticket counting analysis
        Map<String, Object> result = revenueAnalytics.generateRevenueAnalysis(orders);
        Map<String, Object> ticketCounting = (Map<String, Object>) result.get("ticketCounting");
        
        // Expected Output: 3 total orders, average 3 items per order
        assertEquals(3L, (Long) ticketCounting.get("totalOrders"));
        assertEquals(3.0, (Double) ticketCounting.get("averageItemsPerOrder"), 0.01);
        
        Map<String, Long> ordersByStatus = (Map<String, Long>) ticketCounting.get("ordersByStatus");
        assertEquals(2L, ordersByStatus.get("Completed"));
        assertEquals(1L, ordersByStatus.get("Pending"));
        
        // Actual Result: Ticket counting metrics are accurate
    }
    
    // Helper methods for creating test data
    private List<RestaurantOrder> createTestOrders() {
        List<RestaurantOrder> orders = new ArrayList<>();
        
        RestaurantOrder order1 = new RestaurantOrder();
        order1.setOrderId("ORDER_001");
        order1.setCustomerId("CUST_001");
        order1.setOutletId("OUTLET_001");
        order1.setTotalPriceLkr(new BigDecimal("1500.00"));
        order1.setPaymentMethod("Credit Card");
        order1.setStatus("Completed");
        order1.setNumItems(3);
        order1.setOrderPlaced(LocalDateTime.now().minusDays(1));
        orders.add(order1);
        
        RestaurantOrder order2 = new RestaurantOrder();
        order2.setOrderId("ORDER_002");
        order2.setCustomerId("CUST_002");
        order2.setOutletId("OUTLET_002");
        order2.setTotalPriceLkr(new BigDecimal("2500.00"));
        order2.setPaymentMethod("Cash");
        order2.setStatus("Completed");
        order2.setNumItems(5);
        order2.setOrderPlaced(LocalDateTime.now().minusDays(2));
        orders.add(order2);
        
        return orders;
    }
    
    private RestaurantOrder createOrderWithPrice(String orderId, BigDecimal price) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId(orderId);
        order.setTotalPriceLkr(price);
        order.setOrderPlaced(LocalDateTime.now());
        order.setOutletId("DEFAULT_OUTLET"); // Add default outlet ID
        return order;
    }
    
    private RestaurantOrder createOrderWithPayment(String orderId, String paymentMethod, BigDecimal price) {
        RestaurantOrder order = createOrderWithPrice(orderId, price);
        order.setPaymentMethod(paymentMethod);
        order.setOutletId("DEFAULT_OUTLET"); // Add default outlet ID
        return order;
    }
    
    private RestaurantOrder createOrderWithDateTime(String orderId, LocalDateTime dateTime, BigDecimal price) {
        RestaurantOrder order = createOrderWithPrice(orderId, price);
        order.setOrderPlaced(dateTime);
        order.setOutletId("DEFAULT_OUTLET"); // Add default outlet ID
        return order;
    }
    
    private RestaurantOrder createOrderWithOutlet(String orderId, String outletId, BigDecimal price) {
        RestaurantOrder order = createOrderWithPrice(orderId, price);
        order.setOutletId(outletId);
        return order;
    }
    
    private RestaurantOrder createOrderWithStatus(String orderId, String status, int numItems) {
        RestaurantOrder order = new RestaurantOrder();
        order.setOrderId(orderId);
        order.setStatus(status);
        order.setNumItems(numItems);
        order.setTotalPriceLkr(new BigDecimal("1000.00"));
        order.setOrderPlaced(LocalDateTime.now());
        order.setOutletId("DEFAULT_OUTLET"); // Add default outlet ID
        return order;
    }
}