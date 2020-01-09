#!/usr/bin/env python

import pywbem
from lib import wbem_connection
import unittest
import optparse
import os
import time
from socket import getfqdn
from subprocess import Popen
import signal
import sys

import threading



conn = None

#This test requires the usage of elementtree

_g_opts = None
_g_args = None


################################################################################
class UpcallAtomTest(unittest.TestCase):

    global conn


    def setUp(self):
        unittest.TestCase.setUp(self)
        self.conn = conn
        self.conn.debug = True
        self._verbose = _g_opts.verbose
        self._dbgPrint()


    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def _dbgPrint(self, msg=''):
        if self._verbose:
            if len(msg):
                print('\t -- %s --' % msg)
            else:
                print('')

    def test_a_upcalls_all(self):
        rv,outs = self.conn.InvokeMethod('getBrokerName', 'Test_UpcallAtom')
        if rv == 'Pegasus':
            print '\n*** Broker detected as Pegasus.  Skipping upcall test.'
            print 'Re-enable when Pegasus is fixed.' 
            return
        rv,outs = self.conn.InvokeMethod('test_all_upcalls', 'Test_UpcallAtom')
        self.assertEquals(rv, 'Success!')
        self.assertFalse(outs)


def get_unit_test():
    return UpcallAtomTest


if __name__ == '__main__':
    parser = optparse.OptionParser()
    wbem_connection.getWBEMConnParserOptions(parser)
    parser.add_option('--verbose', '', action='store_true', default=False,
            help='Show verbose output')
    parser.add_option('--op', '', action='store_true', default=False,
            help='Use OpenPegasus UDS Connection')
    parser.add_option('--level',
            '-l',
            action='store',
            type='int',
            dest='dbglevel',
            help='Indicate the level of debugging statements to display (default=2)',
            default=2)
    _g_opts, _g_args = parser.parse_args()
    
    if _g_opts.op:
        conn = pywbem.PegasusUDSConnection()
    else:
        conn = wbem_connection.WBEMConnFromOptions(parser)
    
    suite = unittest.makeSuite(UpcallAtomTest)
    unittest.TextTestRunner(verbosity=_g_opts.dbglevel).run(suite)

