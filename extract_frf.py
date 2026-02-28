# Script to extract FRF (strain energy) data from Abaqus ODB
from odbAccess import openOdb
import csv

# Open the ODB file
odb = openOdb('Job-1.odb')

# Access Step 2 (Steady State Dynamics)
step = odb.steps['Step-2']

# Get frequency data and strain energy
frequency_data = []
strain_energy_data = []

# Get history regions
historyRegions = step.historyRegions

# Print available history regions for debugging
print("Available History Regions:")
for key in historyRegions.keys():
    print("  -", key)

# Try to find strain energy output
for key in historyRegions.keys():
    hr = historyRegions[key]
    for outputKey in hr.historyOutputs.keys():
        print("  Output in", key, ":", outputKey)

# Extract frequency and strain energy
# For steady-state dynamics, frequency is typically in the history output
# Common names for the whole model energy region include:
# 'Energy: Whole Model', 'Energy for whole model', 'Energy for the whole model'
possible_regions = ['Energy: Whole Model', 'Energy for whole model', 'Energy for the whole model']
found_region = None

for region_name in possible_regions:
    if region_name in historyRegions:
        found_region = historyRegions[region_name]
        print(f"Found energy region: {region_name}")
        break

if found_region:
    if 'ALLSE' in found_region.historyOutputs:
        allse = found_region.historyOutputs['ALLSE']
        for frame in allse.data:
            frequency_data.append(frame[0])  # Frequency
            strain_energy_data.append(frame[1])  # Strain Energy
    else:
        print("ALLSE not found in the identified region.")
else:
    # Try searching all regions for ALLSE
    for key, hr in historyRegions.items():
        if 'ALLSE' in hr.historyOutputs:
            allse = hr.historyOutputs['ALLSE']
            print(f"Found ALLSE in history region: {key}")
            for frame in allse.data:
                frequency_data.append(frame[0])
                strain_energy_data.append(frame[1])
            break

# Write to CSV
if frequency_data:
    with open('FRF_Data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Frequency (Hz)', 'Strain Energy (J)'])
        for freq, se in zip(frequency_data, strain_energy_data):
            writer.writerow([freq, se])
    print(f"\nExtracted {len(frequency_data)} data points to FRF_Data.csv")
else:
    print("\nNo strain energy data found in history output.")
    print("Checking frame output...")
    
    # Try to get from field output frames
    frames = step.frames
    print(f"Number of frames: {len(frames)}")
    for i, frame in enumerate(frames):
        print(f"Frame {i}: Frequency = {frame.frameValue}")

odb.close()
