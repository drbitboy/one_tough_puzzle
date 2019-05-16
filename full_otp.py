"""[Topinnie][Leftoutie][Bottomoutie][Rightinnie] and
shdc = [spade][heart][diamond][club]:
=>ccdd cdhc ddhh
=>hssc hdsd sshc
=>dhcc sdsh shch"""

import sys

########################################################################
class PIECE(object):
  """
  Piece class; indicates each edge's suit and innie/outie, plus
  keeps track of rotation

  """
  def __init__(self, suits):
    """
    Suits is string with four suit letters (s or h or c or d), in order
    of nominal top innie, nominal left outie, nominal bottom outie,
    nominal right innie.

    N.B. there are eight unique [suit+innie+outie] pairs possible

    """
    ### Extend results by repeating first three suits, so eight
    ### characters starting at an offset (self.top) into the string will
    ### contain four [suit+innie/outie] pairs in sequences, starting at
    ### the one rotated to the top
    self.iooiioo = ''.join(['{0}{1}'.format(suit,io) for suit,io in zip(suits+suits,'iooiioo')])

    ### Invert innies to outies and vice versa, for string comparisons
    ### that will identify where potential neighbors will mate with
    ### this piece
    self.oiiooii = self.iooiioo.replace('i','I').replace('o','i').replace('I','o')

    ### Initialize rotation
    self.set_top(0)

  def set_top(self, top):
    """Set rotation as offset to top [suit+innie/outie]"""
    self.top = top

  def set_left(self, left):
    """
    Set rotation as offset to top [suit+innie/outie], but starting from
    offset to left [suite+innie/outie]
    """
    self.top = (left + 6) % 8

  ### Return [suit+innie/outie] at each position as two characters,
  ### based on the current rotation offset (self.top)

  def top(self): return self.iooiioo[self.top:][:2]
  def left(self): return self.iooiioo[(self.top+2)%8:][:2]
  def bottom(self): return self.iooiioo[(self.top+4)%8:][:2]
  def right(self): return self.iooiioo[(self.top+6)%8:][:2]

  def is_match(self, above, toleft):
    """Does [self] fit below [above] and to the right of [toleft]"""

    if above is None:

      ### If [above] is None, then need only test [toleft]

      ### - If [toleft] is also None, then this first piece must match
      if toleft is None: return True

      ### Find location of right [suit+innie/outie] in inverted string
      pos_find = self.oiiooii.find(toleft.right())

      ### If match occurs, pos_find will be offset to left connection
      func = self.set_left

    elif toleft is None:

      ### If [toleft] is None, then need only test [above] bottom
      pos_find = self.oiiooii.find(above.bottom())

      ### If match occurs, pos_find will be offset to left connection
      func = self.set_top

    else:

      ### Neither [above] nore [toleft] is None, check match against
      ### concatenation of above.bottom() and toleft.right()
      pos_find = self.oiiooii.find(above.bottom()+toleft.right())

      ### If match occurs, pos_find will be offset to left connection
      func = self.set_top

    ### Return False if no match occurs
    if pos_find < 0: return False

    ### Matched [above] and/or [toleft]:  set rotation and return True
    func(pos_find)
    return True

  def __repr__(self):
    """Return four [suit+innie/outie] pairs, starting with top"""
    return '{0}'.format(self.iooiioo[self.top:][:8])


########################################################################
def match_one_piece(cur_soln, piece):
  """Does piece fit into current solution (list of pieces)?"""

  ### Get linear position, and [row,column] of next piece in solution
  new_pos = len(cur_soln)
  new_row,new_col = new_pos/3,new_pos%3

  ### Determine current solution's pieces above and to left of new_pos
  above = new_row and cur_soln[new_pos-3] or None
  toleft = new_col and cur_soln[new_pos-1] or None

  ### Return True if piece can fit into new_pos, else return False
  return piece.is_match(above, toleft)


########################################################################
def solved(solution, pieces):
  """Recursive trial of added pieces to solution"""
  if '--debug' in sys.argv[1:]: print(len(solution),solution,pieces)

  ### If no more pieces, solution is complete
  if not pieces: return solution

  ### Initialize an empty discards list
  discards = []
  while pieces:

    ### Target piece is last piece in pieces list; move to discards
    ### list, assuming it will not fit into current solution
    ###  N.B. it will not stay on discards list if it fits
    discards.append(pieces.pop())

    ###  Loop over rotations
    for top in [0,2,4,6]:

      ### Rotate target piece per top
      if not solution: discards[0].set_top(top)

      ### Test if target piece fits into current solution
      if match_one_piece(solution,discards[-1]):

        ### If it fits, add it to the current solution and recurse
        full_solution = solved(solution+discards[-1:], pieces+discards[:-1])

        ### If that full_solution is non-False, then it is a complete
        ### solution:  return it up the chain of recursed calls
        if full_solution: return full_solution

      ### Cancel further rotations if current solution is not empty
      if solution: break


########################################################################
if "__main__" == __name__:

  pieces = sum([[PIECE(suits) for suits in s[2:].strip().split()] for s in __doc__.split('\n') if '=>' == s[:2]],[])
  end_solution = solved([],pieces)
  if end_solution: print("{0}  {1}  {2}\n{3}  {4}  {5}\n{6}  {7}  {8}".format(*end_solution))
"""
  end_solution = solved([],sum([s[2:].strip().split() for s in __doc__.split('\n') if '=>' == s[:2]],[]))
  if end_solution: print("{0}  {1}  {2}\n{3}  {4}  {5}\n{6}  {7}  {8}".format(*end_solution))
"""
