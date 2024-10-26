"""
CS5001
Spring 2024
Project -- Tile
Yiming Luo

The entire program implements puzzle games.
This file includes Tile class.
"""

class Tile:
   def __init__(self, center_x, center_y, correct_image_name, current_image_name):
      """
      Function -- __init__
         Initialize a Tile object.
      Parameters:
         center_x -- The x-coordinate of the center of the tile.
         center_y --The y-coordinate of the center of the tile.
         correct_image_name -- The filename of the image for the tile that can display as a complete correct image.
         current_image_name -- The filename of the current image displayed on the tile.
      """
      self.center_x = int(center_x)
      self.center_y = int(center_y)
      self.correct_image_name = correct_image_name
      self.current_image_name = current_image_name
      self.stamp_id = -1