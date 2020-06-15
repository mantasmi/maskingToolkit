# maskingToolkit
Image masking toolkit

	Required packages:
		numpy
		cv2
		tkinter
		os
		tifffile

This toolkit contains basic functionality.
Upon launch a directory can be selected in which all files with a selected extension will be found and indexed.
Immeadiately the masking wndow will appear. 
Keystrokes will trigger image actions. Mouse left click draws (in draw mode) or places points (in polygon mode), right click finishes and draws a polygon from points (in polygon mode)

	Keystrokes:
		M - Alternate between Brush and Polygon mode.
		Q - Confirm changes, proceed to next image, save mask.
		R - Reset mask (Clears selection)
		D - Skip current image
		X - End masking in folder
