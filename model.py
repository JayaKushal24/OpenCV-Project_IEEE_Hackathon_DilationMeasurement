import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Read data from CSV file
df = pd.read_csv('circle_radius_data.csv')
df['time_of_data_extraction'] = pd.to_timedelta(df['time_of_data_extraction'])
df['time_difference'] = df['time_of_data_extraction'] - df['time_of_data_extraction'].iloc[0]
df['time_difference_minutes'] = df['time_difference'].dt.total_seconds() / 60  

# Prepare the feature and target variable for regression
X = df['time_difference_minutes'].values.reshape(-1, 1)  # Features
y = df['radius_of_circle'].values  # Target variable

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the linear regression model
model = LinearRegression()
model.fit(X_scaled, y)

# Predict the time difference needed to reach a radius of 5 cm
desired_radius = 5.0
predicted_time_diff_scaled = (desired_radius - model.intercept_) / model.coef_[0]

# Convert the scaled prediction back to minutes
predicted_time_diff_minutes = scaler.inverse_transform([[predicted_time_diff_scaled]])[0][0]

# Calculate the predicted time
initial_time = df['time_of_data_extraction'].iloc[0]
predicted_time = initial_time + pd.to_timedelta(predicted_time_diff_minutes, unit='m')

# Get the last recorded time
last_time = df['time_of_data_extraction'].iloc[-1]

# Calculate remaining time until reaching the predicted radius
remaining_time = predicted_time - last_time

# Print the predictions
print(f"Predicted time to reach a radius of {desired_radius} cm: {predicted_time}")
print(f"TIme Left: {remaining_time}")

# Optional: Plotting the results
plt.scatter(df['time_difference_minutes'], df['radius_of_circle'], color='blue', label='Data Points')
plt.axhline(y=desired_radius, color='red', linestyle='--', label='Target Radius (5 cm)')
plt.xlabel('Time Difference (minutes) from Initial Point')
plt.ylabel('Radius of Circle')
plt.legend()
plt.title('Radius Prediction Based on Time Difference from Initial Point')
plt.grid()
plt.show()
