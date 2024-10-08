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
# DumpCommand.py
# Python implementation of the Class DumpCommand
# Generated by Enterprise Architect
# Created on:      14-Aug-2019 10:12:00 AM
#
#######################################################
from common.mlx_resdump.resourcedump_lib.commands.ResDumpCommand import ResDumpCommand
from common.mlx_resdump.resourcedump_lib.commands.QueryCommand import QueryCommand
from common.mlx_resdump.resourcedump_lib.commands.CommandFactory import CommandFactory
from common.mlx_resdump.resourcedump_lib.utils import constants as cs
from common.mlx_resdump.resourcedump_lib.validation.CapabilityValidator import CapabilityValidator

from common.mlx_resdump.resourcedump_lib.cresourcedump.CResourceDump import CResourceDump
from common.mlx_resdump.resourcedump_lib.cresourcedump.cresourcedump_types import c_device_attributes, c_dump_request
from common.mlx_resdump.segments.MenuSegment import MenuSegment


class DumpCommand(ResDumpCommand):
    """This class is responsible for performing the dump command flow by validate,
    getting the data and print it.
    """
    __MENU: MenuSegment = None

    def __init__(self, **kwargs):
        """DumpCommand initialization.
        """
        super().__init__()

        self.device_name = kwargs['device']
        self.segment = kwargs['segment']
        self.vHCAid = kwargs.get('vHCAid', cs.DEFAULT_VHCA)
        self.index1 = kwargs.get('index1', 0)
        self.index2 = kwargs.get('index2', 0)
        self.numOfObj1 = kwargs.get('numOfObj1', 0)
        self.numOfObj2 = kwargs.get('numOfObj2', 0)
        self.depth = kwargs.get('depth', cs.INF_DEPTH)
        self.bin = kwargs.get('bin', None)
        self.mem = kwargs.get('mem', "")

    def retrieve_data(self):
        """Validate request availability with QueryCommand and retrieve dump data using SDK.
        """
        if DumpCommand.__MENU is None:
            DumpCommand.__MENU = QueryCommand(device=self.device_name, vHCAid=self.vHCAid, mem=self.mem).get_segments()[0]

        # validate that the dump supported by calling ArgToMenuVerifier
        DumpCommand.__MENU.verify_support(segment=self.segment, index1=self.index1, index2=self.index2, numOfObj1=self.numOfObj1, numOfObj2=self.numOfObj2)
        # segment type can be name, this method will convert the name (if needed) to seg number in hex (str)
        if (type(self.segment is str)):
            self.segment = DumpCommand.__MENU.get_segment_type_by_segment_name(self.segment)

        if not self.bin:
            self.retrieve_data_from_sdk()
        else:
            self.dump_to_file_with_sdk()

    def dump_to_file_with_sdk(self):
        device_name = bytes(self.device_name, "utf-8")
        rdma_name = bytes(self.mem, "utf-8")

        device_attrs = c_device_attributes(device_name, self.vHCAid, rdma_name)
        dump_request = c_dump_request(self.segment, self.index1, self.index2, self.numOfObj1, self.numOfObj2)
        bin_filename = bytes(self.bin, "utf-8")
        # dump to file is done with BE as default as convention
        if CResourceDump.c_dump_resource_to_file(device_attrs, dump_request, self.depth, bin_filename, 1) != 0:
            raise Exception(CResourceDump.c_get_resource_dump_error().decode("utf-8"))
        print("write to file: ", self.bin)

    def validate(self):
        """call the capability validator and check if the core dump supported by the FW.
        """
        validation_status = False

        if CapabilityValidator.validate():
            validation_status = True
        else:
            print("resource dump register is not supported by FW")

        return validation_status


CommandFactory.register(cs.RESOURCE_DUMP_COMMAND_TYPE_DUMP, DumpCommand)
