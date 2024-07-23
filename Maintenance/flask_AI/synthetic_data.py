import pandas as pd
import numpy as np

num_samples = 1000
np.random.seed(42)

# Generate synthetic data
operation_time = np.random.randint(100, 10000, num_samples)
locations = np.random.choice(['desert', 'hilly', 'rainy', 'humid', 'all'], num_samples)
companies = np.random.choice(['tata', 'mahindra', 'ashok leyland', 'bharat benz', 'eicher motors'], num_samples)
engines = np.random.choice(['Mahindra Supro Profit Truck (Mini)', 'Mahindra Jeeto Plus', 'Maruti Suzuki Eeco Cargo', 'Ashok Leyland Dost Strong', 'Maruti Suzuki Super Carry'], num_samples)
milage = np.random.choice(['22 kmpl', '21.2 kmpl', '19.71 kmpl', '19.6 kmpl', '18 kmpl'], num_samples)
maintenance_needed = np.random.choice([0, 1], num_samples, p=[0.7, 0.3])

# Create DataFrame
data = pd.DataFrame({
    'operation_time': operation_time,
    'location': locations,
    'company': companies,
    'engine': engines,
    'milage': milage,
    'maintenance_needed': maintenance_needed
})

# Save to CSV
data.to_csv('synthetic_truck_maintenance_data.csv', index=False)
