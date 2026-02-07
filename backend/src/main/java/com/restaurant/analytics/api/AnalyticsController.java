package com.restaurant.analytics.api;

import com.restaurant.analytics.analytics.*;
import com.restaurant.analytics.ingestion.DataIngestionService;
import com.restaurant.analytics.model.RestaurantOrder;
import com.restaurant.analytics.transform.DataTransformationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/api/analytics")
@CrossOrigin(origins = "*")
public class AnalyticsController {
    
    @Autowired
    private DataIngestionService ingestionService;
    
    @Autowired
    private DataTransformationService transformationService;
    
    @Autowired
    private PeakDiningAnalytics peakDiningAnalytics;
    
    @Autowired
    private CustomerAnalytics customerAnalytics;
    
    @Autowired
    private MenuAnalytics menuAnalytics;
    
    @Autowired
    private RevenueAnalytics revenueAnalytics;
    
    @Autowired
    private AnomalyDetectionService anomalyDetectionService;
    
    @Autowired
    private BranchPerformanceAnalytics branchPerformanceAnalytics;
    
    @PostMapping("/ingest/csv")
    public CompletableFuture<ResponseEntity<Map<String, Object>>> ingestCsvFile(@RequestParam("file") MultipartFile file) {
        return ingestionService.ingestCsvFile(file)
                .thenApply(orders -> {
                    Map<String, Object> response = Map.of(
                        "status", "success",
                        "message", "Data ingested successfully",
                        "recordCount", orders.size()
                    );
                    return ResponseEntity.ok(response);
                })
                .exceptionally(throwable -> {
                    Map<String, Object> response = Map.of(
                        "status", "error",
                        "message", throwable.getMessage()
                    );
                    return ResponseEntity.badRequest().body(response);
                });
    }
    
