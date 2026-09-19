scrub:
	scrub.py "$$(cat data/LIGAND.smiles)" -o data/LIGAND_scrubbed.sdf --ph 6 --skip_tautomer

ligand:
	mk_prepare_ligand.py -i data/LIGAND_scrubbed.sdf -o data/LIGAND.pdbqt

atoms:
	python atoms.py data/TARGET.pdb data/TARGET_receptor_atoms.pdb

cryst:
	grep CRYST1 data/TARGET.pdb > data/TARGET_receptor.pdb
	cat data/TARGET_receptor_atoms.pdb >> data/TARGET_receptor.pdb

reduce:
	MMTBX_CCP4_MONOMER_LIB="geostd" mmtbx.reduce2 data/TARGET_receptor.pdb approach=add add_flip_movers=True
	mv TARGET* data

receptor:
	mk_prepare_receptor.py -i data/TARGET_receptorFH.pdb -o data/TARGET_receptor -p -v --default_altloc A --box_center $$(python center.py data/TARGET.pdb) --box_size 30 30 30

docking:
	./vina --receptor data/TARGET_receptor.pdbqt --ligand data/LIGAND.pdbqt --config data/TARGET_receptor.box.txt --exhaustiveness 32 --out data/TARGET_LIGAND_vina_out.pdbqt

score:
	grep RESULT data/TARGET_LIGAND_vina_out.pdbqt | head -n 1 | awk '{print $$4}'
