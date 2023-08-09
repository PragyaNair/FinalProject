""" 
COMP 593 - Final Project

Description: 
  Viewer application for NASA's Astronomy Picture of the Day (APOD)

Usage:
  python apod_viewer.py
"""
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import os
import ctypes
from datetime import date
import image_lib
import apod_desktop

# Initialize the image cache
apod_desktop.init_apod_cache()
selected_apod_info = None

##########################
# Create the main window
##########################
root = Tk()
root.title("Astronomy Picture of the Day Viewer")
root.geometry('900x800')
root.minsize(850, 600)
root.columnconfigure(0, weight=50)
root.columnconfigure(1, weight=50)
root.rowconfigure(0, weight=100)

# Set the icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.ApodViewer')
root.withdraw()  # Not sure if this is necessary
root.iconbitmap(os.path.join(apod_desktop.script_dir, 'NASA_logo.ico'))
root.deiconify()  # Not sure if this is necessary

#####################
# Create the frames
#####################
# Create the frame to hold the image
frm_image = ttk.Frame(root)
frm_image.columnconfigure(0,weight=100)
frm_image.rowconfigure(0,weight=100)
frm_image.grid(row=0, columnspan=2, padx=10, pady=10, sticky=NSEW)

# Create the frame to hold the image explanation
frm_explanation = ttk.Frame(root)
frm_explanation.columnconfigure(0,weight=100)
frm_explanation.rowconfigure(0,weight=100)
frm_explanation.grid(row=1, columnspan=2, padx=10, sticky=NSEW)

# Create the frame to hold the image select widgets
lblfrm_select = ttk.LabelFrame(root, text="view cached image")
lblfrm_select.grid(row=2, column=0, padx=(10,5), pady=10, sticky=NSEW)

# Create the frame to hold the image download widgets
lblfrm_download = ttk.LabelFrame(root, text="Get More Images")
lblfrm_download.grid(row=2, column=1, padx=(5,10), pady=10, sticky=NSEW)

####################################
# Populate the frames with widgets
####################################
# Populate the image display frame
default_image_path = os.path.join(apod_desktop.script_dir,'NASA_logo.png')
img_apod = Image.open(default_image_path)
image_size = image_lib.scale_image(img_apod.size, (800, 600))
photo_apod = ImageTk.PhotoImage(img_apod.copy().resize(image_size, Image.LANCZOS))
lbl_apod = ttk.Label(frm_image, image=photo_apod)
lbl_apod.grid(row=0)

# Populate the image explanation frame
lbl_explanation = ttk.Label(frm_explanation, wraplength=980)
lbl_explanation.grid(row=0)

# Populate the image select frame
lbl_sel_image = ttk.Label(lblfrm_select, text="Select Image:")
lbl_sel_image.grid(row=0, column=0, padx=(10,5), pady=10)

cbox_sel_image = ttk.Combobox(lblfrm_select, state='readonly', width=45)
cbox_sel_image['values'] = apod_desktop.get_all_apod_titles()
cbox_sel_image.set("Select an image")

def handle_sel_image(event):
    # Get information about the selected APOD from the DB
    global selected_apod_info 
    image_id = event.widget.current() + 1
    selected_apod_info = apod_desktop.get_apod_info(image_id)

    # Display the explanation of the newly selected image
    lbl_explanation['text'] = selected_apod_info['explanation']

    # Display the newly selected APOD image
    global img_apod
    global image_size
    global photo_apod
    image_path = selected_apod_info['file_path']
    img_apod = Image.open(image_path)
    image_size = image_lib.scale_image(img_apod.size, (frm_image.winfo_width(), frm_image.winfo_height()))
    photo_apod = ImageTk.PhotoImage(img_apod.copy().resize(image_size, Image.LANCZOS))
    lbl_apod.configure(image=photo_apod)

    # Enable the 'Set Desktop Background' button 
    btn_set_desktop.state(['!disabled'])

cbox_sel_image.bind('<<ComboboxSelected>>', handle_sel_image)
cbox_sel_image.grid(row=0, column=1, pady=10)

txt_set_desktop = 'Set as Desktop'
btn_set_desktop = ttk.Button(lblfrm_select, text=txt_set_desktop, width=len(txt_set_desktop) + 2)
btn_set_desktop.state(['disabled'])

def handle_set_desktop():
    if selected_apod_info is None: return
    image_lib.set_desktop_background_image(selected_apod_info['file_path'])

btn_set_desktop['command'] = handle_set_desktop
btn_set_desktop.grid(row=0, column=2, padx=10, pady=10)

# Populate the image download frame
lbl_sel_date = ttk.Label(lblfrm_download, text="Select Date:")
lbl_sel_date.grid(row=0, column=0, padx=(10,5), pady=10)

cal_sel_date = DateEntry(lblfrm_download, showweeknumbers=False, locale='en_CA')
cal_sel_date['maxdate'] = date.today()
cal_sel_date['mindate'] = date.fromisoformat("1995-06-16")
cal_sel_date.grid(row=0, column=1, pady=10)

txt_download_image = 'Download Image'
btn_download_image = ttk.Button(lblfrm_download, text=txt_download_image, width=len(txt_download_image) + 2)

def handle_download_image():
    # Get the APOD info for the selected date
    sel_date = cal_sel_date.get_date()
    apod_id = apod_desktop.add_apod_to_cache(sel_date)
    if apod_id != 0:
        # Update the list of available images
        cbox_sel_image['values'] = apod_desktop.get_all_apod_titles()
        cbox_sel_image.current(newindex=apod_id-1)
        cbox_sel_image.event_generate('<<ComboboxSelected>>')

btn_download_image['command'] = handle_download_image
btn_download_image.grid(row=0, column=2, padx=10, pady=10, sticky=W)

# Create event and handler to set width of explanation text to width of window
def handle_resize_window(event):
    lbl_explanation['wraplength'] = frm_explanation.winfo_width()
    new_size = image_lib.scale_image(img_apod.size, (frm_image.winfo_width(), frm_image.winfo_height()))
    # Image.thumbnail  # This might also work

    global image_size
    if new_size != image_size:
        image_size = new_size
        global photo_apod
        photo_apod = ImageTk.PhotoImage(img_apod.copy().resize(image_size, Image.LANCZOS))
        lbl_apod.configure(image=photo_apod)

root.bind("<Configure>", handle_resize_window)

root.mainloop()