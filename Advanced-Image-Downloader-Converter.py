import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import webbrowser

# --- Main Application ---
class ImageToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 darkboss1bd - Advanced Image Downloader & Converter")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.config(bg="#0e1a2b")

        # --- Hacker Animation (ASCII Style) ---
        self.animation_text = """
  █▀ █▀█ █░█ █▀█ ▄▀█ █░░   █▀▀ █▀█ █▀█ █▀▄ █░█ █▀
  ▄█ █▄█ █▄█ █▀▄ █▀█ █▄▄   █▄▄ █▄█ █▀▄ █▄▀ █▄█ ▄█
        [Initializing DarkBoss Tool v2.0...]
        [Scanning Target URL...]
        [Access Granted!]
        """
        self.create_banner()
        self.create_ui()
        self.animate_banner()

    def create_banner(self):
        # Banner Frame
        banner_frame = tk.Frame(self.root, bg="#001f3f", height=100)
        banner_frame.pack(fill="x")

        banner_label = tk.Label(
            banner_frame,
            text="🔥 darkboss1bd 🔥",
            font=("Courier", 18, "bold"),
            fg="#00ffcc",
            bg="#001f3f"
        )
        banner_label.pack(pady=20)

        # Animated ASCII Art
        self.anim_label = tk.Label(
            self.root,
            text=self.animation_text,
            font=("Courier", 10),
            fg="#00ff00",
            bg="#0e1a2b",
            justify="left"
        )
        self.anim_label.pack(pady=10)

    def animate_banner(self):
        colors = ["#00ff00", "#00cc00", "#00aa00", "#008800", "#00ff00"]
        self.animate_color_cycle(colors, 0)

    def animate_color_cycle(self, colors, index):
        self.anim_label.config(fg=colors[index])
        self.root.after(500, self.animate_color_cycle, colors, (index + 1) % len(colors))

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#1a2b3c", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # URL Entry
        tk.Label(main_frame, text="🌐 Enter Image URL:", font=("Arial", 12), bg="#1a2b3c", fg="white").pack(anchor="w", pady=(10, 0))
        self.url_entry = tk.Entry(main_frame, width=60, font=("Arial", 11), bd=5, relief="ridge")
        self.url_entry.pack(pady=5, fill="x")

        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#1a2b3c")
        btn_frame.pack(pady=15)

        download_btn = tk.Button(
            btn_frame, text="🔽 Download Image", font=("Arial", 10, "bold"),
            bg="#007acc", fg="white", width=15, command=self.download_image
        )
        download_btn.grid(row=0, column=0, padx=10)

        convert_btn = tk.Button(
            btn_frame, text="🔄 Convert & Resize", font=("Arial", 10, "bold"),
            bg="#28a745", fg="white", width=15, command=self.convert_image
        )
        convert_btn.grid(row=0, column=1, padx=10)

        # Size Selection
        tk.Label(main_frame, text="📏 Resize to:", font=("Arial", 11), bg="#1a2b3c", fg="white").pack(anchor="w", pady=(10, 5))
        self.size_var = tk.StringVar(value="1920x1080")
        sizes = ["1920x1080 (Ultra HD)", "1080x1080 (Square)", "800x600", "640x480", "Custom (WxH)"]
        size_menu = ttk.Combobox(main_frame, values=sizes, textvariable=self.size_var, state="readonly", font=("Arial", 10))
        size_menu.pack(fill="x", pady=5)

        # Custom Size Input
        self.custom_frame = tk.Frame(main_frame, bg="#1a2b3c")
        self.custom_frame.pack(fill="x", pady=5)
        tk.Label(self.custom_frame, text="Custom W:", bg="#1a2b3c", fg="white", font=("Arial", 9)).grid(row=0, column=0)
        self.custom_w = tk.Entry(self.custom_frame, width=8, font=("Arial", 9))
        self.custom_w.grid(row=0, column=1, padx=5)
        tk.Label(self.custom_frame, text="H:", bg="#1a2b3c", fg="white", font=("Arial", 9)).grid(row=0, column=2)
        self.custom_h = tk.Entry(self.custom_frame, width=8, font=("Arial", 9))
        self.custom_h.grid(row=0, column=3, padx=5)
        self.custom_frame.pack_forget()

        # Show custom input if selected
        size_menu.bind("<<ComboboxSelected>>", self.toggle_custom)

        # Image Preview
        self.preview_label = tk.Label(main_frame, text="🖼️ Image Preview", bg="#1a2b3c", fg="#aaa", font=("Arial", 10))
        self.preview_label.pack(pady=10)

        # Footer with Links
        footer = tk.Frame(self.root, bg="#001f3f", height=50)
        footer.pack(fill="x", side="bottom")

        link1 = tk.Label(footer, text="📱 Telegram: @darkvaiadmin", fg="#00ccff", bg="#001f3f", cursor="hand2", font=("Arial", 10, "underline"))
        link1.pack(side="left", padx=20, pady=15)
        link1.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/darkvaiadmin"))

        link2 = tk.Label(footer, text="🌐 Website: serialkey.top", fg="#00ccff", bg="#001f3f", cursor="hand2", font=("Arial", 10, "underline"))
        link2.pack(side="right", padx=20, pady=15)
        link2.bind("<Button-1>", lambda e: webbrowser.open("https://serialkey.top/"))

        # Internal Variables
        self.image = None

    def toggle_custom(self, event=None):
        if self.size_var.get() == "Custom (WxH)":
            self.custom_frame.pack(fill="x", pady=5)
        else:
            self.custom_frame.pack_forget()

    def download_image(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("⚠️ Warning", "Please enter a valid image URL!")
            return

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.image = Image.open(BytesIO(response.content))
            self.display_image(self.image)
            messagebox.showinfo("✅ Success", "Image downloaded successfully in Ultra HD!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to download image:\n{str(e)}")

    def display_image(self, img):
        img_display = img.copy()
        img_display.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(img_display)
        self.preview_label.configure(image=photo, text="")
        self.preview_label.image = photo

    def convert_image(self):
        if self.image is None:
            messagebox.showwarning("⚠️ Warning", "No image loaded! Download first.")
            return

        size_str = self.size_var.get()
        try:
            if size_str == "Custom (WxH)":
                w = int(self.custom_w.get())
                h = int(self.custom_h.get())
                size = (w, h)
            else:
                size = size_str.split()[0]
                w, h = map(int, size.split('x'))
                size = (w, h)

            resized_img = self.image.resize(size, Image.LANCZOS)
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("All Files", "*.*")]
            )
            if save_path:
                resized_img.save(save_path)
                messagebox.showinfo("✅ Success", f"Image saved as {save_path} with size {size}")
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter valid numbers for custom size!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Resize failed: {str(e)}")

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToolApp(root)
    root.mainloop()