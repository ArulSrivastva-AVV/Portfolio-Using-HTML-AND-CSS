import google.generativeai as genai
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
genai.configure(api_key="AIzaSyDuoFVl0ufRSQd5RGr-KD8gmdrkvKvslcs")
model = genai.GenerativeModel("gemini-2.5-pro")
dot_states = ["Loading.", "Loading..", "Loading..."]
dot_index = 0
loading_active = False
def start_loading():
    global loading_active
    loading_active = True
    animate_loading()
def animate_loading():
    global dot_index
    if loading_active:
        loading_label.config(text=dot_states[dot_index % len(dot_states)])
        dot_index += 1
        root.after(500, animate_loading)
def stop_loading():
    global loading_active
    loading_active = False
    loading_label.config(text="")
def check_ecofriendly():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL!")
        return
    start_loading()
    root.after(100, lambda: process_url(url))
def process_url(url):
    prompt_check = f"CHECK THE COMPONENTS OR MATERIAL OF PRODUCT ON THE WEBPAGE {url} AND ANSWER WHETHER IT IS ECOFIENDLY OR NOT. If it is eco-friendly write 'product is ecofriendly', if not write 'non-ecofriendly'. Nothing else should be the output."
    try:
        response_check = model.generate_content(prompt_check)
        result_text = response_check.text.strip().upper()
        if "NON-ECOFRIENDLY" in result_text:
            result_label.config(text=result_text, foreground="red", anchor="center", justify="center")
            prompt_alt = f"Suggest only the name of an eco-friendly alternative product for the product on the webpage {url}. Only output the name, nothing else."
            response_alt = model.generate_content(prompt_alt)
            alt_name = response_alt.text.strip().upper()
            alt_title_label.config(text="ALTERNATIVE PRODUCT:", foreground="green")
            alt_label.config(text=alt_name, foreground="green", anchor="center", justify="center")
        else:
            result_label.config(text=result_text, foreground="green", anchor="center", justify="center")
            alt_title_label.config(text="")
            alt_label.config(text="")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        stop_loading()






        
root = tk.Tk()
root.title("GOECO")
root.state("zoomed") 
root.configure(bg="black")
try:
    logo_img = Image.open("goecologo.png")
    width, height = logo_img.size
    new_width = int(width * 1.5)
    new_height = int(height * (new_width / width))
    logo_img = logo_img.resize((new_width, new_height), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_photo, bg="black", borderwidth=0, highlightthickness=0)
    logo_label.pack(pady=(0, 10))
except FileNotFoundError:
    messagebox.showwarning("Logo Missing", "Logo file 'goecologo.png' not found. Please add it to the same folder.")
url_frame = tk.Frame(root, bg="black")
url_frame.pack(pady=10)
tk.Label(url_frame, text="Enter Product URL:", font=("Segoe UI", 20, "bold"), bg="black", fg="white").pack(side=tk.LEFT, padx=5)
url_entry = tk.Entry(url_frame, width=48, font=("Segoe UI", 14))
url_entry.pack(side=tk.LEFT, padx=5, ipady=8)
ecoify_btn = tk.Button(root, text="ECOIFY", command=check_ecofriendly, font=("Segoe UI", 14, "bold"),
                       bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white",
                       padx=30, pady=12, relief="solid", bd=0, highlightthickness=2)
ecoify_btn.config(width=20)
ecoify_btn.pack(pady=15)
loading_label = tk.Label(root, text="", font=("Segoe UI", 24, "italic"), bg="black", fg="white")
loading_label.pack(pady=5)
result_label = tk.Label(root, text="", font=("Segoe UI", 36, "bold"), bg="black", fg="white", wraplength=800, justify="center")
result_label.pack(pady=10)
alt_title_label = tk.Label(root, text="", font=("Segoe UI", 22, "bold"), bg="black", fg="green", wraplength=800, justify="center")
alt_title_label.pack(pady=(10, 0))
alt_label = tk.Label(root, text="", font=("Segoe UI", 28, "bold"), bg="black", fg="green", wraplength=800, justify="center")
alt_label.pack(pady=5)
disclaimer_label = tk.Label(root, text="THE RESULTS MIGHT BE INACCURATE", font=("Segoe UI", 14, "italic"),
                            bg="black", fg="gray")
disclaimer_label.pack(side=tk.BOTTOM, pady=10)


root.mainloop()

