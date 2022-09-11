from re import I
import pygame
import random
import math
pygame.init()

# Use a class to store information, instead of creating global variables
# Then use an instance of this class with functions that require these values.
class valuesAndInformation:
  TOP_PADDING = 150
  SIDE_PADDING = 150
  # Font for sort control display
  FONT = pygame.font.SysFont('cambria', 25)
  LARGER_FONT = pygame.font.SysFont('cambria', 35)
  # RGB Values
  WHITE = 248, 248, 255
  RED = 238, 0, 0
  GREEN = 84, 255, 159
  BLUE = 0, 104, 139
  YELLOW = 255, 193, 37
  BACKGROUND = BLUE
  # Gradient colors for yellowish gold
  GRADIENTCOLORS = [(255,193,37), (238,180,34), (205,155,29)]

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
    self.blockHeight = math.floor((self.height - self.TOP_PADDING) / (self.maximumValue - self.minimumValue))

    # We want to start at bottom left, in pygame coordinates start at top left aka (0,0)
    # As you move down, Y increase. As you move right, X increases.
    self.startingX = self.SIDE_PADDING // 2
    return 

# GENERATE THE STARTING LIST:
def generate_starting_list(n, minimum, maximum):
  displayList = []

  for _ in range(n):
    value = random.randint(minimum, maximum)
    displayList.append(value)

  return displayList


""" DRAW LIST TO DISPLAY TO WINDOW """
def drawDisplay(drawInfo, algoName, ascend):
  # Everytime we draw, we want to overwrite what was previously on display with a background color.
  # This way there won't be any overlap visible to the user
  drawInfo.window.fill(drawInfo.BACKGROUND)
  
  # Draw title:
  title = drawInfo.LARGER_FONT.render(f"{algoName} - {'Ascending' if ascend else 'Descending'}", 1, drawInfo.YELLOW)
  drawInfo.window.blit(title, (drawInfo.width/2 - title.get_width()/2, 5))

  # Draw controls:
  controls = drawInfo.FONT.render("R - Reset || S - Sort || A - Ascending || D - Descending", 1, drawInfo.WHITE)
  drawInfo.window.blit(controls, (drawInfo.width/2 - controls.get_width()/2, 45))

  # Draw Possible Sorting Choices:
  sortChoice = drawInfo.FONT.render("B - Bubble Sort || I - Insertion Sort || L - Selection Sort || H - Heap Sort", 1, drawInfo.WHITE)
  drawInfo.window.blit(sortChoice, (drawInfo.width/2 - sortChoice.get_width()/2, 75))

  drawList(drawInfo)
  pygame.display.update()
  return 

def drawList(drawInfo, colorPos={}, clearBackground=False):
  # Draw the rectangles for each of the elements in the list
  lst = drawInfo.aList

  # Get the area that the replaced block will need without redrawing entire window
  if clearBackground:
    clearRectangle = (drawInfo.SIDE_PADDING//2, drawInfo.TOP_PADDING,
                      drawInfo.width - drawInfo.SIDE_PADDING,
                      drawInfo.height - drawInfo.TOP_PADDING)

    pygame.draw.rect(drawInfo.window, drawInfo.BACKGROUND, clearRectangle)

  # Get index and value of each element. Then calculate x and y coordinate
  for i, val in enumerate(lst):
    x = drawInfo.startingX + i * drawInfo.blockWidth
    y = drawInfo.height - (val - drawInfo.minimumValue) * drawInfo.blockHeight 
    # Every 3 elements switch to another shade
    colorUsed = drawInfo.GRADIENTCOLORS[i % 3]

    # Override the color for the block that is being sorted (to highlight it)
    if i in colorPos:
      colorUsed = colorPos[i]

    pygame.draw.rect(drawInfo.window, colorUsed, (x, y, drawInfo.blockWidth, drawInfo.height))

  # Update the screen for the area of the cleared rectangle
  if clearBackground:
    pygame.display.update()

  return


""" SORTING FUNCTIONS """
# Bubble Sort: Time Complexity: O(n^2), Space Complexity: O(1)
def bubbleSort(drawInfo, ascend=True):
  inputList = drawInfo.aList
  
  for i in range(len(inputList) - 1):
    for j in range(len(inputList) - i - 1):
      n1 = inputList[j]
      n2 = inputList[j + 1]

      if (n1 > n2 and ascend) or (n1 < n2 and not ascend):
        inputList[j], inputList[j + 1] = inputList[j + 1], inputList[j]
        drawList(drawInfo, {j: drawInfo.GREEN, j+1: drawInfo.RED}, True)
        # this generator allows us to still have controls while iteration occurs
        yield True

  return inputList

