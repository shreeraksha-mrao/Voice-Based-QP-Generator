class WindowManager:
    def __init__(self):
        self.windows = []

    def add_window(self, window):
        self.windows.append(window)

    def close_all_windows(self):
        print("Closing all windows...")
        print("Total windows to close:", len(self.windows))
        for window in self.windows:
            print("Closing window:", window)
            window.destroy()
        print("All windows closed.")

