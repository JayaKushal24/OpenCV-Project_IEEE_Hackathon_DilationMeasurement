import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('circle_radius_data.csv')
df['time_of_data_extraction'] = pd.to_timedelta(df['time_of_data_extraction'])
df['time_difference'] = df['time_of_data_extraction'] - df['time_of_data_extraction'].iloc[0]
df['time_difference_minutes'] = df['time_difference'].dt.total_seconds() / 60

X = df['time_difference_minutes'].values.reshape(-1, 1)
y = df['radius_of_circle'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LinearRegression()
model.fit(X_scaled, y)

desired_radius = 5.0
predicted_time_diff_scaled = (desired_radius - model.intercept_) / model.coef_[0]
predicted_time_diff_minutes = scaler.inverse_transform([[predicted_time_diff_scaled]])[0][0]
initial_time = df['time_of_data_extraction'].iloc[0]
predicted_time = initial_time + pd.to_timedelta(predicted_time_diff_minutes, unit='m')
last_time = df['time_of_data_extraction'].iloc[-1]
remaining_time = predicted_time - last_time

print(f"Predicted time to reach a radius of {desired_radius} cm: {predicted_time}")
print(f"Time left {remaining_time}")

all_time_diff_minutes = np.linspace(0, predicted_time_diff_minutes, num=len(df) + 1).reshape(-1, 1)
all_time_diff_scaled = scaler.transform(all_time_diff_minutes)
predicted_radii = model.predict(all_time_diff_scaled)

plt.scatter(df['time_difference_minutes'], df['radius_of_circle'], color='blue', label='Data Points')
plt.plot(all_time_diff_minutes, predicted_radii, color='orange', label='Prediction Line', linestyle='-')
plt.axhline(y=desired_radius, color='red', linestyle='--', label='Target Radius (5 cm)')
plt.xlabel('Time Difference (minutes) from Initial Point')
plt.ylabel('Radius of Circle')
plt.legend()
plt.title('Radius Prediction Based on Time Difference from Initial Point')
plt.grid()
plt.show()
