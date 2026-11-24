import tkinter as tk

root = tk.Tk()
root.title("My First App")
root.geometry("400x300")

def button_clicked():
    label.config(text="Hello World!")

label = tk.Label(root, text="Welcome!", font=("Arial", 18))
label.pack(pady=20)

button = tk.Button(root, text="Click Me", command=button_clicked)
button.pack()

root.mainloop()