import tempfile
import webbrowser

import plotly
import plotly.graph_objects as go
import json
from flask import Flask, render_template_string
import threading
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>3D Maze Viewer</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h2>Interactive 3D Maze</h2>
    <div id="plotly-div" style="width:100%;height:90vh;"></div>
    <script>
        const fig = {{ plot_json | safe }};
        Plotly.newPlot('plotly-div', fig.data, fig.layout);
    </script>
</body>
</html>
"""

app = Flask(__name__)
plot_data = None

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, plot_json=plot_data)

def visualize_3d_maze(maze, paths=None):
    global plot_data

    wall_x, wall_y, wall_z = [], [], []
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            for z in range(len(maze[0][0])):
                if maze[x][y][z] == 1:
                    wall_x.append(x)
                    wall_y.append(y)
                    wall_z.append(z)

    wall_trace = go.Scatter3d(
        x=wall_x,
        y=wall_y,
        z=wall_z,
        mode='markers',
        marker=dict(size=3, color='black', opacity=0.05),
        name='Walls'
    )

    data = [wall_trace]

    if paths:
        for path in paths:
            if not path:
                continue
            px, py, pz = zip(*path)
            path_trace = go.Scatter3d(
                x=px,
                y=py,
                z=pz,
                mode='lines+markers',
                line=dict(color='red', width=4),
                marker=dict(size=3, color='red'),
                name='Path'
            )
            data.append(path_trace)

    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube'
        ),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)
    plot_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    def run():
        app.run(port=5000, debug=False, use_reloader=False)

    threading.Thread(target=run).start()
    webbrowser.open("http://127.0.0.1:5000")