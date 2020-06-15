# Dataset labeling toolkit v0.1 - basic tools
#
# Developed by Mantas Mikalauskis
# Copyright

# File input/output/conversion/storing operations

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import cv2


class FileOperations:

    class Directory:
        def __init__(self):
            root = tk.Tk()
            root.withdraw()

            self.file_path = filedialog.askdirectory()
            self.all_flies_in_dir = []
            self.all_file_count = 0
            self.current_file = 0
            self.extension = ""
            self.save_extension = ".png"

        def list_all_files(self, extension):
            # List all files with the specified extension
            self.extension = extension

            for file in os.listdir(self.file_path):
                if file.endswith(extension):
                    file_pure_name = os.path.splitext(file)[0]
                    file_dirty_name = os.path.join(self.file_path, file)

                    print("Detected matching file: {}".format(file_dirty_name))

                    self.all_flies_in_dir.append([file_pure_name, file_dirty_name, file])

            if len(os.listdir(self.file_path)) == 0:
                print("No files found!")
                messagebox.showwarning(title="Masking Toolkit",
                                          message="No files with extension '{}' found.".format(extension))
            else:
                self.all_file_count = len(os.listdir(self.file_path))

        def count_files(self):
            return self.all_file_count

        def provide_files(self):
            return self.all_flies_in_dir

        def navigate_files(self, position):
            if position == "NEXT":
                self.current_file = self.current_file + 1
            if position == "BACK":
                self.current_file = self.current_file - 1

        def open_image(self):
            # Open imported image to array

            file = self.all_flies_in_dir[self.current_file][1]
            print("Opening file: {}".format(file))
            img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

            return img

        def save_image(self, img, save_extension):
            # Save image to file destination with changed name

            self.save_extension = save_extension

            #self.save_extension = ".jpeg" # Force jpeg output
            file = self.all_flies_in_dir[self.current_file][0]
            print("Saving with filename: {}".format(file))
            full_destination = os.path.join(self.file_path, file + self.save_extension)
            print("Saving file: {}".format(full_destination))
            cv2.imwrite(full_destination, img)
            if self.current_file < self.all_file_count:
                self.current_file = self.current_file + 1
                print("Proceeding to next...")
            else:
                print("End of pictures.")
                messagebox.showinfo(title="Masking Toolkit", message="Completed masking in this directory.")

        def __del__(self):
            print("Directory is under destruction...")

    def __del__(self):
        print("FileOperations is under destruction...")
