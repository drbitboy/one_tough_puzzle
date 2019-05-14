"""[Topinnie][Leftoutie][Bottomoutie][Rightinnie]:
=>ccdd cdhc ddhh
=>hssc hdsd sshc
=>dhcc sdsh shch
shdc = [spade][heart][diamond][club]"""

import sys

def not_match_one_piece(cur_soln, piece):
  new_pos,new_row,new_col = len(cur_soln),len(cur_soln)/3,len(cur_soln)%3
  if new_col and cur_soln[new_pos-1][3] != piece[1]: return True
  if new_row and cur_soln[new_pos-3][2] != piece[0]: return True

def solved(solution,pieces):
  if '--debug' in sys.argv[1:]: print(len(solution),solution,pieces)
  if not pieces: return solution
  discards = []
  while pieces:
    discards.append(pieces.pop())
    if None is not_match_one_piece(solution,discards[-1]):
      full_solution = solved(solution+discards[-1:],pieces+discards[:-1])
      if full_solution: return full_solution

if "__main__" == __name__:
  end_solution = solved([],sum([s[2:].strip().split() for s in __doc__.split('\n') if '=>' == s[:2]],[]))
  if end_solution: print("""{0}  {1}  {2}\n{3}  {4}  {5}\n{6}  {7}  {8}""".format(*end_solution))
