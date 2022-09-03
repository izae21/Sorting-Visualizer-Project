import pygame
import random
pygame.init()

# Use a class to store information, instead of creating global variables
# Then use an instance of this class with functions that require these values.
class valuesAndInformation:
  TOP_PADDING = 150
  SIDE_PADDING = 150
  #RGB Values
  BLACK = 0, 0, 0
  GREY = 128, 128, 128
  RED = 255, 0, 0
  GREEN = 0, 255, 0
  WHITE = 255, 255, 255
  BACKGROUND = WHITE

  def __init__(self, width, height, aList):
    self.height = height
    self.width = width
    # Set up a window, pass width and height as a tuple
    self.window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sorting Algorithm Visualizer")
    self.set_list(aList)

  # Set the attributes we need that are related to the input list
  def set_list(self, aList):
    # The width and height of the bars need to change depending on the range of values used
    self.aList = aList
    self.minimumValue = min(aList)
    self.maximumValue = max(aList)
    # Set width of the blocks we use to represent the list.
    # Set height of the blocks depending on the list's values
    # For example, if there are 100 values, the heights will be smaller than if there were only 10 values.
    # Object of these calculations is to find the total "drawable" area.
    self.blockWidth = round((self.width - self.SIDE_PADDING)) / len(aList)
    self.blockHeight = round((self.height - self.TOP_PADDING) / (self.maximumValue - self.minimumValue))

    # We want to start at bottom left, in pygame coordinates start at top left aka (0,0)
    # As you move down, Y increase. As you move right, X increases.
    self.startingX = self.SIDE_PADDING // 2

# GENERATE THE STARTING LIST:
def generate_starting_list(n, minimum, maximum):
  displayList = []

  for _ in range(n):
    value = random.randint(minimum, maximum)
    displayList.append(value)

  return displayList

# MAIN DRIVER FUNCTION:
def main():
  run = True
  clock = pygame.time.Clock()

  n, minimumVal, maximumVal = 43, 0, 100

  displayList = generate_starting_list(n, minimumVal, maximumVal)
  drawValuesAndInfo = valuesAndInformation(900, 700, displayList)

  while run:
    # Max number of time loop can run per second
    clock.tick(60)
    # Render display to window
    pygame.display.update()

    for event in pygame.event.get():
      # When user quits application
      if event.type == pygame.QUIT:
        run = False

  pygame.quit()

if __name__ == "__main__":
  main()

