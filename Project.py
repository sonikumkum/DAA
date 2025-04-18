import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AirTrafficControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Air Traffic Control System")
        self.root.geometry("900x700")

        self.graph = nx.Graph()

        # Load default airport connections
        self.load_default_routes()

        # Create UI
        self.create_widgets()

        # Draw the initial graph
        self.show_graph()

    def load_default_routes(self):
        # Predefined routes between airports
        self.graph.add_edge("A", "B", weight=300)
        self.graph.add_edge("A", "C", weight=400)
        self.graph.add_edge("B", "D", weight=500)
        self.graph.add_edge("B", "E", weight=200)
        self.graph.add_edge("C", "E", weight=600)
        self.graph.add_edge("D", "E", weight=800)
        self.graph.add_edge("D", "F", weight=300)
        self.graph.add_edge("E", "F", weight=400)

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")

        # Frame for inputs
        input_frame = ttk.LabelFrame(self.root, text="Find Shortest Path", padding=10)
        input_frame.pack(pady=20, padx=10, fill="x")

        ttk.Label(input_frame, text="Start Airport:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.start_entry = ttk.Entry(input_frame)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="End Airport:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.end_entry = ttk.Entry(input_frame)
        self.end_entry.grid(row=0, column=3, padx=5, pady=5)

        self.find_button = ttk.Button(input_frame, text="Find Shortest Path", command=self.find_shortest_path)
        self.find_button.grid(row=0, column=4, padx=10)

        # Show all paths button
        self.show_button = ttk.Button(self.root, text="Show All Available Paths", command=self.show_all_paths)
        self.show_button.pack(pady=10)

    def find_shortest_path(self):
        start = self.start_entry.get().strip().upper()
        end = self.end_entry.get().strip().upper()

        if start not in self.graph or end not in self.graph:
            messagebox.showerror("Invalid Airports", "Start or End airport not found.")
            return

        try:
            length, path = nx.single_source_dijkstra(self.graph, start, target=end)
            result = f"The shortest path from {start} to {end}:\n" + " → ".join(path) + f"\nTotal Distance: {length} km"
            messagebox.showinfo("Shortest Path", result)
        except nx.NetworkXNoPath:
            messagebox.showerror("No Path", "No path exists between the airports.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_all_paths(self):
        if not self.graph.edges:
            messagebox.showinfo("No Paths", "No routes available.")
            return

        all_paths = "\n".join([f"{u} → {v} : {d['weight']} km" for u, v, d in self.graph.edges(data=True)])
        messagebox.showinfo("Available Routes", all_paths)

    def show_graph(self):
        pos = {
            "A": (2, 0),
            "B": (1, 1),
            "C": (3, 1),
            "D": (0, 2),
            "E": (2, 2),
            "F": (1, 3)
        }

        fig, ax = plt.subplots(figsize=(7, 5))
        nx.draw(self.graph, pos, with_labels=True, ax=ax,
                node_size=2000, node_color="skyblue", font_size=12,
                font_weight="bold", edge_color="black")

        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

# Run the app
root = tk.Tk()
app = AirTrafficControl(root)
root.mainloop()
