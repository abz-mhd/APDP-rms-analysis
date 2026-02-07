import requests

try:
    response = requests.get('http://127.0.0.1:5002/api/outlets')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        outlets = response.json()
        print(f"Total outlets: {len(outlets)}")
        print("\nOutlet Details:")
        for i, outlet in enumerate(outlets):
            print(f"{i+1}. {outlet['name']} - {outlet['borough']} (Capacity: {outlet['capacity']})")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")