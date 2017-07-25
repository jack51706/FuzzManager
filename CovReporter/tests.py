'''
Tests

@author:     Christian Holler (:decoder)

@license:

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

@contact:    choller@mozilla.com
'''

import json
import os
import unittest

from CovReporter import CovReporter

coverallsData = """
{ "git": { "branch":"master", "head": { "id":"1a0d9545b9805f50a70de703a3c04fc0d22e3839"} },
  "repo_token":"unused",
  "service_job_number":"",
  "service_name":"",
  "service_number":"",
  "source_files":[
    {"name":"topdir1/subdir1/file1.c","source_digest":"d41d8cd98f00b204e9800998ecf8427e", "coverage":[null,null,12,12,10,2,0,0,null]},
    {"name":"topdir1/subdir1/file2.c","source_digest":"d41d8cd98f00b204e9800998ecf8427e", "coverage":[null,20,20,15,15,15,15,0,null,null]},
    {"name":"topdir1/subdir2/file3.c","source_digest":"d41d8cd98f00b204e9800998ecf8427e", "coverage":[null,null,12,12,10,2,0,0,null]},
    {"name":"topdir2/subdir1/file1.c","source_digest":"d41d8cd98f00b204e9800998ecf8427e", "coverage":[null,null,0,0,0,0,0,0,null]}
  ]
}"""

coverallsData = json.loads(coverallsData)

class TestCovReporterCoverallsVersionData(unittest.TestCase):
    def runTest(self):
        ret = CovReporter.version_info_from_coverage_data(coverallsData)
        self.assertEqual(ret["revision"], "1a0d9545b9805f50a70de703a3c04fc0d22e3839")
        self.assertEqual(ret["branch"], "master")

class TestCovReporterPreprocessData(unittest.TestCase):
    def runTest(self):
        result = CovReporter.preprocess_coverage_data(coverallsData)

        children = "children"
        coverage = "coverage"
        name = "name"
        linesTotal = "linesTotal"
        linesMissed = "linesMissed"
        linesCovered = "linesCovered"
        coveragePercent = "coveragePercent"

        # Check that we have all the topdirs
        self.assertTrue("topdir1" in result[children], "topdir1 missing in result")
        self.assertTrue("topdir2" in result[children], "topdir1 missing in result")

        # Check that we have all the subdirs
        self.assertTrue("subdir1" in result[children]["topdir1"][children], "subdir1 missing in result")
        self.assertTrue("subdir2" in result[children]["topdir1"][children], "subdir1 missing in result")
        self.assertTrue("subdir1" in result[children]["topdir2"][children], "subdir1 missing in result")

        # Check that we haven't got more subdirs than expected for topdir2
        self.assertEqual(len(result[children]["topdir2"][children]), 1)

        # Check length of coverage list, name and summary values for file1.c
        self.assertEqual(len(result[children]["topdir1"][children]["subdir1"][children]["file1.c"][coverage]), 9)
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][children]["file1.c"][name], "file1.c")
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][children]["file1.c"][linesTotal], 6)
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][children]["file1.c"][linesMissed], 2)
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][children]["file1.c"][linesCovered], 4)
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][children]["file1.c"][coveragePercent], 66.67)


        # Check name and summary values for topdir1/subdir1/
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][name], "subdir1")
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][linesTotal], 13)
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][linesCovered], 10)
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][linesMissed], 3)
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][coveragePercent], 76.92)

        # Check summary values for topdir1/subdir2/
        self.assertEqual(result[children]["topdir1"][children]["subdir2"][linesTotal], 6)
        self.assertEqual(result[children]["topdir1"][children]["subdir2"][linesCovered], 4)
        self.assertEqual(result[children]["topdir1"][children]["subdir2"][linesMissed], 2)

        # Check summary values for topdir1/
        self.assertEqual(result[children]["topdir1"][linesTotal], 19)
        self.assertEqual(result[children]["topdir1"][linesCovered], 14)
        self.assertEqual(result[children]["topdir1"][linesMissed], 5)

        # Check summary values for topdir2/
        self.assertEqual(result[children]["topdir2"][linesTotal], 6)
        self.assertEqual(result[children]["topdir2"][linesCovered], 0)
        self.assertEqual(result[children]["topdir2"][linesMissed], 6)
        self.assertEqual(result[children]["topdir2"][coveragePercent], 0.0)

        # Check that our converter replaces null with -1 to save some space
        self.assertEqual(result[children]["topdir1"][children]["subdir1"][children]["file1.c"][coverage][0], -1)

if __name__ == "__main__":
    unittest.main()
