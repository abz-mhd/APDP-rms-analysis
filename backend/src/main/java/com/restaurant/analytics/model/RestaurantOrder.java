package com.restaurant.analytics.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.math.BigDecimal;

@Entity
@Table(name = "restaurant_orders")
public class RestaurantOrder {
    @Id
    private String orderId;
    
    private String customerId;
    private String outletId;
    private LocalDateTime orderPlaced;
    private LocalDateTime orderConfirmed;
    private LocalDateTime prepStarted;
    private LocalDateTime prepFinished;
    private LocalDateTime servedTime;
    private String status;
    private Integer numItems;
    private BigDecimal totalPriceLkr;
    private String paymentMethod;
    
    // Item details
    private String itemId;
    private Integer quantity;
    private BigDecimal itemPriceLkr;
    
    // Customer details
    private String customerName;
    private String contactNo;
    private String gender;
    private Integer age;
    private LocalDateTime joinDate;
    private String loyaltyGroup;
    private BigDecimal estimatedTotalSpentLkr;
    
    // Outlet details
    private String outletName;
    private String borough;
    private Integer capacity;
    private LocalDateTime opened;
    
    // Menu item details
    private String menuItemName;
    private String category;
    private Boolean isVegetarian;
    private String spiceLevel;

    // Constructors
    public RestaurantOrder() {}

    // Getters and Setters
    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }

    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }

    public String getOutletId() { return outletId; }
    public void setOutletId(String outletId) { this.outletId = outletId; }

    public LocalDateTime getOrderPlaced() { return orderPlaced; }
    public void setOrderPlaced(LocalDateTime orderPlaced) { this.orderPlaced = orderPlaced; }

    public LocalDateTime getOrderConfirmed() { return orderConfirmed; }
    public void setOrderConfirmed(LocalDateTime orderConfirmed) { this.orderConfirmed = orderConfirmed; }

    public LocalDateTime getPrepStarted() { return prepStarted; }
    public void setPrepStarted(LocalDateTime prepStarted) { this.prepStarted = prepStarted; }

    public LocalDateTime getPrepFinished() { return prepFinished; }
    public void setPrepFinished(LocalDateTime prepFinished) { this.prepFinished = prepFinished; }

    public LocalDateTime getServedTime() { return servedTime; }
    public void setServedTime(LocalDateTime servedTime) { this.servedTime = servedTime; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Integer getNumItems() { return numItems; }
    public void setNumItems(Integer numItems) { this.numItems = numItems; }

    public BigDecimal getTotalPriceLkr() { return totalPriceLkr; }
    public void setTotalPriceLkr(BigDecimal totalPriceLkr) { this.totalPriceLkr = totalPriceLkr; }

    public String getPaymentMethod() { return paymentMethod; }
    public void setPaymentMethod(String paymentMethod) { this.paymentMethod = paymentMethod; }

    public String getItemId() { return itemId; }
    public void setItemId(String itemId) { this.itemId = itemId; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public BigDecimal getItemPriceLkr() { return itemPriceLkr; }
    public void setItemPriceLkr(BigDecimal itemPriceLkr) { this.itemPriceLkr = itemPriceLkr; }

    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }

    public String getContactNo() { return contactNo; }
    public void setContactNo(String contactNo) { this.contactNo = contactNo; }

    public String getGender() { return gender; }
    public void setGender(String gender) { this.gender = gender; }

    public Integer getAge() { return age; }
    public void setAge(Integer age) { this.age = age; }

    public LocalDateTime getJoinDate() { return joinDate; }
    public void setJoinDate(LocalDateTime joinDate) { this.joinDate = joinDate; }

    public String getLoyaltyGroup() { return loyaltyGroup; }
    public void setLoyaltyGroup(String loyaltyGroup) { this.loyaltyGroup = loyaltyGroup; }

    public BigDecimal getEstimatedTotalSpentLkr() { return estimatedTotalSpentLkr; }
    public void setEstimatedTotalSpentLkr(BigDecimal estimatedTotalSpentLkr) { this.estimatedTotalSpentLkr = estimatedTotalSpentLkr; }

    public String getOutletName() { return outletName; }
    public void setOutletName(String outletName) { this.outletName = outletName; }

    public String getBorough() { return borough; }
    public void setBorough(String borough) { this.borough = borough; }

    public Integer getCapacity() { return capacity; }
    public void setCapacity(Integer capacity) { this.capacity = capacity; }

    public LocalDateTime getOpened() { return opened; }
    public void setOpened(LocalDateTime opened) { this.opened = opened; }

    public String getMenuItemName() { return menuItemName; }
    public void setMenuItemName(String menuItemName) { this.menuItemName = menuItemName; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public Boolean getIsVegetarian() { return isVegetarian; }
    public void setIsVegetarian(Boolean isVegetarian) { this.isVegetarian = isVegetarian; }

    public String getSpiceLevel() { return spiceLevel; }
    public void setSpiceLevel(String spiceLevel) { this.spiceLevel = spiceLevel; }
}