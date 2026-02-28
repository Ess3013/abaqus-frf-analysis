import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('FRF_Data.csv')

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(df['Frequency (Hz)'], df['Strain Energy (J)'], linewidth=1.5, color='blue')

# Formatting
plt.yscale('log')
plt.xlabel('Frequency (Hz)', fontsize=12)
plt.ylabel('Total Strain Energy (J) - Log Scale', fontsize=12)
plt.title('Frequency Response Function (FRF) - Lattice Structure', fontsize=14)
plt.grid(True, which="both", ls="-", alpha=0.5)

# Highlight identified features
plt.axvspan(7030, 9240, color='red', alpha=0.2, label='1st Bandgap')
plt.axvspan(11100, 14600, color='green', alpha=0.2, label='2nd Bandgap')

plt.legend()

# Save the plot
plt.savefig('FRF_Plot.png', dpi=300)
print("Plot saved as FRF_Plot.png")
