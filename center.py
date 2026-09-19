import sys

from prody import parsePDB, calcCenter

atoms_from_pdb = parsePDB(sys.argv[1])
ligand_selection = "chain A and resname STI"
ligand_atoms = atoms_from_pdb.select(ligand_selection)
center_x, center_y, center_z = calcCenter(ligand_atoms)
print(center_x, center_y, center_z)
