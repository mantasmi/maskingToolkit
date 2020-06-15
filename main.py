# Dataset labeling toolkit v0.1 - basic tools
#
# For masking images in directory manually using a brush paint tool.
# Saves image mask in the same directory with a selected extension.
# It must be different than the input extension.
#
# Developed by Mantas Mikalauskis
# Copyright

from tkinter import *
from tkinter import ttk
import paint
import fileOperations
import numpy as np


def begin_masking():
    # Run process for DIR selection and required functions
    ImageOperations = paint.Paint()
    FileOperations = fileOperations.FileOperations.Directory()

    input_extension = select_export_extension_combo.get()
    print("Selected input extension: {}".format(input_extension))

    FileOperations.list_all_files(extension=input_extension)

    all_images = FileOperations.count_files()

    for image in FileOperations.provide_files():
        original = FileOperations.open_image()

        name_of_current_file = FileOperations.all_flies_in_dir[FileOperations.current_file][2]
        mask = ImageOperations.execute_paint(original=original, current_name=name_of_current_file)
        if invert:
            mask = ImageOperations.invert_mask_colors()
        if grayscale:
            mask = ImageOperations.grayscale_mask_colors()

        if not ImageOperations.skip:
            # Do save skip
            save_extension = ".png"
            if save_in_tiff:
                save_extension = ".tiff"
            else:
                save_extension = ".png"

            FileOperations.save_image(img=mask, save_extension=save_extension)
        else:
            FileOperations.current_file = FileOperations.current_file + 1

        if ImageOperations.end_after_this:
            break


### GUI ###

def onClose():
    root.quit()
    root.destroy()
    sys.exit()

root = Tk(className='Masking Toolkit [Basic]')
root.protocol("WM_DELETE_WINDOW", onClose)

content = ttk.Frame(root)

dir_select_btn = ttk.Button(content, text="DIR select", command=begin_masking)
stop_annotations_btn = ttk.Button(content, text="Stop Annotating")

extension_combo_label = ttk.Label(content, text="Input extension: ")
select_export_extension_combo = ttk.Combobox(content,
                                             values=[
                                                 ".JPG",
                                                 ".tiff",
                                                 ".png",
                                                 ".bmp"])

select_export_extension_combo.current(0)

invert = BooleanVar()
save_in_tiff = BooleanVar()
grayscale = BooleanVar()
grayscale.set(True)
invert.set(True)
save_in_tiff.set(True)

invert_checkbtn = ttk.Checkbutton(content, text="Invert mask", variable=invert, onvalue=True)
save_in_tiff_checkbtn = ttk.Checkbutton(content, text="Save in TIFF", variable=save_in_tiff, onvalue=True)
grayscale_checkbtn = ttk.Checkbutton(content, text="Grayscale mask", variable=grayscale, onvalue=True)

content.grid(column=0, row=0)

dir_select_btn.grid(column=1, row=1)
stop_annotations_btn.grid(column=2, row=1)
extension_combo_label.grid(column=1, row=2)
select_export_extension_combo.grid(column=2, row=2)
invert_checkbtn.grid(column=1, row=3)
save_in_tiff_checkbtn.grid(column=2, row=3)
grayscale_checkbtn.grid(column=1, row=4)

root.mainloop()
