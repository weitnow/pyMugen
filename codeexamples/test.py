import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time

# --- Configuration ---
PRESENTATION_TITLE = "Python Dynamic Presentation Demo (Slide Animation)"
FONT_TITLE = ("Inter", 24, "bold")
FONT_HEADING = ("Inter", 16, "bold")
FONT_BODY = ("Inter", 12)

# --- Animation Constants ---
SLIDE_DURATION_MS = 300  # Total duration of the slide in milliseconds
SLIDE_STEPS = 15         # Number of steps in the animation
STEP_DELAY = SLIDE_DURATION_MS // SLIDE_STEPS
START_OFFSET = 800       # Starting pixel offset (must be wide enough to be off-screen)

class SlideTransitionApp(tk.Tk):
    """A presentation application with a smooth slide-in transition."""
    def __init__(self):
        super().__init__()
        self.title(PRESENTATION_TITLE)
        self.geometry("800x600")
        self.current_slide_index = 0
        self.animating = False

        # Container for all slides
        self.container = ttk.Frame(self, padding="10 10 10 10")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.slides = [
            TitleSlide(self.container, self),
            ContentSlide(self.container, self),
            DynamicSlide(self.container, self)
        ]

        # Place all slides in the same spot, using place() for animation control
        for slide in self.slides:
            # We use place() now to precisely control X-position for sliding
            slide.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Control Panel (Navigation) - Unchanged
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(side="bottom", fill="x", pady=10)
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)

        self.prev_button = ttk.Button(self.control_frame, text="← Previous", command=self.show_previous_slide)
        self.prev_button.grid(row=0, column=0, padx=10)

        self.status_label = ttk.Label(self.control_frame, text="", font=FONT_BODY)
        self.status_label.grid(row=0, column=1)

        self.next_button = ttk.Button(self.control_frame, text="Next →", command=self.show_next_slide)
        self.next_button.grid(row=0, column=2, padx=10)

        # Initialize: Show only the first slide, place others off-screen
        for i, slide in enumerate(self.slides):
            if i == 0:
                slide.place(relx=0, rely=0, relwidth=1, relheight=1)
                slide.tkraise()
            else:
                # Place all other slides off-screen to the right (relx=1)
                slide.place(relx=1, rely=0, relwidth=1, relheight=1)
        
        self.update_navigation()

    def animate_slide(self, new_slide_index, direction):
        """Performs the slide-in/out animation."""
        if self.animating:
            return
        
        self.animating = True
        
        old_slide = self.slides[self.current_slide_index]
        new_slide = self.slides[new_slide_index]
        
        # Calculate the starting position (off-screen)
        start_relx_new = 1 if direction == "next" else -1
        end_relx_new = 0
        
        # Place the new slide off-screen and bring it to the front
        new_slide.place(relx=start_relx_new, rely=0, relwidth=1, relheight=1)
        new_slide.tkraise()

        # Calculate the movement distance per step
        move_per_step = abs(start_relx_new) / SLIDE_STEPS

        def step_slide(step):
            if step < SLIDE_STEPS:
                # Calculate new relative X positions
                current_relx_old = old_slide.winfo_x() / old_slide.winfo_width()
                current_relx_new = new_slide.winfo_x() / new_slide.winfo_width()
                
                if direction == "next":
                    # Old slide moves to -1 (left), New slide moves to 0 (center)
                    new_relx_old = current_relx_old - move_per_step
                    new_relx_new = current_relx_new - move_per_step
                else: # "previous"
                    # Old slide moves to 1 (right), New slide moves to 0 (center)
                    new_relx_old = current_relx_old + move_per_step
                    new_relx_new = current_relx_new + move_per_step

                # Update widget positions
                old_slide.place(relx=new_relx_old, rely=0, relwidth=1, relheight=1)
                new_slide.place(relx=new_relx_new, rely=0, relwidth=1, relheight=1)
                
                # Schedule the next step
                self.after(STEP_DELAY, lambda: step_slide(step + 1))
            else:
                # Animation finished
                old_slide.place(relx=1 if direction == "previous" else -1, rely=0, relwidth=1, relheight=1) # Ensure old is fully off-screen
                new_slide.place(relx=0, rely=0, relwidth=1, relheight=1) # Ensure new is centered
                self.current_slide_index = new_slide_index
                self.animating = False
                self.update_navigation()

        step_slide(0)


    def show_slide(self, index, direction):
        """Starts the animation for switching slides."""
        if self.animating or index == self.current_slide_index:
            return

        if 0 <= index < len(self.slides):
            self.animate_slide(index, direction)
            
    def show_next_slide(self):
        """Moves to the next slide in the sequence."""
        next_index = self.current_slide_index + 1
        if next_index < len(self.slides):
            self.show_slide(next_index, "next")

    def show_previous_slide(self):
        """Moves to the previous slide in the sequence."""
        prev_index = self.current_slide_index - 1
        if prev_index >= 0:
            self.show_slide(prev_index, "previous")

    def update_navigation(self):
        """Enables/disables buttons and updates the status label."""
        num_slides = len(self.slides)
        current = self.current_slide_index
        
        state = tk.DISABLED if self.animating else tk.NORMAL

        self.prev_button.config(state=state if current > 0 else tk.DISABLED)
        self.next_button.config(state=state if current < num_slides - 1 else tk.DISABLED)
        self.status_label.config(text=f"Slide {current + 1} of {num_slides}")

