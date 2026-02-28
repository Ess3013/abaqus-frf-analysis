import pandas as pd
import altair as alt

# Load the data
df = pd.read_csv('FRF_Data.csv')

# Create the chart
chart = alt.Chart(df).mark_line().encode(
    x=alt.X('Frequency (Hz)', title='Frequency (Hz)'),
    y=alt.Y('Strain Energy (J)', title='Total Strain Energy (J)', scale=alt.Scale(type='log')),
    tooltip=['Frequency (Hz)', 'Strain Energy (J)']
).properties(
    title='Frequency Response Function (FRF) - Lattice Structure',
    width=800,
    height=400
).interactive()

# Save the chart as HTML
chart.save('FRF_Plot.html')
print("Plot saved as FRF_Plot.html")
