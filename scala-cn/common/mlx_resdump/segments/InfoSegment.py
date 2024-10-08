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
# InfoSegment.py
# Python implementation of the Class InfoSegment
# Generated by Enterprise Architect
# Created on:      14-Aug-2019 10:11:57 AM
#
#######################################################
from common.mlx_resdump.segments.Segment import Segment
from common.mlx_resdump.segments.SegmentFactory import SegmentFactory
from common.mlx_resdump.resourcedump_lib.utils import constants

import struct
import sys


class InfoSegment(Segment):
    """this class is responsible for holding info segment data.
    """

    _segment_type_id = constants.RESOURCE_DUMP_SEGMENT_TYPE_INFO
    INFO_SEGMENT_FMT_BE = "3sBII"
    INFO_SEGMENT_FMT_LE = "B3sII"

    info_segment_struct = struct.Struct(INFO_SEGMENT_FMT_BE if sys.byteorder == 'big' else INFO_SEGMENT_FMT_LE)

    def __init__(self, data):
        """initialize the class by setting the class data.
        """
        super().__init__(data)

    def get_version(self):
        start = self.segment_header_struct.size
        if len(self.raw_data) > start:
            dump_version, hw_version, fw_version = self.unpack_info()
            return "{}.{}.{}".format(dump_version, hw_version, fw_version)
        return ""

    def unpack_info(self):
        fields = self.info_segment_struct.unpack_from(self.raw_data, self.segment_header_struct.size)
        dump_version = fields[1] if sys.byteorder == 'big' else fields[0]
        hw_version, fw_version = fields[2:]
        return dump_version, hw_version, fw_version


SegmentFactory.register(constants.RESOURCE_DUMP_SEGMENT_TYPE_INFO, InfoSegment)
