import sys

from prody import parsePDB, writePDB

atoms_from_pdb = parsePDB(sys.argv[1])
receptor_selection = "chain A and not water and not hetero"
receptor_atoms = atoms_from_pdb.select(receptor_selection)
writePDB(sys.argv[2], receptor_atoms)
