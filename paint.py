# Dataset labeling toolkit v0.1 - basic tools
#
# Developed by Mantas Mikalauskis
# Copyright

# Paint functionality for masking

import numpy as np
import cv2 as cv


class Paint:
    drawing = False  # true if mouse is pressed
    mask = []
    preview = []
    combined_pic = []
    original = []
    drawBrush = 10  # brush size default value
    skip = False
    end_after_this = False
    original_shape = []
    current_name = ""
    draw_mode = "BRUSH"  # Or POLYGON
    all_coordinates = []

    def combine_images(self, the_mask, the_original):
        # Combine images to have transparent overlay preview of mask on original
        amount = 1  # Transparency factor or org
        amount2 = 0.7  # Transparency of mask

        image_new = cv.addWeighted(the_original, amount, the_mask, amount2, 0)

        font = cv.FONT_HERSHEY_SIMPLEX
        first_line = (20, 20)
        second_line = (20, 40)
        third_line = (20, 60)
        font_scale = 0.7
        font_color = (60, 100, 255)
        line_type = 2

        cv.putText(image_new, 'Current IMG: {}'.format(self.current_name),
                   first_line,
                   font,
                   font_scale,
                   font_color,
                   line_type)

        cv.putText(image_new, 'Mode: {}'.format(self.draw_mode),
                   second_line,
                   font,
                   font_scale,
                   font_color,
                   line_type)

        cv.putText(image_new, 'Q - Confirm  R - Reset  D - Skip  M - Switch mode  X - End session',
                   third_line,
                   font,
                   font_scale,
                   font_color,
                   line_type)

        return image_new

    def new_brush_size(self, val):
        self.drawBrush = val

    def draw_circle(self, event, x, y, flags, param):
        # mouse callback function
        if event == cv.EVENT_LBUTTONDOWN:
            if not self.drawing:
                self.drawing = True

            if self.drawing:
                cv.circle(self.mask, (x, y), self.drawBrush, (255, 255, 255), -1)

                self.combined_pic = self.combine_images(self.mask, self.original)

                cv.imshow('Paint over the required region', self.combined_pic)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing:
                cv.circle(self.mask, (x, y), self.drawBrush, (255, 255, 255), -1)

                self.combined_pic = self.combine_images(self.mask, self.original)

                cv.imshow('Paint over the required region', self.combined_pic)

        elif event == cv.EVENT_LBUTTONUP:
            if self.drawing:
                self.drawing = False

    def contour_finder(self, contour_finder_image):
        # Find contours in image

        contour_finder_image = cv.cvtColor(contour_finder_image, cv.COLOR_BGR2GRAY)

        ret, gray = cv.threshold(contour_finder_image, 127, 255, 0)

        cnt, hier = cv.findContours(gray, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        return cnt

    def draw_filled_in_contour(self, contours_to_draw, image_to_draw_on):
        # Draw polygon from contours

        cv.drawContours(image_to_draw_on, contours_to_draw, 0, (255, 255, 255), cv.FILLED)

        return image_to_draw_on

    def draw_polygon(self, event, x, y, flags, param):
        # mouse callback function

        if event == cv.EVENT_LBUTTONDOWN:
            if not self.drawing:
                self.drawing = True

            if self.drawing:
                point_draw_mask = np.zeros_like(self.mask)
                cv.circle(point_draw_mask, (x, y), self.drawBrush, (255, 255, 255), -1)
                self.all_coordinates.append([x, y])
                self.combined_pic = self.combine_images(self.mask, self.original)
                self.combined_pic = self.combine_images(point_draw_mask, self.original)

                cv.imshow('Paint over the required region', self.combined_pic)

        elif event == cv.EVENT_RBUTTONDOWN:
            if self.drawing:
                self.drawing = False
                print("Length of all coords: {}".format(len(self.all_coordinates)))
                if len(self.all_coordinates) >= 3:
                    # Construct polygon from points in all_coordinates

                    self.all_coordinates = np.array(self.all_coordinates, np.int32)
                    pts = self.all_coordinates.reshape((-1, 1, 2))
                    point_draw_mask = np.zeros_like(self.mask)

                    cv.polylines(point_draw_mask, [pts], True, (255, 255, 255))

                    contours_of_polygon = self.contour_finder(point_draw_mask)

                    self.mask = self.draw_filled_in_contour(contours_of_polygon, self.mask)

                    self.combined_pic = self.combine_images(self.mask, self.original)

                    cv.imshow('Paint over the required region', self.combined_pic)

                    self.all_coordinates = []
                    del self.all_coordinates[:]

    def determine_draw(self, event, x, y, flags, param):
        if self.draw_mode == "BRUSH":
            self.draw_circle(event, x, y, flags, param)
        if self.draw_mode == "POLYGON":
            self.draw_polygon(event, x, y, flags, param)

    def enable_polygon(self):
        self.drawBrush = 2
        self.draw_mode = "POLYGON"
        self.all_coordinates = []
        del self.all_coordinates[:]
        self.combined_pic = self.combine_images(self.mask, self.original)
        cv.imshow('Paint over the required region', self.combined_pic)

    def enable_brush(self):
        self.drawBrush = 10
        self.draw_mode = "BRUSH"
        self.all_coordinates = []
        del self.all_coordinates[:]
        self.combined_pic = self.combine_images(self.mask, self.original)
        cv.imshow('Paint over the required region', self.combined_pic)

    def resize(self, image_to_resize, amount):
        scale_percent = amount  # percent of original size
        width = int(image_to_resize.shape[1] * scale_percent / 100)
        height = int(image_to_resize.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv.resize(image_to_resize, dim, interpolation=cv.INTER_AREA)

        return resized

    def return_resize(self, image_to_resize):
        print(self.original_shape)
        resized = cv.resize(image_to_resize, self.original_shape, interpolation=cv.INTER_AREA)

        return resized

    def execute_paint(self, original, current_name):
        # Take source image and perform masking on it
        # press r to reset mask

        self.current_name = current_name

        self.original_shape = (original.shape[1], original.shape[0])
        original = self.resize(original, 30)

        self.mask = np.zeros_like(original)
        self.combined_pic = original.copy()
        self.combined_pic = self.combine_images(self.mask, self.combined_pic)
        self.preview = original.copy()
        self.original = original.copy()

        cv.namedWindow('Paint over the required region')
        cv.moveWindow('Paint over the required region', 40, 30)
        cv.createTrackbar('Brush Size', 'Paint over the required region', self.drawBrush, 100, self.new_brush_size)

        cv.setMouseCallback('Paint over the required region', self.determine_draw)

        self.skip = False
        self.end_after_this = False

        while 1:
            cv.imshow('Paint over the required region', self.combined_pic)
            k = cv.waitKey(1) & 0xFF
            if k == ord('r'):
                self.mask = np.zeros_like(original)
                self.preview = original.copy()
                self.combined_pic = self.combine_images(self.mask, self.original)
                cv.imshow('Paint over the required region', self.combined_pic)
            if k == ord('q'):
                break
            if k == ord('d'):
                if not self.skip:
                    self.skip = True
                break
            if k == ord('x'):
                self.end_after_this = True
                break
            if k == ord('m'):
                if self.draw_mode == "BRUSH":
                    self.enable_polygon()
                    print("Polygon enabled.")
                elif self.draw_mode == "POLYGON":
                    self.enable_brush()
                    print("Brush enabled.")

        cv.destroyAllWindows()

        self.mask = self.return_resize(self.mask)
        return self.mask

    def invert_mask_colors(self):
        # Invert colors in mask image

        self.mask = cv.bitwise_not(self.mask)
        print("Inverting mask...")

        return self.mask

    def grayscale_mask_colors(self):
        # Convert to grayscale

        self.mask = cv.cvtColor(self.mask, cv.COLOR_BGR2GRAY)

        return self.mask

    def __del__(self):
        print("Paint is under destruction...")
