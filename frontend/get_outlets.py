from data_processor import data_processor

outlets = data_processor.get_outlets()
print(f"Total outlets: {len(outlets)}")
print("\nOutlet Details:")
for i, outlet in enumerate(outlets):
    print(f"{i+1}. {outlet['name']} - {outlet['borough']} (Capacity: {outlet['capacity']})")

# Get some statistics
df = data_processor.df
print(f"\nData Statistics:")
print(f"Total orders: {len(df):,}")
print(f"Total revenue: LKR {df['total_price_lkr'].sum():,.2f}")
print(f"Average order value: LKR {df['total_price_lkr'].mean():.2f}")
print(f"Unique customers: {df['customer_id'].nunique():,}")