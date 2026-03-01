# Script to extract FRF (strain energy) data from Abaqus ODB
from odbAccess import openOdb
import csv
import sys
import os

def extract_frf(odb_path, csv_path):
    if not os.path.exists(odb_path):
        print("ODB file %s not found." % odb_path)
        return False
        
    # Open the ODB file
    odb = openOdb(odb_path)

    # Access Step 2 (Steady State Dynamics)
    try:
        step = odb.steps['Step-2']
    except KeyError:
        print("Step-2 not found in %s." % odb_path)
        odb.close()
        return False

    # Get frequency data and strain energy
    frequency_data = []
    strain_energy_data = []

    # Get history regions
    historyRegions = step.historyRegions

    # Try searching all regions for ALLSE (Strain Energy)
    for key, hr in historyRegions.items():
        if 'ALLSE' in hr.historyOutputs:
            allse = hr.historyOutputs['ALLSE']
            print("Found ALLSE in history region: %s" % key)
            for frame in allse.data:
                frequency_data.append(frame[0])
                strain_energy_data.append(frame[1])
            break

    # Write to CSV
    if frequency_data:
        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Frequency (Hz)', 'Strain Energy (J)'])
            for freq, se in zip(frequency_data, strain_energy_data):
                writer.writerow([freq, se])
        print("Extracted %d data points to %s" % (len(frequency_data), csv_path))
        odb.close()
        return True
    else:
        print("No strain energy data found in history output of %s." % odb_path)
        odb.close()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: abaqus python extract_frf.py <odb_file> <csv_output>")
    else:
        odb_file = sys.argv[1]
        csv_output = sys.argv[2]
        extract_frf(odb_file, csv_output)
