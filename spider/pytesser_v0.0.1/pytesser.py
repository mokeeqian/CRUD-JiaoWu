"""OCR in Python using the Tesseract engine from Google
http://code.google.com/p/pytesser/
by Michael J.T. O'Kelly
V 0.0.1, 3/10/07"""

from PIL import Image
import subprocess

import os
import util
import errors


# 这里的可执行文件路径 ***可能需要修改*** ，如果路径格式有变动的话
# Name of executable to be called at command line
if os.name == "nt":
	tesseract_exe_name = '.\\pytesser_v0.0.1\\tesseract' 
	# tesseract_exe_name = 'tesseract' 
elif os.name == "posix":
	tesseract_exe_name = 'tesseract'
	
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp" # Leave out the .txt extension
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation

def call_tesseract(input_filename, output_filename):
	"""Calls external tesseract.exe on input file (restrictions on types),
	outputting output_filename+'txt'"""
	args = [tesseract_exe_name, input_filename, output_filename]
	proc = subprocess.Popen(args)
	retcode = proc.wait()
	if retcode!=0:
		errors.check_for_errors()

def image_to_string(im, cleanup = cleanup_scratch_flag):
	"""Converts im to file, applies tesseract, and fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	try:
		util.image_to_scratch(im, scratch_image_name)
		call_tesseract(scratch_image_name, scratch_text_name_root)
		text = util.retrieve_text(scratch_text_name_root)
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return text

def image_file_to_string(filename, cleanup = cleanup_scratch_flag, graceful_errors=True):
	"""Applies tesseract to filename; or, if image is incompatible and graceful_errors=True,
	converts to compatible format and then applies tesseract.  Fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	try:
		try:
			call_tesseract(filename, scratch_text_name_root)
			text = util.retrieve_text(scratch_text_name_root)
		except errors.Tesser_General_Exception:
			if graceful_errors:
				im = Image.open(filename)
				text = image_to_string(im, cleanup)
			else:
				raise
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return text
	


# 测试方法
if __name__=='__main__':
	im = Image.open('phototest.tif')
	text = image_to_string(im)		# windows 下使用此方法
	print (text)

	# text = image_file_to_string('fonts_test.png', graceful_errors=True)		# Linux 用这个方法
	# print (text)


