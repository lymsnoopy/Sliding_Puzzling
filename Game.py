"""
CS5001
Spring 2024
Project -- Game
Yiming Luo

The entire program implements puzzle games.
This file includes Game class.
"""

import turtle
import os
import random
import math
import inspect
from pathlib import Path
from Tile import Tile
import helper_function

class Game:
   def __init__(self):
      """
      Function -- __init__
         Initialize a Game object.
      """
      self.tiles = []
      self.number_of_tiles = -1
      self.number_per_row = -1
      self.tile_size_length = -1
      self.image_names=[]
      self.current_blank_tile_idx = -1
      self.thumbnail_name = ""
      self.game_name = ""
      self.thumbnail_stamp_id = -1
      self.num_of_chances = 0
      self.current_chance_number = 0
      self.t = turtle.Turtle()
      self.t.hideturtle()
      self.splash_screen_stamp_id = -1
      self.lose_image_stamp_id = -1
      self.file_error_stamp_id = -1
      self.puz_files = []
      self.thumbnail_path = []
      self.image_path = []
      self.player_name = ""
      self.t2 = turtle.Turtle()
      self.t2.hideturtle()


   def search_puz_file(self):
      """
      Function -- search_puz_file
         Find any .puz files in the root directory and store them in a list.
      Parameters:
         self -- The Game object.
      Returns:
         list -- A list containing the names of .puz files found in the root directory.
      """
      helper_function.change_directory("")
      project_root_directory = helper_function.add_to_project_root_directory("")
      # Get a list of all files in the root directory.
      all_files = os.listdir(project_root_directory)
      # Iterate through the files in the root directory.
      for file_name in all_files:
         if file_name.endswith(".puz"):
            self.puz_files.append(file_name)
      return self.puz_files
   

   def splash_screen(self):
      """
      Function -- splash_screen
         Display the splash screen image and proceed to set player name and chances after a delay.
      Parameters:
         self -- The Game object.
      """
      helper_function.change_directory("Resources")
      self.splash_screen_stamp_id = helper_function.add_image(0, 0, "splash_screen.gif")
      # Set a timer to call set_name_and_chances after a delay of 4000 milliseconds (4 seconds).
      turtle.ontimer(self.set_name_and_chances, 4000)
   

   def clear_stamp(self, stamp_id):
      """
      Function -- clear_stamp
         Clear the specific image on the scrren.
      Parameters:
         self -- The Game object.
      """
      turtle.clearstamp(stamp_id)


   def set_chances(self):
      """
      Function -- set_chances
         The players select the number of moves to unscramble the puzzle.
      Parameters:
         self -- The Game object.
      """
      self.num_of_chances = int(turtle.numinput(
         "5001 Puzzle Slides - Moves", "Enter the number of moves (chances) you want(5-200)?",
         50,
         minval=5,
         maxval=200
      ))
   

   def set_player_name(self):
      """
      Function -- set_player_name
         The players input their name to the game through a pop-up window.
      Parameters:
         self -- The Game object.
      Return:
         The name of the player.
      """
      while True:
         self.player_name = turtle.textinput("CS5001 Puzzle Slide", "Your Name:")
         if self.player_name != "":
            break

   def start_game(self):
      """
      Function -- start_game
         Start the game by setting up the game interface and loading a puzzle.
      Parameters:
         self -- The Game object.
      """
      turtle.clearstamps()

      # Draw rectangles for different sections of the game interface
      helper_function.draw_rectangle(8, 112, 371, "black", 550, 480) # Main game area
      helper_function.draw_rectangle(8, 402, 371, "blue", 550, 240) # Thumbnail and Leaderboard display area
      helper_function.draw_rectangle(8, 402, -229, "black", 100, 770) # Control button area
      helper_function.change_directory("Resources")

      # Add images for control buttons
      helper_function.add_image(352, -278, "quitbutton.gif")
      helper_function.add_image(262, -278, "loadbutton.gif")
      helper_function.add_image(172, -278, "resetbutton.gif")
      self.load("mario.puz")
      self.setup_game_interface()
      turtle.onscreenclick(self.handle_click)


   def set_name_and_chances(self):
      """
      Function -- set_name_and_chances
         Call functions to set name and chances and start the game.
      Parameters:
         self -- The Game object.
      """
      self.clear_stamp(self.splash_screen_stamp_id)
      self.set_player_name()
      self.set_chances()
      self.start_game()
   

   def split_info_from_puz(self, line):
      """
      Function -- split_info_from_puz
         Read the .puz file and get information from the line.
      Parameters:
         self -- The Game object.
         line -- The specific line that want to split.
      Return:
         the information split from the line.
      """
      line_split = line.strip().split(" ")
      line_element = line_split[1].split("/")
      return line_element


   def read_puz(self, name):
      """
      Function -- read_puz
         Read the .puz file and get information.
      Parameters:
         self -- The Game object.
         name -- The .puz name.
      """
      self.image_names = []
      helper_function.change_directory("")
      try:
         with open(name, mode='r') as puz_file:
            # Read the first line to get the game name.
            first_line = puz_file.readline()
            self.game_name = first_line.strip().split(": ")[1]
            # Read the second line to get the number of tiles.
            second_line = puz_file.readline()
            self.number_of_tiles = int(second_line.strip().split(": ")[1])
            self.number_per_row = int(math.sqrt(self.number_of_tiles))
            # Read the third line to get the tile size length.
            third_line = puz_file.readline()
            self.tile_size_length = int(third_line.strip().split(": ")[1])
            # Read the fourth line to get thumbnail information.
            thumbnail_line = puz_file.readline()
            thumbnail_info = self.split_info_from_puz(thumbnail_line)
            self.thumbnail_name = thumbnail_info[-1]
            self.thumbnail_path = thumbnail_info[:-1]
            # Read the remaining lines to get image names and paths.
            lines_puz_file = puz_file.readlines()
         for line_puz_file in lines_puz_file:
            line_puz_info = self.split_info_from_puz(line_puz_file)
            image = line_puz_info[-1]
            self.image_names.append(image)
            self.image_path = line_puz_info[:-1]

      except FileNotFoundError:
        current_function = inspect.getframeinfo(inspect.currentframe()).function
        helper_function.log_error(f"File {name} not found.", current_function)
      except OSError:
         current_function = inspect.getframeinfo(inspect.currentframe()).function
         helper_function.log_error(f"Error in reading {name} file.", current_function)
      except Exception as e: # e is the name of the error.
        current_function = inspect.getframeinfo(inspect.currentframe()).function
        helper_function.log_error(f"Error: {str(e)}.", current_function)


   def load(self, name):
      """
      Function -- load
         shuffle the puzzle and match the name with the puzzle position.
      Parameters:
         self -- The Game object.
      """
      self.read_puz(name)
      self.tiles = []

      # Shuffle image names to randomize tile positions
      shuffled_image_names = self.image_names.copy()
      for original_position in range(len(self.image_names)):
         new_postion = random.randint(0, len(self.image_names) - 1)
         temporary = shuffled_image_names[new_postion]
         shuffled_image_names[new_postion] = shuffled_image_names[original_position]
         shuffled_image_names[original_position] = temporary

      # Find center_x and center_y of every tile, and define correct_image_name and current_image_name of every tile.
      for idx_number_list in range(self.number_of_tiles):
         center_x = -350 + 19 + (self.tile_size_length + 10) * (idx_number_list % self.number_per_row) + self.tile_size_length / 2
         center_y = 280 - 42 - (self.tile_size_length + 7) * (idx_number_list // self.number_per_row) + self.tile_size_length / 2
         correct_image_name = self.image_names[idx_number_list]
         current_image_name = shuffled_image_names[idx_number_list]
         if current_image_name == "blank.gif":
            self.current_blank_tile_idx = idx_number_list
         tile = Tile(center_x, center_y, correct_image_name, current_image_name)
         self.tiles.append(tile)


   def initialize_leaderboard_file(self):
      """
      Function -- initialize_leaderboard_file
         Open the leaderboard file and write information into the file.
      Parameters:
         self -- The Game object.
      Returns:
         str -- Leaders:\n\n
      """
      with open("leaderboard.txt", "w") as leaderboard_file:
         leaderboard_file.write(f"Leaders:\n\n")
      return f"Leaders:\n\n"
   

   def load_leaderboard(self):
      """
      Function -- load_leaderboard
         Refresh the leaderboard on screen.
      Parameters:
         self -- The Game object.
      """
      self.t2.clear()
      helper_function.change_directory("")
      try:
         leaderboard_file_path = helper_function.add_to_project_root_directory("leaderboard.txt")
         if Path(leaderboard_file_path).is_file(): # File exists.
            # Save file content.
            with open("leaderboard.txt", "r") as leaderboard_file:
               content = leaderboard_file.read()
            
            if content == "":
               content = self.initialize_leaderboard_file()
         
         else:
            # File doesn't exist, create file, initialize file, save content.
            content = self.initialize_leaderboard_file()

      except OSError:
         current_function = inspect.getframeinfo(inspect.currentframe()).function
         helper_function.log_error(f"Error in operating 'leaderboard.txt'.", current_function)
      except Exception as e: # e is the name of the error.
        current_function = inspect.getframeinfo(inspect.currentframe()).function
        helper_function.log_error(f"Error: {str(e)}.", current_function)

      number_of_lines = content.count('\n') + 1
      t2_y_coordinate = 250 - number_of_lines * 20
      self.t2.penup()
      self.t2.goto(250, t2_y_coordinate)
      self.t2.color("blue")
      self.t2.write(content, align="center", font=('Arial', 18, 'normal'))

   
   def add_directories_and_change_paths(self, paths):
      """
      Function -- add_directories_and_change_paths
         add needed directories to original path and change the path.
      Parameters:
         self -- The Game object.
         paths -- several needed directories.
      """
      needed_directory = ""
      for directory in paths:
         needed_directory = os.path.join(needed_directory, directory)
      helper_function.change_directory(needed_directory)


   def setup_game_interface(self):
      """
      Function -- setup_game_interface
         Add puzzle tile images and thumbnail image on screen.
      Parameters:
         self -- The Game object.
      """
      self.load_leaderboard()
      self.add_directories_and_change_paths(self.thumbnail_path)
      self.thumbnail_stamp_id = helper_function.add_image(402, 371, self.thumbnail_name)
      self.add_directories_and_change_paths(self.image_path)

      # Add image stamp for each tile at its respective position
      for idx_tiles in range(len(self.tiles)):
         stamp_id = helper_function.add_image(self.tiles[idx_tiles].center_x, self.tiles[idx_tiles].center_y, self.tiles[idx_tiles].current_image_name)
         self.tiles[idx_tiles].stamp_id = stamp_id


   def clear_all_tile_stamp(self):
      """
      Function -- clear_all_tile_stamp
         Clear all tile images on screen.
      Parameters:
         self -- The Game object.
      """
      for tile in self.tiles:
         turtle.clearstamp(tile.stamp_id)


   def reset(self):
      """
      Function -- reset
         Reset all tile images to the correct position to form a whole complete image.
      Parameters:
         self -- The Game object.
      """
      self.clear_all_tile_stamp()
      self.add_directories_and_change_paths(self.image_path)

      # Set the current image name of each tile to its correct image name and add the image.
      for idx_tiles in range(len(self.tiles)):
         self.tiles[idx_tiles].current_image_name = self.tiles[idx_tiles].correct_image_name 
         stamp_id = helper_function.add_image(self.tiles[idx_tiles].center_x, self.tiles[idx_tiles].center_y, self.tiles[idx_tiles].current_image_name)
         self.tiles[idx_tiles].stamp_id = stamp_id

         # Update the current_blank_tile_idx if the tile is a blank tile.
         if self.tiles[idx_tiles].current_image_name == "blank.gif":
            self.current_blank_tile_idx = idx_tiles
   

   def quit(self):
      """
      Function -- quit
         Quit the game.
      Parameters:
         self -- The Game object.
      """
      helper_function.change_directory("Resources")
      helper_function.add_image(0, 0, 'quitmsg.gif')
      turtle.ontimer(turtle.bye, 1500)


   def clear_file_error_stamp(self):
      """
      Function -- clear_file_error_stamp
         Clear the file error image.
         Set up to enable the use of turtle.ontimer() function. 
      Parameters:
         self -- The Game object.
      """
      self.clear_stamp(self.file_error_stamp_id)


   def check_puz_file_validity(self, name):
      """
      Function -- check_puz_file_validity
         Check the validity of puz file.
      Parameters:
         self -- The Game object.
         name -- The puz file name.
      Return:
         Boolean -- True or False
      """
      helper_function.change_directory("")
      try:
         with open(name, mode='r') as puz_file:
            # Read the first line.
            puz_file.readline()
            # Read the second line to get the number of tiles.
            second_line = puz_file.readline()
            number_of_tiles = int(second_line.strip().split(": ")[1])
            number_per_row = math.sqrt(number_of_tiles)
            # Read the third line.
            puz_file.readline()
            # Read the fourth line.
            puz_file.readline()
            # Read the remaining lines.
            lines_puz_file = puz_file.readlines()
         
         # Check whether the puzzle file is malformed.
         if ((number_of_tiles != len(lines_puz_file)) 
            or ((number_per_row != 2.0) and (number_per_row != 3.0) and (number_per_row != 4.0))
         ):
            current_function = inspect.getframeinfo(inspect.currentframe()).function
            helper_function.log_error(f"Malformed puzzle file.", current_function)
            return False

      except FileNotFoundError:
         current_function = inspect.getframeinfo(inspect.currentframe()).function
         helper_function.log_error(f"File {name} not found.", current_function)
         return False
      except OSError:
         current_function = inspect.getframeinfo(inspect.currentframe()).function
         helper_function.log_error(f"Error in reading {name} file.", current_function)
         return False
      except Exception as e: # e is the name of the error.
        current_function = inspect.getframeinfo(inspect.currentframe()).function
        helper_function.log_error(f"Error: {str(e)}.", current_function)
        return False
      return True


   def load_another_game(self):
      """
      Function -- load_another_game
         Load another game selected by the player.
      Parameters:
         self -- The Game object.
      """
      # Prompt the player to enter the name of the puzzle they want to load.
      selected_puzzle = turtle.textinput(
         "Load Puzzle", 
         "Enter the name of the puzzle you wish to load. Choices are:\n" + '\n'.join(self.puz_files))
      
      # Check if the selected puzzle exists in the list of available puzzles and check the validity of puz file.
      if selected_puzzle in self.puz_files and self.check_puz_file_validity(selected_puzzle):
         turtle.clearstamp(self.thumbnail_stamp_id)
         self.clear_all_tile_stamp()
         self.load(selected_puzzle)
         self.setup_game_interface()
         self.current_chance_number = 0
         self.update_player_move()
      else:
         current_function = inspect.getframeinfo(inspect.currentframe()).function
         helper_function.log_error(f"Puzzle {selected_puzzle} not found.", current_function)
         helper_function.change_directory("Resources")
         self.file_error_stamp_id = helper_function.add_image(0, 0, "file_error.gif")
         turtle.ontimer(self.clear_file_error_stamp, 2000)


   def update_player_move(self):
      """
      Function -- update_player_move
         Refresh the number of move played by the player.
      Parameters:
         self -- The Game object.
      """
      self.t.clear()
      self.t.penup()
      self.t.goto(-220, -300)
      self.t.write(f"Player Move: {self.current_chance_number}", align="center", font=('Arial', 30, 'normal'))


   def save_leaderboard(self):
      """
      Function -- save_leaderboard
         Read the leaderboard file and update the new winner informaiton into the file.
      Parameters:
         self -- The Game object.
      """
      helper_function.change_directory("")
      leaderboard_list = []
      # Read the current leaderboard from the file and store it in a list.
      try:
         with open("leaderboard.txt", 'r') as leaderboard_file:
            leaderboard_file.readline()
            leaderboard_file.readline()
            leader_info_check = leaderboard_file.readlines()
            for line in leader_info_check:
               info = line.strip().split(" : ")
               leaderboard_list.append((int(info[0]), info[1]))
         
         # Append the player's score and name to the leaderboard list.
         leaderboard_list.append((self.current_chance_number, self.player_name))
         # Sort the leaderboard list based on the score.
         leaderboard_list.sort(key=lambda x: x[0])
         
         # Write the sorted leaderboard list back to the leaderboard file.
         with open("leaderboard.txt", 'w') as leaderboard_file:
            leaderboard_file.write(f"Leaders:\n\n")
            for sort_info in leaderboard_list:
               leaderboard_file.write(f"{sort_info[0]} : {sort_info[1]}\n")
      
      except OSError:
         current_function = inspect.getframeinfo(inspect.currentframe()).function
         helper_function.log_error(f"Error in operating 'leaderboard.txt'.", current_function)
      except Exception as e: # e is the name of the error.
        current_function = inspect.getframeinfo(inspect.currentframe()).function
        helper_function.log_error(f"Error: {str(e)}.", current_function)


   def win(self):
      """
      Function -- win
         Check if all tiles are correctly positioned and update the leaderboard if the player wins.
      Parameters:
         self -- The Game object.
      """
      # Check if all tiles are correctly positioned.
      all_correct = True
      for tile in self.tiles:
        if tile.current_image_name != tile.correct_image_name:
            all_correct = False
            break
      
      # If all tiles are correctly positioned, update the leaderboard.
      if all_correct:
         self.save_leaderboard()
         self.load_leaderboard()
         # Display the winner message.
         helper_function.change_directory("Resources")
         helper_function.add_image(0, 0, "winner.gif")
         # Close the game window after a delay.
         turtle.ontimer(turtle.bye, 2000)
   

   def swap_tile(self, x, y, other_tile_index):
      """
      Function -- swap_tile
         Swap the positions of the blank tile and another tile if they are adjacent.
      Parameters:
         self -- The Game object.
         x -- The x coordinate of the center of the tile that is adjacent to the blank tile.
         y -- The y coordinate of the center of the tile that is adjacent to the blank tile.
         other_tile_index -- The index of the tile to be swapped with the blank tile.
      """
      blank_tile = self.tiles[self.current_blank_tile_idx]
      other_tile = self.tiles[other_tile_index]
      
      # Check if the click is within the bounds of the other tile.
      if (
         (other_tile.center_x - (self.tile_size_length / 2)) <= x
         and x <= (other_tile.center_x + (self.tile_size_length / 2))
         and (other_tile.center_y - (self.tile_size_length / 2)) <= y
         and y <= (other_tile.center_y + (self.tile_size_length / 2))
      ): 
         # Clear the stamps of the blank tile and the other tile.
         turtle.clearstamp(blank_tile.stamp_id)
         turtle.clearstamp(other_tile.stamp_id)
         self.add_directories_and_change_paths(self.image_path)        
        
         # swamp image on game board
         stamp_id = helper_function.add_image(blank_tile.center_x, blank_tile.center_y, other_tile.current_image_name)
         blank_tile.stamp_id = stamp_id
         stamp_id = helper_function.add_image(other_tile.center_x, other_tile.center_y, blank_tile.current_image_name)
         other_tile.stamp_id = stamp_id
         
         # swap current_image_name
         tmp_image_name = blank_tile.current_image_name
         blank_tile.current_image_name = other_tile.current_image_name
         other_tile.current_image_name = tmp_image_name
        
         # Update the index of the blank tile and the number of moves made by the player
         self.current_blank_tile_idx = other_tile_index
         self.current_chance_number += 1
         self.update_player_move()
         self.win()
   

   def move(self, x, y):
      """
      Function -- move
         Move a tile adjacent to the blank tile if possible.
      Parameters:
         self -- The Game object.
         x -- The x-coordinate of the click.
         y -- The y-coordinate of the click.
      """
      right_index = self.current_blank_tile_idx + 1
      down_index = self.current_blank_tile_idx + self.number_per_row
      left_index = self.current_blank_tile_idx - 1
      up_index = self.current_blank_tile_idx - self.number_per_row
      
      # Check the position of the blank tile and swap adjacent tiles accordingly.
      if self.current_blank_tile_idx == 0: # Upper left corner.
         self.swap_tile(x, y, right_index)
         self.swap_tile(x, y, down_index)
      elif (
         1 <= (self.current_blank_tile_idx % self.number_per_row)
         and (self.current_blank_tile_idx % self.number_per_row) < (self.number_per_row - 1)
         and self.current_blank_tile_idx // self.number_per_row == 0
      ): # Middle position of the first upper row.
         self.swap_tile(x, y, right_index)
         self.swap_tile(x, y, down_index)
         self.swap_tile(x, y, left_index)
      elif (
         self.current_blank_tile_idx % self.number_per_row == (self.number_per_row - 1)
         and self.current_blank_tile_idx // self.number_per_row == 0
      ): # Upper right corner.
         self.swap_tile(x, y, down_index)
         self.swap_tile(x, y, left_index)
      elif (
         1 <= (self.current_blank_tile_idx // self.number_per_row)
         and (self.current_blank_tile_idx // self.number_per_row) < (self.number_per_row - 1)
         and self.current_blank_tile_idx % self.number_per_row == 0
      ): # Middle position of the first column.
         self.swap_tile(x, y, right_index)
         self.swap_tile(x, y, down_index)
         self.swap_tile(x, y, up_index)
      elif (
         (1 <= (self.current_blank_tile_idx // self.number_per_row))
         and ((self.current_blank_tile_idx // self.number_per_row )< (self.number_per_row - 1))
         and (1 <= (self.current_blank_tile_idx % self.number_per_row))
         and ((self.current_blank_tile_idx % self.number_per_row) < (self.number_per_row - 1))
      ): # Inner positions.
         self.swap_tile(x, y, right_index)
         self.swap_tile(x, y, down_index)
         self.swap_tile(x, y, up_index)
         self.swap_tile(x, y, left_index)
      elif (
         (1 <= (self.current_blank_tile_idx // self.number_per_row))
         and ((self.current_blank_tile_idx // self.number_per_row) < (self.number_per_row - 1))
         and ((self.current_blank_tile_idx % self.number_per_row) == (self.number_per_row - 1))
      ): # Middle position of the last column.
         self.swap_tile(x, y, down_index)
         self.swap_tile(x, y, up_index)
         self.swap_tile(x, y, left_index)
      elif (
         (self.current_blank_tile_idx % self.number_per_row) == 0
         and (self.current_blank_tile_idx // self.number_per_row) == (self.number_per_row - 1)
      ): # Lower left corner.
         self.swap_tile(x, y, up_index)
         self.swap_tile(x, y, right_index)
      elif (
         (1 <= (self.current_blank_tile_idx % self.number_per_row))
         and ((self.current_blank_tile_idx % self.number_per_row) < (self.number_per_row - 1))
         and ((self.current_blank_tile_idx // self.number_per_row) == (self.number_per_row - 1))
      ): # Middle position of the last upper row.
         self.swap_tile(x, y, up_index)
         self.swap_tile(x, y, right_index)
         self.swap_tile(x, y, left_index)
      elif (self.current_blank_tile_idx == (self.number_per_row * self.number_per_row) - 1): # Lower right corner.
         self.swap_tile(x, y, up_index)
         self.swap_tile(x, y, left_index)
      

   def end_game_when_lost(self):
      """
      Function -- end_game_when_lost
         End the game when the player loses by displaying credits and exiting after a delay.
      Parameters:
         self -- The Game object.
      """
      self.clear_stamp(self.lose_image_stamp_id)
      helper_function.add_image(0, 0, "credits.gif")
      turtle.ontimer(turtle.bye, 1500)


   def handle_click(self, x, y):
      """
      Function -- handle_click
         Handle the click event by performing actions based on the clicked position.
      Parameters:
         self -- The Game object.
         x -- The x-coordinate of the click.
         y -- The y-coordinate of the click.
      """
      if (132 <= x and x <= 212 and -318 <= y and y <= -238):
         self.reset()
      elif (312 <= x and x <= 392 and -305 <= y and y <= -251):
         self.quit()
      elif (182 <= x and x <= 342 and -354<= y and y <= -202):
         self.load_another_game()
      else:
         if self.current_chance_number < self.num_of_chances: 
            self.move(x, y)
         else:
            helper_function.change_directory("Resources")
            self.lose_image_stamp_id = helper_function.add_image(0, 0, "Lose.gif")
            turtle.ontimer(self.end_game_when_lost, 2000)