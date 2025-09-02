import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import webbrowser

class AdvancedImageTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 darkboss1bd - Advanced Image Toolkit")
        self.root.geometry("900x700")
        self.root.config(bg="#0e1a2b")
        self.root.resizable(False, False)

        self.image = None

        # --- Hacker ASCII Animation ---
        self.hack_text = """
    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄    ▄▄   ▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
   █       █      █  █ █  █       █  █  █ █  █      █       █
   █    ▄  █  ▄    █  █ █  █  ▄▄▄▄▄█  █  █▄█  █  ▄   █▄     ▄█
   █   █▄█ █ █ █   █  █▄█  █ █▄     █       █ █ █  █ █ ▄▄▄▄▄█
   █    ▄▄▄█ █▄█   █       █  █▄▄▄▄█  █     █ █ ██ █ █ █▄▄▄▄▄
   █   █    █       █     █ █       █   ▄  █ █ █ █  █ █▄▄▄▄  █
   █▄▄▄█    █▄▄▄▄▄▄  █▄▄▄█ █▄▄▄▄▄▄▄█  █__█ █▄█ █  █▄█▄█       █
           [Initializing DarkBoss Toolkit v3.0...]
           [Accessing Image Module... ✔]
           [Ready to Hack the Pixels!]
        """
        self.create_banner()
        self.create_ui()
        self.animate_hack_text()

    def create_banner(self):
        banner_frame = tk.Frame(self.root, bg="#001f3f", height=80)
        banner_frame.pack(fill="x")
        banner_frame.pack_propagate(False)

        banner_label = tk.Label(
            banner_frame,
            text="🔥 DARKBOSS1BD - IMAGE MASTER TOOL 🔥",
            font=("Courier", 14, "bold"),
            fg="#00ffcc",
            bg="#001f3f"
        )
        banner_label.pack(pady=20)

        self.anim_label = tk.Label(
            self.root,
            text=self.hack_text,
            font=("Courier", 9),
            fg="#00ff00",
            bg="#0e1a2b",
            justify="left"
        )
        self.anim_label.pack(pady=10)

    def animate_hack_text(self):
        colors = ["#00ff00", "#33cc33", "#66aa00", "#999900", "#cc6600", "#ff3300", "#ff0000", "#cc0033"]
        self.cycle_color(colors, 0)

    def cycle_color(self, colors, index):
        self.anim_label.config(fg=colors[index])
        self.root.after(600, self.cycle_color, colors, (index + 1) % len(colors))

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#1a2b3c", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # === Download & Upload Section ===
        tk.Label(main_frame, text="🔽 Download Image from URL", font=("Arial", 12, "bold"), bg="#1a2b3c", fg="white").pack(anchor="w", pady=(10, 5))
        self.url_entry = tk.Entry(main_frame, width=70, font=("Arial", 10), bd=5, relief="ridge")
        self.url_entry.insert(0, "https://example.com/image.jpg")
        self.url_entry.pack(fill="x", pady=5)

        download_btn = tk.Button(
            main_frame, text="📥 Download Image", font=("Arial", 10, "bold"),
            bg="#007acc", fg="white", command=self.download_image
        )
        download_btn.pack(pady=5)

        tk.Label(main_frame, text="📁 Or Upload Image from PC", font=("Arial", 12, "bold"), bg="#1a2b3c", fg="white").pack(anchor="w", pady=(20, 5))
        upload_btn = tk.Button(
            main_frame, text="📂 Choose Image File", font=("Arial", 10, "bold"),
            bg="#d9534f", fg="white", command=self.upload_image
        )
        upload_btn.pack(pady=5)

        # === Resize Options ===
        tk.Label(main_frame, text="📐 Select Resize Preset", font=("Arial", 12, "bold"), bg="#1a2b3c", fg="white").pack(anchor="w", pady=(20, 5))

        self.size_var = tk.StringVar(value="1920x1080 (Ultra HD)")
        sizes = [
            "1920x1080 (Ultra HD)",
            "1280x720 (HD)",
            "1080x1080 (Instagram)",
            "800x600 (Standard)",
            "640x480 (VGA)",
            "Custom (Enter Width & Height)"
        ]
        size_combo = ttk.Combobox(main_frame, values=sizes, textvariable=self.size_var, state="readonly", font=("Arial", 10))
        size_combo.pack(fill="x", pady=5)

        # Custom Size Frame
        self.custom_frame = tk.Frame(main_frame, bg="#1a2b3c")
        tk.Label(self.custom_frame, text="Width:", bg="#1a2b3c", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.custom_w = tk.Entry(self.custom_frame, width=8, font=("Arial", 10))
        self.custom_w.grid(row=0, column=1, padx=5)
        tk.Label(self.custom_frame, text="Height:", bg="#1a2b3c", fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.custom_h = tk.Entry(self.custom_frame, width=8, font=("Arial", 10))
        self.custom_h.grid(row=0, column=3, padx=5)
        self.custom_frame.pack(pady=5)
        self.custom_frame.pack_forget()

        size_combo.bind("<<ComboboxSelected>>", self.toggle_custom_input)

        # === Convert & Save Button ===
        convert_btn = tk.Button(
            main_frame, text="⚡ Convert & Save Image", font=("Arial", 12, "bold"),
            bg="#28a745", fg="white", height=2, command=self.convert_and_save
        )
        convert_btn.pack(pady=20, fill="x")

        # === Image Preview ===
        self.preview_label = tk.Label(
            main_frame, text="🖼️ No Image Loaded\nDownload or Upload to Begin",
            bg="#2c3e50", fg="#aaa", font=("Arial", 11), width=60, height=10, relief="solid"
        )
        self.preview_label.pack(pady=15)

        # === Footer with Clickable Links ===
        footer = tk.Frame(self.root, bg="#001f3f", height=60)
        footer.pack(fill="x", side="bottom")

        telegram_link = tk.Label(
            footer, text="📱 Telegram: @darkvaiadmin", fg="#00ccff", bg="#001f3f",
            font=("Arial", 10, "underline"), cursor="hand2"
        )
        telegram_link.pack(side="left", padx=20, pady=15)
        telegram_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/darkvaiadmin"))

        website_link = tk.Label(
            footer, text="🌐 Website: serialkey.top", fg="#00ccff", bg="#001f3f",
            font=("Arial", 10, "underline"), cursor="hand2"
        )
        website_link.pack(side="right", padx=20, pady=15)
        website_link.bind("<Button-1>", lambda e: webbrowser.open("https://serialkey.top/"))

    def toggle_custom_input(self, event=None):
        if self.size_var.get() == "Custom (Enter Width & Height)":
            self.custom_frame.pack(fill="x", pady=10)
        else:
            self.custom_frame.pack_forget()

    def download_image(self):
        url = self.url_entry.get().strip()
        if not url or "http" not in url:
            messagebox.showwarning("⚠️ Invalid URL", "Please enter a valid image URL!")
            return

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.image = Image.open(BytesIO(response.content))
            self.show_preview(self.image)
            messagebox.showinfo("✅ Success", "Image downloaded successfully in Ultra HD quality!")
        except Exception as e:
            messagebox.showerror("❌ Download Failed", f"Error: {str(e)}")

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp *.tiff"),
                ("All Files", "*.*")
            ]
        )
        if not file_path:
            return
        try:
            self.image = Image.open(file_path)
            self.show_preview(self.image)
            messagebox.showinfo("✅ Success", "Image uploaded successfully!")
        except Exception as e:
            messagebox.showerror("❌ Upload Failed", f"Invalid image file: {str(e)}")

    def show_preview(self, img):
        img_display = img.copy()
        img_display.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(img_display)
        self.preview_label.configure(image=photo, text="", bg="#000")
        self.preview_label.image = photo

    def convert_and_save(self):
        if self.image is None:
            messagebox.showwarning("⚠️ No Image", "Please download or upload an image first!")
            return

        try:
            size_option = self.size_var.get()
            if size_option == "Custom (Enter Width & Height)":
                w = int(self.custom_w.get())
                h = int(self.custom_h.get())
                if w <= 0 or h <= 0:
                    raise ValueError("Size must be positive")
                new_size = (w, h)
            else:
                # Extract size from string like "1920x1080 (Ultra HD)"
                size_str = size_option.split()[0]
                w, h = map(int, size_str.split('x'))
                new_size = (w, h)

            resized_img = self.image.resize(new_size, Image.LANCZOS)

            save_path = filedialog.asksaveasfilename(
                title="Save Converted Image",
                defaultextension=".png",
                filetypes=[
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg"),
                    ("WebP", "*.webp"),
                    ("BMP", "*.bmp"),
                    ("All Files", "*.*")
                ]
            )
            if save_path:
                resized_img.save(save_path)
                messagebox.showinfo("✅ Success", f"Image saved successfully as:\n{save_path}\nSize: {new_size}")
        except ValueError as ve:
            messagebox.showerror("❌ Invalid Input", "Please enter valid numbers for width and height!")
        except Exception as e:
            messagebox.showerror("❌ Conversion Failed", f"Error: {str(e)}")

# === Run Application ===
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedImageTool(root)
    root.mainloop()
