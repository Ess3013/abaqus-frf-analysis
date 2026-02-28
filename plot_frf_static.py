import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Load data
df = pd.read_csv('FRF_Data.csv')
freq = df['Frequency (Hz)'].values
energy = df['Strain Energy (J)'].values

# Set up image dimensions
width, height = 1000, 600
padding = 80
img = Image.new('RGB', (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# Data scaling
log_energy = np.log10(energy)
min_freq, max_freq = freq.min(), freq.max()
min_log, max_log = log_energy.min(), log_energy.max()

# Ensure we have some range for log scale
if max_log == min_log:
    max_log += 1

def to_coords(f, le):
    x = padding + (f - min_freq) / (max_freq - min_freq) * (width - 2 * padding)
    y = height - padding - (le - min_log) / (max_log - min_log) * (height - 2 * padding)
    return x, y

# Draw axes
draw.line([(padding, padding), (padding, height - padding)], fill=(0, 0, 0), width=2)
draw.line([(padding, height - padding), (width - padding, height - padding)], fill=(0, 0, 0), width=2)

# Draw the line
points = [to_coords(f, le) for f, le in zip(freq, log_energy)]
draw.line(points, fill=(0, 0, 255), width=2)

# Highlight bandgaps
# Bandgap 1: 7030 - 9240
# Bandgap 2: 11100 - 14600
def draw_span(f1, f2, color):
    x1, _ = to_coords(f1, min_log)
    x2, _ = to_coords(f2, min_log)
    draw.rectangle([x1, padding, x2, height - padding], fill=color)

# Draw colored rectangles behind the line
# Note: Redraw line after this
draw_span(7030, 9240, (255, 200, 200)) # Light Red
draw_span(11100, 14600, (200, 255, 200)) # Light Green

# Redraw line and axes for clarity
draw.line([(padding, padding), (padding, height - padding)], fill=(0, 0, 0), width=2)
draw.line([(padding, height - padding), (width - padding, height - padding)], fill=(0, 0, 0), width=2)
draw.line(points, fill=(0, 0, 255), width=2)

# Save
img.save('FRF_Plot.png')
print("Static plot saved as FRF_Plot.png")
