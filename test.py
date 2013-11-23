#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase, main
from py3dna import Py3DNA, Py3DNAMissingFile


class Tests(TestCase):

    def setUp(self):
        pass

    def test_Basic_1xjr(self):
        """
            """

        p = Py3DNA('test_data/1xjr.pdb')
        seq = p.get_seq()
        self.assertEqual(seq,
                         'gGAGUUCACCGAGGCCACGCGGAGUACGAUCGAGGGUACAGUGAAUU'
                         )

    def test_FilesDoesNotExists(self):
        self.assertRaises(Py3DNAMissingFile, lambda : \
                          Py3DNA('test/dupa666'))


if __name__ == '__main__':
    main()
