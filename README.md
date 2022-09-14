# The residence time ([PDBrt](https://pdbrt.polsl.pl/)) database

The [PDBrt](https://pdbrt.polsl.pl/) database is a free, non-commercial repository for 3D protein-ligand complex data, including 
the measured ligand residence time inside the binding pocket of the specific biological macromolecules as deposited in The Protein Data Bank. The PDBrt database contains information about both the protein and the ligand separately, as well as the protein-ligand complex, binding kinetics, and time of the ligand residence inside the protein binding site.

## Availability
The [PDBrt](https://pdbrt.polsl.pl/) is available to the community through its web-based interface only. 

## How to work with the PDBrt locally?

### Requirements
- [make](https://www.gnu.org/software/make/)
- [docker-compose](https://docs.docker.com/compose/)

### Download 
Use git to clone this repository and its submodules

```git clone https://github.com/mlugowska/residence_time.git```

### Run

```cd residence_time```

```make build-dev```


## What about the data?
All users have access to the online database content - login is not required!

### Data description
Datatable consists of the following columns:

1. PDB ID	
2. Residence Time	
3. Residence Time Plus Minus	
4. Ligand Name	
5. Ligand Inchi	
6. Ligand SMILES	
7. Ligand Formula	
8. Ligand Code	
9. Protein Name	
10. Protein Organism	
11. Complex Name	
12. Release year	
13. Ki	
14. Ki Plus Minus	
15. Kon	
16. Kon Plus Minus	
17. Kon 10^	
18. Koff	
19, Koff Plus Minus	
20. Primary Reference	
21. PubMed ID	
22. is calculated from koff		

### Data upload
To upload your data you need to create the admin user

```docker-compose exec web bash```

```./manage.py createsuperuser```

Then, go to your homepage and login. New data can be added either by uploading an xlsx (MS Excel) file or manually. 

If you choose to upload an xlsx file, please be sure that column names agree with those described above. 

Contact us, if you feel like some data on the PDBrt webpage is missing or you have just found a protein-ligand complex with known residence time which is not included.

e-mail: magdalena.lugowska@polsl.pl

## More information

You can read about the PDBrt on [F1000Research platform](https://f1000research.com/articles/10-1236/v1) or talk to authors using the e-mail address above.
