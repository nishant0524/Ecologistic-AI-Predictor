from django.shortcuts import render
import joblib
import pandas as pd
import os

# ==========================================
# 1. THE COLD START FIX (Load Model Globally)
# ==========================================
# We load the AI brain here at the top so it only loads ONCE when the server starts.
# If we put this inside the function, the server would lag on every single click!

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'predictor', 'ml_models', 'supply_model.pkl')

print("Loading AI Model into server memory...")
model = joblib.load(MODEL_PATH)

# ==========================================
# 2. THE PREDICTION API
# ==========================================
def predict_emissions(request):
    context = {'prediction': None}
    
    if request.method == 'POST':
        try:
            # 1. Extract data
            user_weight = float(request.POST.get('weight'))
            user_distance = float(request.POST.get('distance'))
            user_mode = request.POST.get('transport_mode')
            
            # 2. Package it for the main prediction
            input_data = pd.DataFrame({
                'weight_tons': [user_weight],
                'distance_km': [user_distance],
                'transport_mode': [user_mode]
            })
            
            # 3. Main Prediction
            raw_result = model.predict(input_data)[0]
            # BUG FIX: Convert numpy.float64 to a standard Python float
            final_prediction = float(max(raw_result, 0)) 
            
            # 4. Real-world equivalencies
            trees = round(final_prediction / 21, 1)
            car_miles = round(final_prediction / 0.4, 1)
            home_days = round(final_prediction / 22, 1)
            
            # --- NEW FEATURE: BACKGROUND CHART PREDICTIONS ---
            modes_to_test = ['Truck', 'Rail', 'Sea', 'Air']
            chart_data = []
            
            for m in modes_to_test:
                test_df = pd.DataFrame({
                    'weight_tons': [user_weight],
                    'distance_km': [user_distance],
                    'transport_mode': [m]
                })
                pred = max(model.predict(test_df)[0], 0)
                # BUG FIX: Convert numpy.float64 to a standard Python float here too!
                chart_data.append(float(round(pred, 2))) 
            
            context['chart_labels'] = modes_to_test
            context['chart_data'] = chart_data
            # --------------------------------------------------
            
            # 5. Send EVERYTHING back
            context['prediction'] = round(final_prediction, 2)
            context['weight'] = user_weight
            context['distance'] = user_distance
            context['mode'] = user_mode
            context['trees'] = trees
            context['car_miles'] = car_miles
            context['home_days'] = home_days
            
        except Exception as e:
            context['error'] = "Something went wrong with the calculation. Please check your inputs."

    return render(request, 'predictor/predict.html', context)