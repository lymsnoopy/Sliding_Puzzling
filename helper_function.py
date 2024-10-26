"""
CS5001
Spring 2024
Project -- helper functions
Yiming Luo

The entire program implements puzzle games.
This file includes helper functions.
"""

import turtle
import os
import datetime
import inspect

def add_to_project_root_directory(directory):
   """
   Function -- add_to_project_root_directory
      Add root directory and needed directory together.
   Parameters:
      directory -- The directory we needed.
   Returns:
      The path of the new directory.
   """
   file_path = os.path.realpath(__file__)
   # Find the root directory.
   project_root_directory = os.path.dirname(file_path)
   # Join the directory that needed.
   directory_path = os.path.join(project_root_directory, directory)
   return directory_path


def log_error(error, function_name):
   """
   Function -- log_error
      Log errors to a file.
   Parameters:
      error: The error message to be logged.
   """
   current_time = datetime.datetime.now()
   current_time_str = current_time.strftime("%A %m/%d/%y %H:%M:%S %Y")
   # Record the error in a file.
   change_directory("")
   with open ("5001_puzzle.err", "a",) as error_log:
      error_log.write(f"{current_time_str}:{error} Location:{function_name}\n")


def change_directory(directory):
   """
   Function -- change_direcitory
      Change the current working directory to the specified directory.
   Parameters:
      directory -- The directory to change to.
   """
   try:
      directory_path = add_to_project_root_directory(directory)
      os.chdir(directory_path)
   except FileNotFoundError:
      current_function = inspect.getframeinfo(inspect.currentframe()).function
      log_error(f"The system cannot find the specified file.", current_function)
   except Exception as e: # e is the name of the error.
        current_function = inspect.getframeinfo(inspect.currentframe()).function
        log_error(f"Error in changing directory: {str(e)}.", current_function)


def add_image(x, y, shape_name):
   """
   Funciton -- add_image
      Add the image to the srcreen.
   Parameters:
      x -- The x coordinate of the center of the image.
      y -- The y coordinate of the center of the image.
      shape_name -- The name of the image.
   Return:
      stamp_id -- A specific id for adding the image.
   """
   turtle.penup()
   turtle.goto(x, y)
   
   try:
      turtle.register_shape(shape_name)
      turtle.shape(shape_name)
      stamp_id = turtle.stamp()
      return stamp_id
   except turtle.TurtleGraphicsError:
      current_function = inspect.getframeinfo(inspect.currentframe()).function
      log_error(f"Error in adding {shape_name}.", current_function)
   except Exception as e: # e is the name of the error.
        current_function = inspect.getframeinfo(inspect.currentframe()).function
        log_error(f"Error in adding images: {str(e)}.", current_function)
   

def draw_rectangle(pen_size, start_x, start_y, color, up_down_length, left_right_length):
   """
   Function -- draw_rectangle
      Use turtle to draw rectangle shape.
   Parameters:
      pen_size -- Turtle pen size.
      start_x -- The x coordinate of the point that starts to be drawn.
      start_y -- The y coordinate of the point that starts to be drawn.
      color -- Pen color.
      up_down_length -- One side of the shape length.
      left_right_length -- Another side of the shape length.
   """
   turtle.pensize(pen_size)
   turtle.penup()
   turtle.goto(start_x, start_y)
   turtle.color(color)
   turtle.pendown()
   turtle.right(90)
   turtle.forward(up_down_length)
   turtle.right(90)
   turtle.forward(left_right_length)
   turtle.right(90)
   turtle.forward(up_down_length)
   turtle.right(90)
   turtle.forward(left_right_length)