import tkinter as tk
from tkinter import ttk
import mouse
import time
import threading

class SimultaneousClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Simultaneous Clicker")
        self.root.geometry("400x300")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Instructions
        instructions = ttk.Label(main_frame, text="Click the button below to trigger simultaneous clicks.\nMake sure your windows are in position first!", wraplength=350)
        instructions.grid(row=0, column=0, pady=10)
        
        # Click button
        self.click_button = ttk.Button(main_frame, text="Click Both Windows", command=self.trigger_clicks)
        self.click_button.grid(row=1, column=0, pady=20)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=2, column=0, pady=10)
        
        # Countdown label
        self.countdown_label = ttk.Label(main_frame, text="")
        self.countdown_label.grid(row=3, column=0, pady=10)
        
        # Window positions
        self.window1_pos = None
        self.window2_pos = None
        
        # Setup buttons
        ttk.Button(main_frame, text="Set Window 1 Position", command=self.set_window1_position).grid(row=4, column=0, pady=5)
        ttk.Button(main_frame, text="Set Window 2 Position", command=self.set_window2_position).grid(row=5, column=0, pady=5)
        
        # Position labels
        self.pos1_label = ttk.Label(main_frame, text="Window 1: Not set")
        self.pos1_label.grid(row=6, column=0, pady=5)
        self.pos2_label = ttk.Label(main_frame, text="Window 2: Not set")
        self.pos2_label.grid(row=7, column=0, pady=5)

    def set_window1_position(self):
        self.status_label.config(text="Move mouse to Window 1 position and press Enter...")
        self.root.update()
        self.root.bind('<Return>', self.save_window1_position)
        
    def save_window1_position(self, event):
        self.window1_pos = mouse.get_position()
        self.pos1_label.config(text=f"Window 1: {self.window1_pos}")
        self.status_label.config(text="Window 1 position saved!")
        self.root.unbind('<Return>')
        
    def set_window2_position(self):
        self.status_label.config(text="Move mouse to Window 2 position and press Enter...")
        self.root.update()
        self.root.bind('<Return>', self.save_window2_position)
        
    def save_window2_position(self, event):
        self.window2_pos = mouse.get_position()
        self.pos2_label.config(text=f"Window 2: {self.window2_pos}")
        self.status_label.config(text="Window 2 position saved!")
        self.root.unbind('<Return>')

    def click_window(self, position, window_num):
        if position:
            try:
                # Move to position and double click
                mouse.move(position[0], position[1])
                mouse.double_click()
                print(f"Successfully clicked window {window_num} at position {position}")
            except Exception as e:
                print(f"Error clicking window {window_num}: {str(e)}")

    def trigger_clicks(self):
        if not self.window1_pos or not self.window2_pos:
            self.status_label.config(text="Please set both window positions first!")
            return
            
        self.status_label.config(text="Starting in 3 seconds...")
        self.root.update()
        
        # Countdown
        for i in range(3, 0, -1):
            self.countdown_label.config(text=str(i))
            self.root.update()
            time.sleep(1)
            
        self.countdown_label.config(text="")
        self.status_label.config(text="Clicking!")
        
        # Click windows as quickly as possible
        self.click_window(self.window1_pos, 1)
        self.click_window(self.window2_pos, 2)
        
        self.status_label.config(text="Clicks completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimultaneousClicker(root)
    root.mainloop()