import json
import random
import networkx as nx
from pyvis.network import Network
import os
import webbrowser
from urllib.parse import quote

def load_data(path="data/symbols.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_graph(data):
    G = nx.Graph()
    for node in data["nodes"]:
        G.add_node(node["id"], type=node["type"])
    for edge in data["edges"]:
        G.add_edge(edge[0], edge[1])
    return G

def randomize_color(base_hex, variation=30, transparency="aa"):
    r = int(base_hex[1:3], 16)
    g = int(base_hex[3:5], 16)
    b = int(base_hex[5:7], 16)
    
    r = min(255, max(0, r + random.randint(-variation, variation)))
    g = min(255, max(0, g + random.randint(-variation, variation)))
    b = min(255, max(0, b + random.randint(-variation, variation)))
    
    return f"#{r:02x}{g:02x}{b:02x}{transparency}"

def visualize_interactive_graph():
    data = load_data()
    G = build_graph(data)
    
    base_colors = {
        "planet": "#2e1630",
        "metal": "#aaaaaa",
        "mood": "#00fddb",
        "tarot": "#ffcc00",
        "symbol": "#cc33ff",
        "esoteric_concept": "#33ccff"
    }
    
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        notebook=False
    )
    
    # Add nodes with randomized colors
    for node, node_data in G.nodes(data=True):
        node_type = node_data.get("type", "")
        base_color = base_colors.get(node_type, "#ffffff")
        random_color = randomize_color(base_color)
        net.add_node(
            node,
            label=node,
            color=random_color,
            title=f"{node} ({node_type})"
        )
    
    # edges
    for source, target in G.edges():
        net.add_edge(source, target, color="#888888", width=0.5)

    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)
    
    # Save the file
    output_path = "esoteric_network.html"
    net.save_graph(output_path)
    abs_path = os.path.abspath(output_path)
    print(f"Graph saved to: {abs_path}")
    
    # Open in browser - Windows compatible
    try:
        # Convert path to URI format
        uri_path = abs_path.replace('\\', '/')
        if not uri_path.startswith('/'):
            uri_path = '/' + uri_path
        webbrowser.open(f"file://{uri_path}")
    except Exception as e:
        print(f"Couldn't open automatically: {str(e)}")
        print(f"Please manually open the file at: {abs_path}")

if __name__ == "__main__":
    visualize_interactive_graph()