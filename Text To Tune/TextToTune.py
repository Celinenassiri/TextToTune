from tkinter.filedialog import askopenfilename
from tkinter import *
import pyttsx3
import threading
import PyPDF2

# Initialize the TTS engine
engine = pyttsx3.init()

# Flag to control pausing and resuming
is_paused = False
current_line_index = 0  # Track the current line index

window = Tk()
window.title("Book Reader")
window.configure(bg="orange")  # Change the background color here

window.rowconfigure(0, minsize=600, weight=1)
window.columnconfigure(1, minsize=600, weight=1)

# Change the icon of the window (replace 'icon.ico' with your own icon file)
window.iconbitmap('reads.ico')

def open_file():
    file = askopenfilename(title="Select a PDF", filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*")))
    if file:
        try:
            pdf_file = PyPDF2.PdfReader(file)
            page_numbers = len(pdf_file.pages)
            for page in range(page_numbers):
                try:
                    current_page = pdf_file.pages[page]
                    text = current_page.extract_text()
                    if text:
                        txt_edit.insert(END, text)
                except Exception as e:
                    print(f"Error extracting text from page {page}: {e}")
        except Exception as e:
            print(f"Error opening file: {e}")

def read_file():
    global is_paused, current_line_index
    text = txt_edit.get('1.0', END).splitlines()
    while current_line_index < len(text):
        if is_paused:
            engine.stop()
            break
        else:
            engine.say(text[current_line_index])
            engine.runAndWait()
            current_line_index += 1

def start_reading():
    global is_paused
    is_paused = False
    threading.Thread(target=read_file).start()

def pause_reading():
    global is_paused
    is_paused = True

def start_over_reading():
    global is_paused, current_line_index
    is_paused = False
    current_line_index = 0
    threading.Thread(target=read_file).start()

txt_edit = Text(window, bg="lightgray")  # background color of text widget
frm_buttons = Frame(window, relief=RAISED, bd=2, bg="orange")  # background color of frame

btn_open = Button(frm_buttons, text="Open file", command=open_file, bg="darkgray", fg="black", font=('times', 12, 'bold'))
btn_read = Button(frm_buttons, text="Read file", command=start_reading, bg="black", fg="darkgray", font=('times', 12, 'bold'))
btn_pause = Button(frm_buttons, text="Pause", command=pause_reading, bg="white", fg="black", font=('times', 12, 'bold'))
btn_start_over = Button(frm_buttons, text="Start Over", command=start_over_reading, bg="red", fg="white", font=('times', 12, 'bold'))

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_read.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_pause.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_start_over.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()



