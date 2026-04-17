import pandas as pd
import random
import joblib
import os
from sklearn.linear_model import LinearRegression  # <-- We changed the import here
from sklearn.preprocessing import OneHotEncoder , PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

print("--- STARTING ECOLOGISTICS AI ENGINE ---")

# 1. Setup exact file paths
current_folder = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_folder, 'SupplyGreenChain.csv')
model_save_path = os.path.join(current_folder, 'supply_model.pkl')

# ==========================================
# PHASE 1: GENERATE LOGISTICS DATASET
# ==========================================
print("Generating 5,000 rows of realistic logistics data...")
modes = ['Truck', 'Rail', 'Sea', 'Air']
# Industry average kg CO2 per ton-km
emission_factors = {'Truck': 0.105, 'Rail': 0.022, 'Sea': 0.016, 'Air': 1.250}

data = []
for _ in range(5000):
    mode = random.choice(modes)
    weight = round(random.uniform(1.0, 50.0), 1)     # 1 to 50 tons
    distance = round(random.uniform(50, 3000), 1)    # 50 to 3000 km
    
    # Calculate emissions + 5% random real-world variance
    base_emission = weight * distance * emission_factors[mode]
    variance = random.uniform(0.95, 1.05)
    total_emission = round(base_emission * variance, 2)
    
    data.append([weight, distance, mode, total_emission])

# Save it as a physical file
df = pd.DataFrame(data, columns=['weight_tons', 'distance_km', 'transport_mode', 'carbon_emissions_kg'])
df.to_csv(csv_file_path, index=False)
print(f"-> Success: Created {csv_file_path}")

# ==========================================
# PHASE 2: TRAIN AND SAVE THE AI
# ==========================================
print("\nTraining the Machine Learning Model...")
X = df[['weight_tons', 'distance_km', 'transport_mode']]
y = df['carbon_emissions_kg']

numeric_transformer = Pipeline(steps=[
    ('poly', PolynomialFeatures(degree=2, include_bias=False))
])
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', ['weight_tons', 'distance_km']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['transport_mode'])
    ])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('poly', PolynomialFeatures(degree=3, include_bias=False)),
    ('regressor', LinearRegression()) 
])

model.fit(X, y)

print("Saving the trained brain to disk...")
joblib.dump(model, model_save_path)
print(f"\n--- MISSION ACCOMPLISHED! Model saved as {model_save_path} ---")