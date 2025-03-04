import os

import dash
import plotly.graph_objects as go
from dash import dcc, html

# Create a sample Plotly figure
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[3, 1, 6], mode="lines+markers")])

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout for the app
app.layout = html.Div(
    [
        html.H1("Interactive Plotly Graph"),
        dcc.Graph(figure=fig),  # Display the Plotly figure
    ]
)

# Run the app when executed
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1000))  # Use Render's PORT
    app.run_server(debug=False, host="0.0.0.0", port=port)
