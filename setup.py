# tzselect - A solution for generating a select field for timezones.
#
#       http://github.com/davidreynolds/tzselect
#
# Copyright 2010 David Reynolds
#
# Use and distribution licensed under the MIT license. See
# the LICENSE file for full text.

import distutils.core

distutils.core.setup(
    name="tzselect",
    version="0.1",
    packages=["tzselect"],
    author="David Reynolds",
    author_email="david@alwaysmovefast.com",
    url="http://github.com/davidreynolds/tzselect",
    license="MIT License",
    description="tzselect provides a simple solution for creating a timezone select field."
)