# Insertion Sort: Time Complexity: O(n^2), Space Complexity: O(1)
def insertionSort(drawInfo, ascend=True):
  inputList = drawInfo.aList

  for i in range(1, len(inputList)):

    current = inputList[i]

    while True:
      sortAscending = i > 0 and inputList[i - 1] > current and ascend
      sortDescending = i > 0 and inputList[i - 1] < current and not ascend

      # If at some point, there is nothing to swap, exit while loop, move to next iteration in for loop
      if not sortAscending and not sortDescending:
        break

      inputList[i] = inputList[i - 1]
      i = i - 1
      inputList[i] = current
      drawList(drawInfo, {i: drawInfo.GREEN, i - 1: drawInfo.RED}, True)
      yield True

  return inputList

# Selection Sort: Time Complexity: O(n^2), Space Complexity: O(1)
def selectionSort(drawInfo, ascend=True):
  inputList = drawInfo.aList

  for i in range(len(inputList)):
    minimumIndex = i

    for j in range(minimumIndex + 1, len(inputList)):

      if ascend:
        if inputList[j] < inputList[minimumIndex]:
          minimumIndex = j
      else:
        if inputList[j] > inputList[minimumIndex]:
          minimumIndex = j
      
    inputList[i], inputList[minimumIndex] = inputList[minimumIndex], inputList[i]
    drawList(drawInfo, {i: drawInfo.GREEN, minimumIndex: drawInfo.RED}, True)
    yield True

  return inputList

# Heap Sort: Time Complexity: O(n log n), Space Complexity: O(1)
def heapify(inputList, length, index, ascend=True):

  maxOrminIdx = index
  # Index of child nodes
  l = index * 2 + 1
  r = index * 2 + 2

  if ascend:
    if l < length and inputList[index] < inputList[l]:
      maxOrminIdx = l
    if r < length and inputList[maxOrminIdx] < inputList[r]:
      maxOrminIdx = r

  elif not ascend:
    if l < length and inputList[l] < inputList[maxOrminIdx]:
      maxOrminIdx = l
    if r < length and inputList[r] < inputList[maxOrminIdx]:
      maxOrminIdx = r 

  if maxOrminIdx != index:
    inputList[index], inputList[maxOrminIdx] = inputList[maxOrminIdx], inputList[index]
    heapify(inputList, length, maxOrminIdx, ascend)



def heapSort(drawInfo, ascend=True):
  inputList = drawInfo.aList
  n = len(inputList)

  for i in range(n//2, -1, -1):
    heapify(inputList, n, i, ascend)


  for i in range(n - 1, 0, -1):
    inputList[i], inputList[0] = inputList[0], inputList[i]
    drawList(drawInfo, {i: drawInfo.GREEN, 0: drawInfo.RED}, True)
    yield True
    heapify(inputList, i, 0, ascend)



""" MAIN DRIVER FUNCTION """
def main():
  run = True
  clock = pygame.time.Clock()

  nowSort = False
  ascend = True

  # Default is bubbleSort
  sortAlgo = bubbleSort
  sortAlgoName = "Bubble Sort"
  sortAlgoGenerator = None

  n, minimumVal, maximumVal = 43, 0, 100

  displayList = generate_starting_list(n, minimumVal, maximumVal)
  drawInfo = valuesAndInformation(900, 700, displayList)

  while run:
    # Max number of time loop can run per second
    clock.tick(30)

    # Use the generator to get to next yield, end when no more items to iterate
    if nowSort:
      try:
        next(sortAlgoGenerator)
      except StopIteration:
        nowSort = False
    else:
      # Render display to window
      drawDisplay(drawInfo, sortAlgoName, ascend)


    for event in pygame.event.get():
      # When user quits application
      if event.type == pygame.QUIT:
        run = False

      # Set up event of user reloading list
      # If no key press, continue to next event, else reload.
      if event.type != pygame.KEYDOWN:
        continue
      if event.key == pygame.K_r:
        displayList = generate_starting_list(n, minimumVal, maximumVal)
        drawInfo.set_list(displayList)
        # Reset sorting when list is reset
        nowSort = False

      # Initialize sorting on key press and if not already sorting
      elif event.key == pygame.K_s and nowSort == False:
        nowSort = True
        sortAlgoGenerator = sortAlgo(drawInfo, ascend)

      # Let user decide to sort by ascending or descending order
      elif event.key == pygame.K_a and not nowSort:
        ascend = True
      elif event.key == pygame.K_d and not nowSort:
        ascend = False
      elif event.key == pygame.K_b and not nowSort:
        sortAlgo = bubbleSort
        sortAlgoName = "Bubble Sort"
      elif event.key == pygame.K_i and not nowSort:
        sortAlgo = insertionSort
        sortAlgoName = "Insertion Sort"
      elif event.key == pygame.K_l and not nowSort:
        sortAlgo = selectionSort
        sortAlgoName = "Selection Sort"
      elif event.key == pygame.K_h and not nowSort:
        sortAlgo = heapSort
        sortAlgoName = "Heap Sort"



  pygame.quit()
  return

if __name__ == "__main__":
  main()

