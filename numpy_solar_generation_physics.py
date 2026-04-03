import numpy as np

def calculate_solar_radiation(tilt_angle, azimuth, lat, day_of_year):
    """
    Advanced Solar Radiation Intensity Calculation using NumPy vectorization.
    Simulates the beam radiation on a tilted surface.
    """
    delta = 23.45 * np.sin(np.deg2rad(360/365 * (284 + day_of_year)))
    
    phi = np.deg2rad(lat)
    beta = np.deg2rad(tilt_angle)
    gamma = np.deg2rad(azimuth)
    
    omega = np.deg2rad(np.linspace(-90, 90, 48))
    
    cos_theta_z = (np.sin(phi) * np.sin(delta) + 
                  np.cos(phi) * np.cos(delta) * np.cos(omega))
    
    cos_theta_z = np.clip(cos_theta_z, 0, 1)
    
    cos_theta = (np.sin(delta) * (np.sin(phi)*np.cos(beta) - np.cos(phi)*np.sin(beta)*np.cos(gamma)) + 
                 np.cos(delta) * np.cos(omega) * (np.cos(phi)*np.cos(beta) + np.sin(phi)*np.sin(beta)*np.cos(gamma)) + 
                 np.cos(delta) * np.sin(beta) * np.sin(gamma) * np.sin(omega))
    
    cos_theta = np.clip(cos_theta, 0, 1)
    
    I_sc = 1367
    I_beam = I_sc * cos_theta
    
    return omega, I_beam

TILT = 30
AZIMUTH = 0
LAT = 34.05
DAY = 172

omega, radiation = calculate_solar_radiation(TILT, AZIMUTH, LAT, DAY)

print(f"  Solar Physics Simulation (Day {DAY})  ")
print(f"Max Irradiance: {np.max(radiation):.2f} W/m")
print(f"Average Irradiance: {np.mean(radiation):.2f} W/m")
print(f"Total Theoretical Daily Energy: {np.trapz(radiation, omega):.2f} kWh/m equivalent")

rotation_matrix = np.array([[np.cos(0.1), -np.sin(0.1)], 
                           [np.sin(0.1),  np.cos(0.1)]])
tracked_vector = np.dot(rotation_matrix, np.array([np.mean(radiation), np.max(radiation)]))

print(f"\n Tracker Displacement Vector: {tracked_vector}")
print(" NumPy Operations Complete ")
