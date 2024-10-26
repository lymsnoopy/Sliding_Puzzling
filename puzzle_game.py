"""
   CS5001
   Spring 2024
   Project
   Yiming Luo

   This is a program that implements puzzle games.
"""

import turtle
import inspect
from Game import Game
import helper_function

def main():
   turtle.tracer(0)
   turtle.screensize(810, 740)
   turtle.hideturtle()
   game = Game()
   game.search_puz_file()
   game.splash_screen()
   turtle.update()
   turtle.mainloop()
if __name__ == "__main__":
   try:
      main()
   except Exception as e: # e is the name of the error.
      current_function = inspect.getframeinfo(inspect.currentframe()).function
      helper_function.log_error(f"Unknown error: {str(e)}.", current_function)