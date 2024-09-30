
/*
 * Copyright (c) 2013-2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 *
 * This software is available to you under a choice of one of two
 * licenses.  You may choose to be licensed under the terms of the GNU
 * General Public License (GPL) Version 2, available from the file
 * COPYING in the main directory of this source tree, or the
 * OpenIB.org BSD license below:
 *
 *     Redistribution and use in source and binary forms, with or
 *     without modification, are permitted provided that the following
 *     conditions are met:
 *
 *      - Redistributions of source code must retain the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer.
 *
 *      - Redistributions in binary form must reproduce the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer in the documentation and/or other materials
 *        provided with the distribution.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include "mtcr_mem_ops.h"

#if defined(__WIN__) || defined(MST_UL) || defined(__FreeBSD__) || defined(__VMKERNEL_UW_NATIVE__)
#else
// #include "mst_pciconf.h"
#include <sys/ioctl.h>
#endif

#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int mtcr_memaccess(mfile* mf, unsigned int offset, unsigned int size, unsigned char* data, int rw, mem_type_t type)
{
    (void)type;
    (void)mf;
    (void)offset;
    (void)size;
    (void)data;
    (void)rw;
    return ME_UNSUPPORTED_OPERATION;
}

int get_mem_props(mfile* mf, mem_type_t type, mem_props_t* props)
{
    (void)mf;
    (void)type;
    (void)props;
    return ME_UNSUPPORTED_OPERATION;
}

void init_mem_ops(mfile* mf)
{
    (void)mf;
}

void close_mem_ops(mfile* mf)
{
    if (mf->dma_props)
    {
        free(mf->dma_props);
        mf->dma_props = NULL;
    }
}
