# -*- coding: utf-8 -*-

############################ Copyrights and license ############################
#                                                                              #
# Copyright 2012 Vincent Jacques <vincent@vincent-jacques.net>                 #
# Copyright 2012 Zearin <zearin@gonk.net>                                      #
# Copyright 2013 Ed Jackson <ed.jackson@gmail.com>                             #
# Copyright 2013 Vincent Jacques <vincent@vincent-jacques.net>                 #
# Copyright 2014 Vincent Jacques <vincent@vincent-jacques.net>                 #
# Copyright 2016 Peter Buckley <dx-pbuckley@users.noreply.github.com>          #
# Copyright 2018 sfdye <tsfdye@gmail.com>                                      #
#                                                                              #
# This file is part of PyGithub.                                               #
# http://pygithub.readthedocs.io/                                              #
#                                                                              #
# PyGithub is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU Lesser General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.             #
#                                                                              #
################################################################################

import datetime

import Framework


class RateLimiting(Framework.TestCase):
    def testRateLimiting(self):
        self.assertEqual(self.g.rate_limiting, (4929, 5000))
        self.g.get_user("jacquev6")
        self.assertEqual(self.g.rate_limiting, (4928, 5000))
        self.assertEqual(self.g.rate_limiting_resettime, 1536123356)

    def testSearchRateLimiting(self):
        self.assertEqual(self.g.rate_limiting, (4991, 5000))
        self.g.get_user("jacquev6")
        self.assertEqual(self.g.rate_limiting, (4990, 5000))
        self.assertEqual(self.g.rate_limiting_resettime, 1561025835)
        users_list = self.g.search_users("Linus Torvalds")
        torvalds = users_list[0]
        self.assertEqual(self.g.rate_limiting, (4990, 5000))
        self.assertEqual(self.g.rate_limiting_resettime, 1561025835)
        self.assertEqual(self.g.search_rate_limiting, (29, 30))
        self.assertEqual(self.g.search_rate_limiting_resettime, 1561022312)
        self.g.get_user("jacquev6")
        self.assertEqual(self.g.rate_limiting, (4989, 5000))
        self.assertEqual(self.g.rate_limiting_resettime, 1561025868)
        self.assertEqual(self.g.search_rate_limiting, (29, 30))
        self.assertEqual(self.g.search_rate_limiting_resettime, 1561022312)

    def testResetTime(self):
        self.assertEqual(self.g.rate_limiting_resettime, 1536123356)

    def testGetRateLimit(self):
        rateLimit = self.g.get_rate_limit()
        self.assertEqual(rateLimit.core.limit, 5000)
        self.assertEqual(rateLimit.core.remaining, 4929)
        self.assertEqual(rateLimit.core.reset, datetime.datetime(2018, 9, 5, 4, 55, 56))
