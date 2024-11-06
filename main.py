import pandas as pd
import plotly.graph_objects as go
from plotly.io import to_html

# Load your data
df = pd.read_csv('data.csv')
df['date'] = pd.to_datetime(df['Date'])

# Identify columns to plot, explicitly excluding 'Date' and 'Type'
stat_columns = df.select_dtypes(include=['float', 'int']).columns.difference(['Date', 'Type'])

# Read the HTML preamble from 'preamble.html'
with open("preamble.html", "r") as preamble_file:
    html_content = preamble_file.read()

# HTML string to save all figures in a single file
# Loop through each stat column and create a single plot with all types on the same chart
for stat in stat_columns:
    fig = go.Figure()
    
    for type_name in df['Type'].unique():
        # Filter data for the current 'Type'
        df_filtered = df[df['Type'] == type_name]
        
        # Add line plot for each 'Type' with larger circle markers
        fig.add_trace(go.Scatter(
            x=df_filtered['date'], 
            y=df_filtered[stat], 
            mode='lines+markers',  # Add markers to the line
            name=type_name,
            marker=dict(size=6),  # Set marker size
            line=dict(width=2)     # Optionally, set line width
        ))

    # Update layout for each figure
    fig.update_layout(title=f"Progression of {stat} by Type",
                      xaxis_title="Date",
                      yaxis_title=stat,
                      showlegend=True)
    
    # Convert each figure to HTML and add it to the HTML content string
    html_content += '<div class="chart-container">' + to_html(fig, full_html=False) + '</div>'

# Close the HTML document
html_content += """
</body>
</html>
"""

# Save the entire content to the specified HTML file
with open("half_marathon_training.html", "w") as f:
    f.write(html_content)

# Display the file path for confirmation
print("All charts saved to half_marathon_training.html")