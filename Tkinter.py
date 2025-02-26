import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Demo:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Demo")
        self.root.geometry("800x600")

        self.theme_color = "teal"

        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Home screen
        self.home_frame = ttk.Frame(self.notebook, style='My.TFrame')
        self.notebook.add(self.home_frame, text='Home')
        self.setup_home_screen()

        # Path Planning screen
        self.path_frame = ttk.Frame(self.notebook, style='My.TFrame')
        self.notebook.add(self.path_frame, text='Path Planning')
        self.setup_path_planning_screen()

        # Post Processing screen
        self.post_frame = ttk.Frame(self.notebook, style='My.TFrame')
        self.notebook.add(self.post_frame, text='Post Processing')
        self.setup_post_processing_screen()

        # Custom Planning screen
        self.custom_frame = ttk.Frame(self.notebook, style='My.TFrame')
        self.notebook.add(self.custom_frame, text='Custom Planning')
        self.setup_custom_planning_screen()

        # Navigation buttons
        self.nav_bar = ttk.Frame(root, style='My.TFrame')
        self.nav_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.setup_navigation_bar()

    def setup_home_screen(self):
        label = ttk.Label(self.home_frame, text="Welcome Home", font=("Helvetica", 24))
        label.pack(pady=100)

    def setup_path_planning_screen(self):
        label = ttk.Label(self.path_frame, text="Path Planning", font=("Helvetica", 24))
        label.pack(pady=100)

        # Dummy map view (placeholder)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot([1, 2, 3, 4], [5, 10, 12, 9])
        ax.set_ylabel("Y Axis")
        ax.set_xlabel("X Axis")

        canvas = FigureCanvasTkAgg(fig, master=self.path_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        gen_file_button = ttk.Button(self.path_frame, text="Generate File", command=self.generate_file)
        gen_file_button.pack(pady=20)

    def setup_post_processing_screen(self):
        label = ttk.Label(self.post_frame, text="Post Processing", font=("Helvetica", 24))
        label.pack(pady=100)

        # Dummy plot (placeholder)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot([1, 2, 3, 4], [5, 10, 12, 9])
        ax.set_ylabel("Y Axis")
        ax.set_xlabel("X Axis")

        canvas = FigureCanvasTkAgg(fig, master=self.post_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        find_file_button = ttk.Button(self.post_frame, text="Find Data File", command=self.find_data_file)
        find_file_button.pack(pady=20)

    def setup_custom_planning_screen(self):
        label = ttk.Label(self.custom_frame, text="Custom Planning", font=("Helvetica", 24))
        label.pack(pady=100)

        # Dummy map view (placeholder)
        # For demonstration purposes, you may need to integrate a proper map library
        # such as OpenStreetMap with Tkinter, which is more complex.
        map_label = ttk.Label(self.custom_frame, text="Custom Map Placeholder")
        map_label.pack(pady=20)

        enter_location_entry = ttk.Entry(self.custom_frame, width=30)
        enter_location_entry.pack(pady=20)

        gen_file_button = ttk.Button(self.custom_frame, text="Generate File", command=self.generate_file)
        gen_file_button.pack(pady=20)

    def setup_navigation_bar(self):
        nav_label = ttk.Label(self.nav_bar, text="Navigation", font=("Helvetica", 18))
        nav_label.pack(pady=20)

        buttons = [
            ("Home", self.home_frame),
            ("Path Planning", self.path_frame),
            ("Custom Planning", self.custom_frame),
            ("Post Processing", self.post_frame)
        ]

        for text, frame in buttons:
            button = ttk.Button(self.nav_bar, text=text, command=lambda f=frame: self.show_frame(f))
            button.pack(fill=tk.X, padx=10, pady=5)

    def show_frame(self, frame):
        self.notebook.select(frame)

    def generate_file(self):
        print("Generate File button pressed")

    def find_data_file(self):
        print("Find Data File button pressed")

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.configure('My.TFrame', background='white', foreground='black')
    app = Demo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
