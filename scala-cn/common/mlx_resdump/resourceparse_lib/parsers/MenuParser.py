# Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software is available to you under a choice of one of two
# licenses.  You may choose to be licensed under the terms of the GNU
# General Public License (GPL) Version 2, available from the file
# COPYING in the main directory of this source tree, or the
# OpenIB.org BSD license below:
#
#     Redistribution and use in source and binary forms, with or
#     without modification, are permitted provided that the following
#     conditions are met:
#
#      - Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      - Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials
#        provided with the distribution.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#######################################################
#
# ResourceParser.py
# Created on:      26-Sep-2023 05:51:33 PM
#
#######################################################

from common.mlx_resdump.resourceparse_lib.utils import constants as cs
from common.mlx_resdump.resourceparse_lib.parsers.ResourceParser import ResourceParser, PARSER_CLASSES
from common.mlx_resdump.segments.Segment import Segment


class MenuParser(ResourceParser):
    PARSER_TYPE = "menu"

    def __init__(self, parser_args):
        pass

    def parse_segment(self, segment: Segment):
        if segment.get_type() == cs.RESOURCE_DUMP_SEGMENT_TYPE_MENU:
            for record in segment.get_printable_records():
                for el in record:
                    segment.add_parsed_data(el)

    @staticmethod
    def get_description():
        return \
            """        This parse method assumes that the provided segments contain a menu-segments
        and outputs it in a human readable structure.
"""


PARSER_CLASSES[MenuParser.PARSER_TYPE] = MenuParser
