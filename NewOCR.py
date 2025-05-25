import tkinter as tk
from googletrans import Translator

# Function to translate text
def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    target_lang = lang_var.get()

    if text and target_lang:
        translator = Translator()
        translated = translator.translate(text, src='en', dest=target_lang)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)

# Create main application window
root = tk.Tk()
root.title("Language Translator")
root.geometry("400x400")

# Label and text input
tk.Label(root, text="Enter text in English:").pack()
input_text = tk.Text(root, height=5, width=50)
input_text.pack()

# Dropdown menu for language selection
tk.Label(root, text="Select Language:").pack()
lang_var = tk.StringVar(root)
lang_var.set("ta")  # Default language is Tamil

languages = {
    "Tamil": "ta",
    "Telugu": "te",
    "Hindi": "hi"
}

lang_menu = tk.OptionMenu(root, lang_var, *languages.values())
lang_menu.pack()

# Translate button
translate_btn = tk.Button(root, text="Translate", command=translate_text)
translate_btn.pack()

# Output text area
tk.Label(root, text="Translated Text:").pack()
output_text = tk.Text(root, height=5, width=50)
output_text.pack()

# Run the Tkinter event loop
root.mainloop()
