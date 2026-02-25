# PDF Merger Tool in Python (Extended Version)

from tkinter import *
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os

window = Tk()
window.title("PDF Merger Tool")
window.geometry("500x400")
window.config(bg="#E8E8E8")

files = []  # List to store selected files


# Function to refresh the listbox
def refresh_listbox():
    listbox.delete(0, END)
    for f in files:
        listbox.insert(END, os.path.basename(f))


# Function to add files
def add_files():
    selected = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf")]
    )
    for f in selected:
        if f not in files:
            files.append(f)
    refresh_listbox()
    if selected:
        messagebox.showinfo("Files Added", f"{len(selected)} file(s) added successfully!")


# Function to remove selected file
def remove_file():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a file to remove.")
        return
    index = selected[0]
    del files[index]
    refresh_listbox()


# Function to clear all files
def clear_all():
    if messagebox.askyesno("Clear All", "Are you sure you want to remove all files?"):
        files.clear()
        refresh_listbox()


# Function to move file up
def move_up():
    selected = listbox.curselection()
    if not selected or selected[0] == 0:
        return
    i = selected[0]
    files[i - 1], files[i] = files[i], files[i - 1]
    refresh_listbox()
    listbox.select_set(i - 1)


# Function to move file down
def move_down():
    selected = listbox.curselection()
    if not selected or selected[0] == len(files) - 1:
        return
    i = selected[0]
    files[i + 1], files[i] = files[i], files[i + 1]
    refresh_listbox()
    listbox.select_set(i + 1)


# Function to merge PDFs
def merge_pdfs():
    if not files:
        messagebox.showwarning("No Files", "Please add PDF files first!")
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Merged PDF As"
    )

    if not output_path:
        return

    try:
        merger = PdfMerger()
        for pdf in files:
            merger.append(pdf)

        merger.write(output_path)
        merger.close()

        messagebox.showinfo(
            "Success",
            f"PDFs merged successfully!\nSaved as: {os.path.basename(output_path)}"
        )

    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs.\n{e}")


# --- GUI Layout ---

Label(window, text="PDF Merger Tool",
      font=("Arial", 18, "bold"),
      bg="#E8E8E8").pack(pady=10)

frame = Frame(window, bg="#E8E8E8")
frame.pack(pady=10)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(frame, width=50, height=8, yscrollcommand=scrollbar.set)
listbox.pack(side=LEFT, fill=BOTH)

scrollbar.config(command=listbox.yview)


# Buttons for file operations
Button(window, text="Add Files",
       command=add_files, width=20,
       bg="#4CAF50", fg="white").pack(pady=5)

Button(window, text="Remove Selected File",
       command=remove_file, width=20,
       bg="#FF9800", fg="white").pack(pady=5)

Button(window, text="Clear All Files",
       command=clear_all, width=20,
       bg="#9C27B0", fg="white").pack(pady=5)


# Buttons for rearranging order
move_frame = Frame(window, bg="#E8E8E8")
move_frame.pack(pady=10)

Button(move_frame, text="Move Up",
       command=move_up, width=10,
       bg="#2196F3", fg="white").pack(side=LEFT, padx=20)

Button(move_frame, text="Move Down",
       command=move_down, width=10,
       bg="#2196F3", fg="white").pack(side=RIGHT, padx=20)


# Merge and Exit Buttons
Button(window, text="Merge PDFs",
       command=merge_pdfs, width=20,
       bg="#009688", fg="white").pack(pady=10)

Button(window, text="Exit",
       command=window.destroy, width=20,
       bg="#f44336", fg="white").pack(pady=5)

window.mainloop()