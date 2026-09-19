scrub:
	scrub.py "$$(cat data/Imatinib.smiles)" -o data/Imatinib_scrubbed.sdf --ph 6 --skip_tautomer

ligand:
	mk_prepare_ligand.py -i data/Imatinib_scrubbed.sdf -o data/Imatinib.pdbqt

atoms:
	python atoms.py data/1IEP.pdb data/1IEP_receptor_atoms.pdb
