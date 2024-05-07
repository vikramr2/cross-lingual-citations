import igraph as ig
import matplotlib.pyplot as plt

# Create a complete graph with 7 vertices
g = ig.Graph(n=7)

# Visual style for the graph
visual_style = {
    "vertex_size": 20,
    "vertex_label": range(1, 8),
    "vertex_color": "lightblue",
    "vertex_label_dist": 2,
    "edge_color": "gray",
    "bbox": (300, 300),
    "margin": 20
}

# Plotting
ig.plot(g, **visual_style).save("7_empty.png")

# Displaying the image using matplotlib to show it in this notebook environment
img = plt.imread("7_empty.png")
plt.figure(figsize=(6,6))
plt.imshow(img)
plt.axis('off')  # Turn off axis numbers and ticks
plt.savefig('7empty.png')