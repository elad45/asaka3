# importing system module for reading files
import sys
from congruence_closure import congruenceClosure
# import utility functions
from utils import get_terms, get_function_symbols

# import classses for parsing smt2 files
from pysmt.smtlib.parser import SmtLibParser
from six.moves import cStringIO

# import pysmt functions for creating formulas and terms
from pysmt.shortcuts import Not, Equals, Function

# solver for uninterpreted functions
# we represent a cube as a list of literals
# returns two elements `b,c`:
# if `cube` is satisfiable, `b` is `True` and `c` is `None`.
# otherwise, `b` is `False` and `c` is a sub-list of
# `cube` such that `c` is already unsatisfiable.
# `c` consists of the literals that were used
# in the derivation.
# In some cases, `c` will be simply the same as `cube`.
# But in various cases, the derivation did not
# rely on all literals of `cube`, and in such cases,
# only those literals that were relied on would be a 
# part of `c`.
def uf_solver(cube):
  cc = congruenceClosure(cube)
  cc.solve()
  # for literal in cube:
  #   if literal.is_not():
  #       flag = False
  #       cc.add_vars(literal, flag)
  #   elif literal.is_equals():
  #       flag = True
  #       cc.add_vars(literal, flag)
  #   else:
  #       raise ValueError("invalid literal")
  # print(cc.get_groups())
  #
  # isChange = cc.top_level()

  return True, None

# main function
def main():
  # read path from input
  path = sys.argv[1]
  with open(path, "r") as f:
    smtlib = f.read()

  # parse the smtlib file and get a formula
  parser = SmtLibParser()
  script = parser.get_script(cStringIO(smtlib))
  formula = script.get_last_formula()

  # we are assuming `formula` is a flat cube.
  # `cube` represents `formula` as a list of literals
  cube = formula.args()
  print(cube)
  # check if sat or unsat and print result
  sat, core = uf_solver(cube)
  if sat:
    print("sat")
  else:
    print("unsat")
    print("-----")
    print("\n".join([str(x) for x in core]))

if __name__ == "__main__":
    main()