    @GetMapping("/peak-dining")
    public ResponseEntity<Map<String, Object>> getPeakDiningAnalysis(
            @RequestParam(required = false) String outletId,
            @RequestParam(required = false) String season,
            @RequestParam(required = false) String festival) {
        
        try {
            List<RestaurantOrder> orders = loadDataFromFile();
            orders = transformationService.cleanAndValidateData(orders);
            
            // Apply filters
            if (outletId != null) {
                orders = orders.stream()
                        .filter(order -> outletId.equals(order.getOutletId()))
                        .collect(java.util.stream.Collectors.toList());
            }
            
            if (season != null) {
                orders = transformationService.filterBySeason(orders, season);
            }
            
            if (festival != null) {
                orders = transformationService.filterByFestival(orders, festival);
            }
            
            Map<String, Object> analysis = peakDiningAnalytics.generatePeakDiningAnalysis(orders);
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }  
  
    @GetMapping("/customer-demographics")
    public ResponseEntity<Map<String, Object>> getCustomerDemographics(
            @RequestParam(required = false) String outletId,
            @RequestParam(required = false) String season) {
        
        try {
            List<RestaurantOrder> orders = loadDataFromFile();
            orders = transformationService.cleanAndValidateData(orders);
            
            if (outletId != null) {
                orders = orders.stream()
                        .filter(order -> outletId.equals(order.getOutletId()))
                        .collect(java.util.stream.Collectors.toList());
            }
            
            if (season != null) {
                orders = transformationService.filterBySeason(orders, season);
            }
            
            Map<String, Object> analysis = customerAnalytics.generateCustomerDemographicsAnalysis(orders);
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/customer-seasonal")
    public ResponseEntity<Map<String, Object>> getCustomerSeasonalBehavior(
            @RequestParam(required = false) String outletId) {
        
        try {
            List<RestaurantOrder> orders = loadDataFromFile();
            orders = transformationService.cleanAndValidateData(orders);
            
            if (outletId != null) {
                orders = orders.stream()
                        .filter(order -> outletId.equals(order.getOutletId()))
                        .collect(java.util.stream.Collectors.toList());
            }
            
            Map<String, Object> analysis = customerAnalytics.generateSeasonalBehaviorAnalysis(orders);
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/menu-analysis")
    public ResponseEntity<Map<String, Object>> getMenuAnalysis(
            @RequestParam(required = false) String outletId,
            @RequestParam(required = false) String category) {
        
        try {
            List<RestaurantOrder> orders = loadDataFromFile();
            orders = transformationService.cleanAndValidateData(orders);
            
            if (outletId != null) {
                orders = orders.stream()
                        .filter(order -> outletId.equals(order.getOutletId()))
                        .collect(java.util.stream.Collectors.toList());
            }
            
            if (category != null) {
                orders = orders.stream()
                        .filter(order -> category.equals(order.getCategory()))
                        .collect(java.util.stream.Collectors.toList());
            }
            
            Map<String, Object> analysis = menuAnalytics.generateMenuAnalysis(orders);
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/revenue-analysis")
    public ResponseEntity<Map<String, Object>> getRevenueAnalysis(
            @RequestParam(required = false) String outletId,
            @RequestParam(required = false) String timeWindow) {
        
        try {
            List<RestaurantOrder> orders = loadDataFromFile();
            orders = transformationService.cleanAndValidateData(orders);
            
            if (outletId != null) {
                orders = orders.stream()
                        .filter(order -> outletId.equals(order.getOutletId()))
                        .collect(java.util.stream.Collectors.toList());
            }
            
            Map<String, Object> analysis = revenueAnalytics.generateRevenueAnalysis(orders);
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/anomaly-detection")
    public ResponseEntity<Map<String, Object>> getAnomalyDetection(
            @RequestParam(required = false) String outletId) {
        
        try {
            List<RestaurantOrder> orders = loadDataFromFile();
            orders = transformationService.cleanAndValidateData(orders);
            
            if (outletId != null) {
                orders = orders.stream()
                        .filter(order -> outletId.equals(order.getOutletId()))
                        .collect(java.util.stream.Collectors.toList());
            }
            
            Map<String, Object> analysis = anomalyDetectionService.detectServiceAnomalies(orders);
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/branch-performance")
    public ResponseEntity<Map<String, Object>> getBranchPerformance(
            @RequestParam(required = false) String outletId) {
        
        try {
            List<RestaurantOrder> orders = loadDataFromFile();
            orders = transformationService.cleanAndValidateData(orders);
            
            if (outletId != null) {
                orders = orders.stream()
                        .filter(order -> outletId.equals(order.getOutletId()))
                        .collect(java.util.stream.Collectors.toList());
            }
            
            Map<String, Object> analysis = branchPerformanceAnalytics.generateBranchPerformanceAnalysis(orders);
            return ResponseEntity.ok(analysis);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    @GetMapping("/outlets")
    public ResponseEntity<List<Map<String, Object>>> getOutlets() {
        try {
            List<RestaurantOrder> orders = loadDataFromFile();
            
            List<Map<String, Object>> outlets = orders.stream()
                    .collect(java.util.stream.Collectors.groupingBy(RestaurantOrder::getOutletId))
                    .entrySet().stream()
                    .map(entry -> {
                        RestaurantOrder sample = entry.getValue().get(0);
                        Map<String, Object> map = new java.util.HashMap<>();
                        map.put("outletId", entry.getKey());
                        map.put("outletName", sample.getOutletName() != null ? sample.getOutletName() : "Unknown");
                        map.put("borough", sample.getBorough() != null ? sample.getBorough() : "Unknown");
                        map.put("capacity", sample.getCapacity() != null ? sample.getCapacity() : 0);
                        return map;
                    })
                    .collect(java.util.stream.Collectors.toList());
            
            return ResponseEntity.ok(outlets);
            
        } catch (Exception e) {
            Map<String, Object> errorMap = new java.util.HashMap<>();
            errorMap.put("error", e.getMessage());
            return ResponseEntity.badRequest().body(List.of(errorMap));
        }
    }
    
    private List<RestaurantOrder> loadDataFromFile() {
        try {
            // Try multiple possible locations for the CSV file
            String[] possiblePaths = {
                "restaurant_dataset_combined.csv",
                "./restaurant_dataset_combined.csv",
                "../restaurant_dataset_combined.csv",
                "backend/restaurant_dataset_combined.csv"
            };
            
            for (String path : possiblePaths) {
                try {
                    java.nio.file.Path filePath = java.nio.file.Paths.get(path);
                    if (java.nio.file.Files.exists(filePath)) {
                        return ingestionService.ingestCsvFile(path).get();
                    }
                } catch (Exception e) {
                    // Try next path
                    continue;
                }
            }
            
            throw new RuntimeException("Could not find restaurant_dataset_combined.csv in any expected location");
        } catch (Exception e) {
            throw new RuntimeException("Failed to load data from file: " + e.getMessage(), e);
        }
    }
}