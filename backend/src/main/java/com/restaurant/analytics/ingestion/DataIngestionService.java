package com.restaurant.analytics.ingestion;

import com.restaurant.analytics.model.RestaurantOrder;
import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvException;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@Service
public class DataIngestionService {
    
    private static final int CHUNK_SIZE = 1000;
    private final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss");
    
    public CompletableFuture<List<RestaurantOrder>> ingestCsvFile(String filePath) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return processCsvFile(filePath);
            } catch (Exception e) {
                throw new RuntimeException("Failed to ingest CSV file: " + filePath, e);
            }
        });
    }
    
    public CompletableFuture<List<RestaurantOrder>> ingestCsvFile(MultipartFile file) {
        return CompletableFuture.supplyAsync(() -> {
            try (InputStream inputStream = file.getInputStream()) {
                return processCsvStream(inputStream);
            } catch (Exception e) {
                throw new RuntimeException("Failed to ingest uploaded CSV file", e);
            }
        });
    }
    
    private List<RestaurantOrder> processCsvFile(String filePath) throws IOException, CsvException {
        try (FileReader fileReader = new FileReader(filePath);
             CSVReader csvReader = new CSVReader(fileReader)) {
            
            return processChunkedData(csvReader);
        }
    }
    
    private List<RestaurantOrder> processCsvStream(InputStream inputStream) throws IOException, CsvException {
        try (InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
             CSVReader csvReader = new CSVReader(inputStreamReader)) {
            
            return processChunkedData(csvReader);
        }
    }
    
    private List<RestaurantOrder> processChunkedData(CSVReader csvReader) throws IOException, CsvException {
        List<RestaurantOrder> allOrders = new ArrayList<>();
        List<String[]> chunk = new ArrayList<>();
        
        // Skip header
        csvReader.readNext();
        
        String[] line;
        while ((line = csvReader.readNext()) != null) {
            chunk.add(line);
            
            if (chunk.size() >= CHUNK_SIZE) {
                allOrders.addAll(processChunk(chunk));
                chunk.clear();
            }
        }
        
        // Process remaining chunk
        if (!chunk.isEmpty()) {
            allOrders.addAll(processChunk(chunk));
        }
        
        return allOrders;
    }
    
    private List<RestaurantOrder> processChunk(List<String[]> chunk) {
        List<RestaurantOrder> orders = new ArrayList<>();
        
        for (String[] row : chunk) {
            try {
                RestaurantOrder order = mapRowToOrder(row);
                orders.add(order);
            } catch (Exception e) {
                // Log error and continue processing (dead-letter queue logic can be added here)
                System.err.println("Failed to process row: " + String.join(",", row) + " - " + e.getMessage());
            }
        }
        
        return orders;
    }
    
    private RestaurantOrder mapRowToOrder(String[] row) {
        RestaurantOrder order = new RestaurantOrder();
        
        // Map CSV columns to order fields
        order.setOrderId(row[0]);
        order.setCustomerId(row[1]);
        order.setOutletId(row[2]);
        order.setOrderPlaced(parseDateTime(row[3]));
        order.setOrderConfirmed(parseDateTime(row[4]));
        order.setPrepStarted(parseDateTime(row[5]));
        order.setPrepFinished(parseDateTime(row[6]));
        order.setServedTime(parseDateTime(row[7]));
        order.setStatus(row[8]);
        order.setNumItems(parseInt(row[9]));
        order.setTotalPriceLkr(parseBigDecimal(row[10]));
        order.setPaymentMethod(row[11]);
        order.setItemId(row[12]);
        order.setQuantity(parseInt(row[13]));
        order.setItemPriceLkr(parseBigDecimal(row[14]));
        order.setCustomerName(row[15]);
        order.setContactNo(row[16]);
        order.setGender(row[17]);
        order.setAge(parseInt(row[18]));
        order.setJoinDate(parseDateTime(row[19]));
        order.setLoyaltyGroup(row[20]);
        order.setEstimatedTotalSpentLkr(parseBigDecimal(row[21]));
        order.setOutletName(row[22]);
        order.setBorough(row[23]);
        order.setCapacity(parseInt(row[24]));
        order.setOpened(parseDateTime(row[25]));
        order.setMenuItemName(row[26]);
        order.setCategory(row[27]);
        order.setItemPriceLkr(parseBigDecimal(row[28]));
        order.setIsVegetarian(parseBoolean(row[29]));
        order.setSpiceLevel(row[30]);
        
        return order;
    }
    
    private LocalDateTime parseDateTime(String dateStr) {
        if (dateStr == null || dateStr.trim().isEmpty()) {
            return null;
        }
        return LocalDateTime.parse(dateStr, formatter);
    }
    
    private Integer parseInt(String intStr) {
        if (intStr == null || intStr.trim().isEmpty()) {
            return null;
        }
        return Integer.parseInt(intStr);
    }
    
    private BigDecimal parseBigDecimal(String decimalStr) {
        if (decimalStr == null || decimalStr.trim().isEmpty()) {
            return null;
        }
        return new BigDecimal(decimalStr);
    }
    
    private Boolean parseBoolean(String boolStr) {
        if (boolStr == null || boolStr.trim().isEmpty()) {
            return null;
        }
        return Boolean.parseBoolean(boolStr);
    }
}