import tkinter as tk
from tkinter import ttk
import smhi_try
from smhi_stationer import get_city_coords, get_station_coords, fetch_stations, fetch_cities, city_input_loop, get_city_coords, clear_terminal
 



def display_resutls(lat, lon, textwidget):
    textwidget.delete(1.0, tk.END)
    smhi_try.main(lat, lon, textwidget)
    root.update_idletasks()
    resize_window()

def on_submit(event=None):
    city_name = city_entry.get()
    lat, lon = get_city_coords(city_name)
    if lat is not None and lon is not None:
        display_resutls(lat, lon, text_widget)

    else:
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "City not found\n")
        root.update_idletasks()
        resize_window()

def resize_window():
    text_widget.update_idletasks()
    req_width = text_widget.winfo_reqwidth()
    req_height = text_widget.winfo_reqheight()
    
    max_width = 80
    max_height = 20
    
    new_text_width = min(req_width, max_width)
    new_text_height = min(req_height, max_height)

    text_widget.config(width=new_text_width, height=new_text_height)

    # Calculate the new window size
    new_width = new_text_width * 10
    new_height = new_text_height * 20  + 40

    # Get the current window size
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    # Resize the window if needed
    if new_width > current_width or new_height > current_height:
        root.geometry(f"{new_width}x{new_height}") 

    # Center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2
    root.geometry(f"{new_width}x{new_height}+{x}+{y}")
    
# Create the main window
root = tk.Tk()
root.title("SMHI App")

# Configure the grid
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


# Create and place the input fields and labels
ttk.Label(root, text="City Name:").grid(row=0, column=0, padx=10, pady=10, sticky="E")
city_entry = ttk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10, sticky="W")
city_entry.bind("<Return>", on_submit)

# Create and place the submit button
submit_button = ttk.Button(root, text="Submit", command= on_submit)
submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="")

# Create and place the text widget for displaying the results
text_widget = tk.Text(root, height=10, width=40)
text_widget.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Initialize the data
fetch_stations()
fetch_cities()
clear_terminal()

# Run the app
root.mainloop()