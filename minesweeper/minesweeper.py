import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if len(self.cells) == self.count:
            return set(self.cells)
        return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #First I check if the cell is within the list
        if cell in self.cells:

            #IF exist, remove it and decrease the count 
            self.cells.remove(cell)
            self.count -= 1
            return None

            



    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #First I check if the cell is within the list
        if cell in self.cells:

            #IF exist, remove it
            self.cells.remove(cell)
            
            return None



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def get_neightbours(self, cell):
        """

        """

        #Neightbours cell
        nb = set()
        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if ((0 <= i < self.height) and (0 <= j < self.width) and ((i, j) != cell) and ((i, j) not in self.moves_made)):
                    
                    if (i,j) in self.mines:
                        count += 1
                    elif (i,j) in self.safes:
                        continue
                    else:
                        nb.add((i,j))

        return nb, count





    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.safes.add(cell)

        # 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        

        nb = self.get_neightbours(cell)[0]
        mines_fromnb= self.get_neightbours(cell)[1]

        count -= mines_fromnb

        if count == 0:
            #all of these are safe
            for neighbor in nb:
                self.safes.add(neighbor)

        elif count == len(nb):
            #all of these are mines
            for neighbor in nb:
                self.mines.add(neighbor)
                
        else:
            new_sentence = Sentence(nb,count)

            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)


        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base

        for s in self.knowledge:
            new_safes = s.known_safes() #get safes from the sentences and add them
            
            for safe in new_safes:
                self.mark_safe(safe)
            
            
            new_mines = s.known_mines() #get mines from the sentences and add them

            for mine in new_mines:
                self.mark_mine(mine)
                
            

        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge

        temp_knowledge = copy.deepcopy(self.knowledge)
        for sentence1 in temp_knowledge:
            for sentence2 in temp_knowledge:
                
                if sentence1 == sentence2:
                    continue
                elif (len(sentence1.cells) > 0) and (sentence1.cells.issubset(sentence2.cells)):
                    #print("Found a subset! Sentece ", sentence1, " is a subset of ", sentence2)
                    sentence3 = Sentence(sentence2.cells-sentence1.cells,sentence2.count-sentence1.count)

                    #check if sentence3 is new

                    isnew = True

                    for check_sentence in temp_knowledge:
                        if (sentence3.cells == check_sentence.cells) and (sentence3.count == check_sentence.count):
                            isnew = False
                            break

                    
                    if len(sentence3.cells) > 0 and isnew:
                        #print("A new sentece was created: ", sentence3)
                        self.knowledge.append(sentence3)




        # print(cell)
        # print(count)


        
        print("Known mines: ", len(self.mines), " | Detail: ", self.mines)

        print("______")
            
        #print(cell,count)
        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        if self.safes.issubset(self.moves_made):
            return None
        
        

        else:

            while True:
                random_i = random.randint(0,7)
                random_j = random.randint(0,7)

                if (((random_i,random_j) not in self.moves_made) and ((random_i,random_j) not in self.mines) and ((random_i,random_j) in self.safes)):
                    print("Move made: ",(random_i,random_j))
                    return (random_i,random_j)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        if len(self.moves_made) + len(self.mines) == self.height * self.width:
            #the game is finish
            return None

        while True:
            random_i = random.randint(0,7)
            random_j = random.randint(0,7)

            if (((random_i,random_j) not in self.moves_made) and ((random_i,random_j) not in self.mines)):
                print("Move made: ",(random_i,random_j))
                
                return (random_i,random_j)
            