# --- Slide Definitions (Now just ttk.Frame, no 'attributes') ---

class TitleSlide(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        title = ttk.Label(self, text=PRESENTATION_TITLE, font=FONT_TITLE, foreground="#3A4A70")
        title.grid(row=1, column=0, sticky="n")

        subtitle = ttk.Label(self, text="A Dynamic Presentation using Python's Tkinter", font=FONT_HEADING, foreground="#666666")
        subtitle.grid(row=2, column=0, sticky="n", pady=10)

        author = ttk.Label(self, text="Built with Code and Animation!", font=FONT_BODY)
        author.grid(row=3, column=0, sticky="n")

class ContentSlide(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        content_frame = ttk.Frame(self, padding="20")
        content_frame.grid(row=0, column=0, sticky="nsew")

        title = ttk.Label(content_frame, text="Why a Dynamic Presentation?", font=FONT_TITLE, foreground="#007BFF")
        title.pack(pady=20, anchor="w")

        ttk.Label(content_frame, text="Unlike static files (like PDF or PPTX), a dynamic GUI can:", font=FONT_HEADING).pack(pady=(10, 5), anchor="w")

        points = [
            "1. Update data in real-time (e.g., from a database or API).",
            "2. Integrate interactive widgets (sliders, buttons, input fields).",
            "3. Run Python code directly for live demonstrations.",
            "4. Change visualization layouts based on user input."
        ]
        for point in points:
            ttk.Label(content_frame, text=f"• {point}", font=FONT_BODY, padding="5 0 0 0").pack(pady=5, anchor="w")

class DynamicSlide(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        content_frame = ttk.Frame(self, padding="20")
        content_frame.grid(row=0, column=0, sticky="nsew")

        title = ttk.Label(content_frame, text="Live Dynamic Content", font=FONT_TITLE, foreground="#28A745")
        title.pack(pady=20)

        instruction = ttk.Label(content_frame, text="Click the button to update the timestamp in real-time:", font=FONT_HEADING)
        instruction.pack(pady=15)

        self.dynamic_label = ttk.Label(content_frame, text="Press the button to begin...", font=FONT_BODY, padding="10", background="#E0FFE0")
        self.dynamic_label.pack(pady=10)

        update_button = ttk.Button(content_frame, text="Generate Live Timestamp", command=self.update_content)
        update_button.pack(pady=20)
        
    def update_content(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dynamic_label.config(text=f"Last updated: {now}\n(This is live Python code execution!)")

if __name__ == "__main__":
    app = SlideTransitionApp()
    app.mainloop()