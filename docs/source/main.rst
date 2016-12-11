rna-pdb-tools
========================================

.. automodule:: rna_pdb_tools.pdb_parser_lib
   :members:

Selection
-----------------------------------------

.. automodule:: rna_pdb_tools.utils.extra_functions.select_fragment
		:members:

Edit
-----------------------------------------

.. autofunction:: rna_pdb_tools.pdb_parser_lib.edit_pdb

Examples::

  rna-pdb-tools.py --edit 'A:3-21>A:1-19' 1f27_clean.pdb > 1f27_clean_A1-19.pdb

or even::

  $ md_1f27_clx rna-pdb-tools.py --edit 'A:3-21>A:1-19,B:22-32>B:20-30' 1f27_clean.pdb > 1f27_clean_renumb.pdb