import csv
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
import os

def plot_frf(csv_path, output_png):
    if not os.path.exists(csv_path):
        print(f"CSV file {csv_path} not found.")
        return

    freq = []
    energy = []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            freq.append(float(row['Frequency (Hz)']))
            energy.append(float(row['Strain Energy (J)']))
            
    freq = np.array(freq)
    energy = np.array(energy)

    # Set up image dimensions
    width, height = 1000, 600
    padding = 80
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Data scaling
    log_energy = np.log10(energy)
    min_freq, max_freq = freq.min(), freq.max()
    min_log, max_log = log_energy.min(), log_energy.max()

    # Padding for Y-axis to see the line clearly
    log_range = max_log - min_log
    if log_range == 0:
        log_range = 1.0
    y_min_plot = min_log - 0.1 * log_range
    y_max_plot = max_log + 0.1 * log_range

    def to_coords(f, le):
        x = padding + (f - min_freq) / (max_freq - min_freq) * (width - 2 * padding)
        y = height - padding - (le - y_min_plot) / (y_max_plot - y_min_plot) * (height - 2 * padding)
        return x, y

    # Draw grid
    for i in range(11):
        f_grid = min_freq + i * (max_freq - min_freq) / 10.0
        x_grid, _ = to_coords(f_grid, min_log)
        draw.line([(x_grid, padding), (x_grid, height - padding)], fill=(230, 230, 230), width=1)

    # Draw axes
    draw.line([(padding, padding), (padding, height - padding)], fill=(0, 0, 0), width=2)
    draw.line([(padding, height - padding), (width - padding, height - padding)], fill=(0, 0, 0), width=2)

    # Draw the line
    points = [to_coords(f, le) for f, le in zip(freq, log_energy)]
    draw.line(points, fill=(0, 0, 255), width=2)

    # Draw Labels (Simple)
    draw.text((width/2 - 50, height - 40), "Frequency (Hz)", fill=(0,0,0))
    draw.text((20, height/2), "log10(SE)", fill=(0,0,0))
    draw.text((width/2 - 100, 20), f"FRF Plot: {os.path.basename(csv_path)}", fill=(0,0,0))

    # Save
    img.save(output_png)
    print(f"Plot saved as {output_png}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        csv_in = 'Sweep_Files/Job_F_S_2_FRF.csv'
        png_out = 'Job_F_S_2_Plot.png'
    else:
        csv_in = sys.argv[1]
        png_out = sys.argv[2]
        
    plot_frf(csv_in, png_out)
