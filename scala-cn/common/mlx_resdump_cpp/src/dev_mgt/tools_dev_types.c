/*
 * Copyright (C) Jan 2013 Mellanox Technologies Ltd. All rights reserved.
 * Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
 *
 * End of legal section ......................................................
 *
 *  toos_dev_types.c - Defines static info records for all mellanox chips in order to
 *                     have a uniform IDs and info for all tools.
 *
 *  Version: $Id$
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <reg_access.h>
#include <reg_access_hca_layouts.h>
#include "tools_dev_types.h"

enum dm_dev_type {
    DM_UNKNOWN = -1,
    DM_HCA,
    DM_SWITCH,
    DM_BRIDGE,
    DM_QSFP_CABLE,
    DM_CMIS_CABLE,
    DM_SFP_CABLE,
    DM_LINKX, /* linkx chip */
    DM_GEARBOX,
    DM_RETIMER
};

struct device_info {
    dm_dev_id_t      dm_id;
    u_int16_t        hw_dev_id;
    int              hw_rev_id; /* -1 means all revisions match this record */
    int              sw_dev_id; /* -1 means all hw ids  match this record */
    const char     * name;
    int              port_num;
    enum dm_dev_type dev_type;
};

#define DEVID_ADDR                                         0xf0014
#define CABLEID_ADDR                                       0x0
#define SFP_DIGITAL_DIAGNOSTIC_MONITORING_IMPLEMENTED_ADDR 92
#define SFP_PAGING_IMPLEMENTED_INDICATOR_ADDR              64

#define ARDBEG_REV0_DEVID       0x6e
#define ARDBEG_REV1_DEVID       0x7e
#define ARDBEG_MIRRORED_DEVID   0x70
#define BARITONE_DEVID          0x6b
#define BARITONE_MIRRORED_DEVID 0x71
#define MENHIT_DEVID_VER0       0x6f
#define MENHIT_DEVID_VER1       0x72
#define MENHIT_DEVID_VER2       0x73
#define ARCUS_P_TC_DEVID        0x7f
#define ARCUS_P_REV0_DEVID      0x80
#define ARCUS_E_REV0_DEVID      0x81

#ifdef CABLES_SUPP
enum dm_dev_type getCableType(u_int8_t id)
{
    switch (id) {
    case 0xd:
    case 0x11:
    case 0xe:
    case 0xc:
        return DM_QSFP_CABLE;

    case 0x3:
        return DM_SFP_CABLE;

    case 0x18:
    case 0x19:     /* Stallion2 */
    case 0x1e:
        return DM_CMIS_CABLE;

    default:
        return DM_UNKNOWN;
    }
}
#endif

static struct device_info g_devs_info[] = {
    {
        DeviceConnectX3,                                      /* dm_id */
        0x1f5,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        -1,                                                   /* sw_dev_id */
        "ConnectX3",                                          /* name */
        2,                                                    /* port_num */
        DM_HCA                                                /* dev_type */
    },
    {
        DeviceConnectIB,                                      /* dm_id */
        0x1ff,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        4113,                                                 /* sw_dev_id */
        "ConnectIB",                                          /* name */
        2,                                                    /* port_num */
        DM_HCA                                                /* dev_type */
    },
    {
        DeviceConnectX3Pro,                                      /* dm_id */
        0x1f7,                                                   /* hw_dev_id */
        -1,                                                      /* hw_rev_id */
        4103,                                                    /* sw_dev_id */
        "ConnectX3Pro",                                          /* name */
        2,                                                       /* port_num */
        DM_HCA                                                   /* dev_type */
    },
    {
        DeviceSwitchIB,                                      /* dm_id */
        0x247,                                               /* hw_dev_id */
        -1,                                                  /* hw_rev_id */
        52000,                                               /* sw_dev_id */
        "SwitchIB",                                          /* name */
        36,                                                  /* port_num */
        DM_SWITCH                                            /* dev_type */
    },
    {
        DeviceSpectrum,                                      /* dm_id */
        0x249,                                               /* hw_dev_id */
        -1,                                                  /* hw_rev_id */
        52100,                                               /* sw_dev_id */
        "Spectrum",                                          /* name */
        64,                                                  /* port_num */
        DM_SWITCH                                            /* dev_type */
    },
    {
        DeviceConnectX4,                                      /* dm_id */
        0x209,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        4115,                                                 /* sw_dev_id */
        "ConnectX4",                                          /* name */
        2,                                                    /* port_num */
        DM_HCA                                                /* dev_type */
    },
    {
        DeviceConnectX4LX,                                      /* dm_id */
        0x20b,                                                  /* hw_dev_id */
        -1,                                                     /* hw_rev_id */
        4117,                                                   /* sw_dev_id */
        "ConnectX4LX",                                          /* name */
        2,                                                      /* port_num */
        DM_HCA                                                  /* dev_type */
    },
    {
        DeviceConnectX5,                                      /* dm_id */
        0x20d,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        4119,                                                 /* sw_dev_id */
        "ConnectX5",                                          /* name */
        2,                                                    /* port_num */
        DM_HCA                                                /* dev_type */
    },
    {
        DeviceConnectX6,                                      /* dm_id */
        0x20f,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        4123,                                                 /* sw_dev_id */
        "ConnectX6",                                          /* name */
        2,                                                    /* port_num */
        DM_HCA                                                /* dev_type */
    },
    {
        DeviceConnectX6DX,                                      /* dm_id */
        0x212,                                                  /* hw_dev_id */
        -1,                                                     /* hw_rev_id */
        4125,                                                   /* sw_dev_id */
        "ConnectX6DX",                                          /* name */
        2,                                                      /* port_num */
        DM_HCA                                                  /* dev_type */
    },
    {
        DeviceConnectX6LX,                                      /* dm_id */
        0x216,                                                  /* hw_dev_id */
        -1,                                                     /* hw_rev_id */
        4127,                                                   /* sw_dev_id */
        "ConnectX6LX",                                          /* name */
        2,                                                      /* port_num */
        DM_HCA                                                  /* dev_type */
    },
    {
        DeviceConnectX7,                                      /* dm_id */
        0x218,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        4129,                                                 /* sw_dev_id */
        "ConnectX7",                                          /* name */
        4,                                                    /* port_num */
        DM_HCA                                                /* dev_type */
    },
    {
        DeviceConnectX8,                                      /* dm_id */
        0x21e,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        -1,                                                   /* sw_dev_id */
        "ConnectX8",                                          /* name */
        4,                                                    /* port_num */
        DM_HCA                                                /* dev_type */
    },
    {
        DeviceBlueField,                                      /* dm_id */
        0x211,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        41682,                                                /* sw_dev_id */
        "BlueField",                                          /* name */
        2,                                                    /* port_num */
        DM_HCA                                                /* dev_type */
    },
    {
        DeviceBlueField2,                                      /* dm_id */
        0x214,                                                 /* hw_dev_id */
        -1,                                                    /* hw_rev_id */
        41686,                                                 /* sw_dev_id */
        "BlueField2",                                          /* name */
        2,                                                     /* port_num */
        DM_HCA                                                 /* dev_type */
    },
    {
        DeviceBlueField3,                                      /* dm_id */
        0x21c,                                                 /* hw_dev_id */
        -1,                                                    /* hw_rev_id */
        41692,                                                 /* sw_dev_id */
        "BlueField3",                                          /* name */
        4,                                                     /* port_num */
        DM_HCA                                                 /* dev_type */
    },
    {
        DeviceBlueField4,                                      /* dm_id */
        0x220,                                                 /* hw_dev_id */
        -1,                                                    /* hw_rev_id */
        41694,                                                 /* sw_dev_id */
        "BlueField4",                                          /* name */
        4,                                                     /* port_num */
        DM_HCA                                                 /* dev_type */
    },
    {
        DeviceSwitchIB2,                                      /* dm_id */
        0x24b,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        53000,                                                /* sw_dev_id */
        "SwitchIB2",                                          /* name */
        36,                                                   /* port_num */
        DM_SWITCH                                             /* dev_type */
    },
    {
        DeviceCableQSFP,                                      /* dm_id */
        0x0d,                                                 /* hw_dev_id */
        0,                                                    /* hw_rev_id */
        -1,                                                   /* sw_dev_id */
        "CableQSFP",                                          /* name */
        -1,                                                   /* port_num */
        DM_QSFP_CABLE                                         /* dev_type */
    },
    {
        DeviceCableQSFPaging,                                      /* dm_id */
        0x11,                                                      /* hw_dev_id */
        0xab,                                                      /* hw_rev_id */
        -1,                                                        /* sw_dev_id */
        "CableQSFPaging",                                          /* name */
        -1,                                                        /* port_num */
        DM_QSFP_CABLE                                              /* dev_type */
    },
    {
        DeviceCableCMIS,                                      /* dm_id */
        0x19,                                                 /* hw_dev_id */
        0,                                                    /* hw_rev_id */
        -1,                                                   /* sw_dev_id */
        "CableCMIS",                                          /* name */
        -1,                                                   /* port_num */
        DM_CMIS_CABLE                                         /* dev_type */
    },
    {
        DeviceCableCMISPaging,                                      /* dm_id */
        0x19,                                                       /* hw_dev_id */
        0xab,                                                       /* hw_rev_id */
        -1,                                                         /* sw_dev_id */
        "CableCMISPaging",                                          /* name */
        -1,                                                         /* port_num */
        DM_CMIS_CABLE                                               /* dev_type */
    },
    {
        DeviceCableSFP,                                      /* dm_id */
        0x03,                                                /* hw_dev_id */
        1,                                                   /* hw_rev_id */
        -1,                                                  /* sw_dev_id */
        "CableSFP",                                          /* name */
        -1,                                                  /* port_num */
        DM_SFP_CABLE                                         /* dev_type */
    },
    {
        DeviceCableSFP51,                                      /* dm_id */
        0x03,                                                  /* hw_dev_id */
        1,                                                     /* hw_rev_id */
        -1,                                                    /* sw_dev_id */
        "CableSFP51",                                          /* name */
        -1,                                                    /* port_num */
        DM_SFP_CABLE                                           /* dev_type */
    },
    {
        DeviceCableSFP51Paging,                                      /* dm_id */
        0x03,                                                        /* hw_dev_id */
        1,                                                           /* hw_rev_id */
        -1,                                                          /* sw_dev_id */
        "CableSFP51Paging",                                          /* name */
        -1,                                                          /* port_num */
        DM_SFP_CABLE                                                 /* dev_type */
    },
    {
        DeviceSpectrum2,                                      /* dm_id */
        0x24e,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        53100,                                                /* sw_dev_id */
        "Spectrum2",                                          /* name */
        128,                                                  /* port_num */
        DM_SWITCH                                             /* dev_type */
    },
    {
        DeviceDummy,                                        /* dm_id */
        0x1,                                                /* hw_dev_id */
        -1,                                                 /* hw_rev_id */
        -1,                                                 /* sw_dev_id */
        "DummyDevice",                                      /* name */
        2,                                                  /* port_num */
        DM_HCA                                              /* dev_type */
    },
    {
        DeviceQuantum,                                      /* dm_id */
        0x24d,                                              /* hw_dev_id */
        -1,                                                 /* hw_rev_id */
        54000,                                              /* sw_dev_id */
        "Quantum",                                          /* name */
        80,                                                 /* port_num */
        DM_SWITCH                                           /* dev_type */
    },
    {
        DeviceArdbeg,                                      /* dm_id */
        0x6e,                                              /* hw_dev_id (ArdbegMirror 0x70) */
        -1,                                                /* hw_rev_id */
        -1,                                                /* sw_dev_id */
        "Ardbeg",                                          /* name */
        -1,                                                /* port_num */
        DM_LINKX                                           /* dev_type */
    },
    {
        DeviceBaritone,                                      /* dm_id */
        0x6b,                                                /* hw_dev_id (BaritoneMirror 0x71) */
        -1,                                                  /* hw_rev_id */
        -1,                                                  /* sw_dev_id */
        "Baritone",                                          /* name */
        -1,                                                  /* port_num */
        DM_LINKX                                             /* dev_type */
    },
    {
        DeviceMenhit,                                      /* dm_id */
        0x72,                                              /* hw_dev_id (other versions 0x6f,0x73) */
        -1,                                                /* hw_rev_id */
        -1,                                                /* sw_dev_id */
        "Menhit",                                          /* name */
        -1,                                                /* port_num */
        DM_LINKX                                           /* dev_type */
    },
    {
        DeviceArcusPTC,                                          /* dm_id */
        0x7f,                                                    /* hw_dev_id */
        -1,                                                      /* hw_rev_id */
        -1,                                                      /* sw_dev_id */
        "ArcusP Test-Chip",                                      /* name */
        -1,                                                      /* port_num */
        DM_LINKX                                                 /* dev_type */
    },
    {
        DeviceArcusP,                                      /* dm_id */
        0x80,                                              /* hw_dev_id (other versions 0x6f,0x73) */
        -1,                                                /* hw_rev_id */
        -1,                                                /* sw_dev_id */
        "ArcusP",                                          /* name */
        -1,                                                /* port_num */
        DM_LINKX                                           /* dev_type */
    },
    {
        DeviceArcusE,                                      /* dm_id */
        0x81,                                              /* hw_dev_id (other versions 0x6f,0x73) */
        -1,                                                /* hw_rev_id */
        -1,                                                /* sw_dev_id */
        "ArcusE",                                          /* name */
        -1,                                                /* port_num */
        DM_LINKX                                           /* dev_type */
    },
    {
        DeviceArcusE, // dm_id
        0xb200,       // hw_dev_id (other versions 0x6f,0x73)
        -1,           // hw_rev_id
        -1,           // sw_dev_id
        "ArcusE",     // name
        -1,           // port_num
        DM_RETIMER    // dev_type
    },
    {
        DeviceSecureHost,                                      /* dm_id */
        0xcafe,                                                /* hw_dev_id */
        0xd0,                                                  /* hw_rev_id */
        0,                                                     /* sw_dev_id */
        "Unknown Device",                                      /* name */
        -1,                                                    /* port_num */
        DM_UNKNOWN                                             /* dev_type */
    },
    {
        DeviceSpectrum3,                                      /* dm_id */
        0x250,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        53104,                                                /* sw_dev_id */
        "Spectrum3",                                          /* name */
        128,                                                  /* port_num NEED_CHECK */
        DM_SWITCH                                             /* dev_type */
    },
    {
        DeviceSpectrum4,                                      /* dm_id */
        0x254,                                                /* hw_dev_id */
        -1,                                                   /* hw_rev_id */
        53120,                                                /* sw_dev_id */
        "Spectrum4",                                          /* name */
        128,                                                  /* port_num NEED_CHECK */
        DM_SWITCH                                             /* dev_type */
    },
    {
        DeviceQuantum2,                                      /* dm_id */
        0x257,                                               /* hw_dev_id */
        -1,                                                  /* hw_rev_id */
        54002,                                               /* sw_dev_id */
        "Quantum2",                                          /* name */
        128,                                                 /* port_num NEED_CHECK */
        DM_SWITCH                                            /* dev_type */
    },
    {
        DeviceQuantum3,                                      /* dm_id */
        0x25b,                                              /* hw_dev_id */
        -1,                                                  /* hw_rev_id */
        54004,                                               /* sw_dev_id */
        "Quantum3",                                          /* name */
        128,                                                 /* port_num NEED_CHECK */
        DM_SWITCH                                            /* dev_type */
    },
    {
        DeviceBW00,                                      /* dm_id */
        0x2900,                                           /* hw_dev_id */
        -1,                                               /* hw_rev_id */
        10496,                                            /* sw_dev_id */
        "BW00",                                          /* name */
        128,                                              /* port_num NEED_CHECK */
        DM_SWITCH                                         /* dev_type */
    },
    {
        DeviceGearBox,                                      /* dm_id */
        0x252,                                              /* hw_dev_id */
        -1,                                                 /* hw_rev_id */
        53108,                                              /* sw_dev_id */
        "AmosGearBox",                                      /* name */
        128,                                                /* port_num NEED_CHECK */
        DM_GEARBOX                                          /* dev_type */
    },
    {
        DeviceGearBoxManager,                                      /* dm_id */
        0x253,                                                     /* hw_dev_id */
        -1,                                                        /* hw_rev_id */
        -1,                                                        /* sw_dev_id */
        "AmosGearBoxManager",                                      /* name */
        -1,                                                        /* port_num NEED_CHECK */
        DM_GEARBOX                                                 /* dev_type */
    },
    {
        DeviceAbirGearBox,                                      /* dm_id */
        0x256,                                                  /* hw_dev_id */
        -1,                                                     /* hw_rev_id */
        -1,                                                     /* sw_dev_id */
        "AbirGearBox",                                          /* name */
        -1,                                                     /* port_num NEED_CHECK */
        DM_GEARBOX                                              /* dev_type */
    },
    {
        DeviceUnknown,                                         /* dm_id */
        0,                                                     /* hw_dev_id */
        0,                                                     /* hw_rev_id */
        0,                                                     /* sw_dev_id */
        "Unknown Device",                                      /* name */
        -1,                                                    /* port_num */
        DM_UNKNOWN                                             /* dev_type */
    }
};

static const struct device_info* get_entry(dm_dev_id_t type)
{
    const struct device_info* p = g_devs_info;

    while (p->dm_id != DeviceUnknown) {
        if (type == p->dm_id) {
            break;
        }
        p++;
    }
    return p;
}

static const struct device_info* get_entry_by_dev_rev_id(u_int32_t hw_dev_id, u_int32_t hw_rev_id)
{
    const struct device_info* p = g_devs_info;

    while (p->dm_id != DeviceUnknown) {
        if (hw_dev_id == p->hw_dev_id) {
            if ((p->hw_rev_id == -1) || ((int)hw_rev_id == p->hw_rev_id)) {
                break;
            }
        }
        p++;
    }
    return p;
}

typedef enum get_dev_id_error_t {
    GET_DEV_ID_SUCCESS,
    GET_DEV_ID_ERROR,
    CRSPACE_READ_ERROR,
    CHECK_PTR_DEV_ID,
} dev_id_error;

const char* dm_dev_type2str(dm_dev_id_t type)
{
    return get_entry(type)->name;
}

dm_dev_id_t dm_dev_str2type(const char* str)
{
    const struct device_info* p = g_devs_info;

    if (!str) {
        return DeviceUnknown;
    }
    while (p->dm_id != DeviceUnknown) {
        if (strcmp(str, p->name) == 0) {
            return p->dm_id;
        }
        p++;
    }
    return DeviceUnknown;
}

dm_dev_id_t dm_dev_aproxstr2type(const char* str)
{
    const struct device_info* p = g_devs_info;
    char                      d_str[256];

    if (!str) {
        return DeviceUnknown;
    }
    while (p->dm_id != DeviceUnknown) {
        /* to lowercase */
        unsigned short i;
        for (i = 0; i <= strlen(p->name); ++i) {
            if (((p->name)[i] >= 'A') && ((p->name)[i] <= 'Z')) {
                d_str[i] = (p->name)[i] + 'a' - 'A';
            } else {
                d_str[i] = (p->name)[i];
            }
        }

        if (strncmp(str, d_str, strlen(d_str)) == 0) {
            return p->dm_id;
        }
        p++;
    }
    return DeviceUnknown;
}

dm_dev_id_t dm_dev_sw_id2type(int sw_dev_id)
{
    const struct device_info* p = g_devs_info;

    while (p->dm_id != DeviceUnknown) {
        if (sw_dev_id == p->sw_dev_id) {
            return p->dm_id;
        }
        p++;
    }
    return DeviceUnknown;
}

int dm_get_hw_ports_num(dm_dev_id_t type)
{
    return get_entry(type)->port_num;
}

int dm_dev_is_hca(dm_dev_id_t type)
{
    return (!dm_dev_is_dummy(type)) && (get_entry(type)->dev_type == DM_HCA);
}

int dm_dev_is_dummy(dm_dev_id_t type)
{
    return type == DeviceDummy;
}

int dm_dev_is_gearbox(dm_dev_id_t type)
{
    return (get_entry(type)->dev_type == DM_GEARBOX);
}

int dm_is_menhit(dm_dev_id_t type)
{
    return type == DeviceMenhit || type == DeviceArcusPTC || type == DeviceArcusP || type == DeviceArcusE;
}

int dm_dev_is_200g_speed_supported_hca(dm_dev_id_t type)
{
    bool isBlueField = (type == DeviceBlueField || type == DeviceBlueField2 || type == DeviceBlueField3);

    return !isBlueField &&
           (dm_dev_is_hca(type) && (get_entry(type)->hw_dev_id >= get_entry(DeviceConnectX6)->hw_dev_id));
}

int dm_dev_is_switch(dm_dev_id_t type)
{
    return get_entry(type)->dev_type == DM_SWITCH;
}

int dm_dev_is_200g_speed_supported_switch(dm_dev_id_t type)
{
    return (dm_dev_is_switch(type) && (get_entry(type)->hw_dev_id >= get_entry(DeviceQuantum)->hw_dev_id));
}

int dm_dev_is_bridge(dm_dev_id_t type)
{
    return get_entry(type)->dev_type == DM_BRIDGE;
}

int dm_dev_is_qsfp_cable(dm_dev_id_t type)
{
    return get_entry(type)->dev_type == DM_QSFP_CABLE;
}

int dm_dev_is_sfp_cable(dm_dev_id_t type)
{
    return get_entry(type)->dev_type == DM_SFP_CABLE;
}

int dm_dev_is_cmis_cable(dm_dev_id_t type)
{
    return get_entry(type)->dev_type == DM_CMIS_CABLE;
}

int dm_dev_is_cable(dm_dev_id_t type)
{
    return (type == DeviceCable || dm_dev_is_qsfp_cable(type) || dm_dev_is_sfp_cable(type) ||
            dm_dev_is_cmis_cable(type));
}

int dm_dev_is_retimer_arcuse(dm_dev_id_t type)
{
    return get_entry(type)->dev_type == DM_RETIMER && type == DeviceArcusE;
}

u_int32_t dm_get_hw_dev_id(dm_dev_id_t type)
{
    return get_entry(type)->hw_dev_id;
}

u_int32_t dm_get_hw_rev_id(dm_dev_id_t type)
{
    return get_entry(type)->hw_rev_id;
}

int dm_is_fpp_supported(dm_dev_id_t type)
{
    /* Function per port is supported only in HCAs that arrived after CX3 */
    const struct device_info* dp = get_entry(type);

    return dm_is_5th_gen_hca(dp->dm_id);
}

int dm_is_device_supported(dm_dev_id_t type)
{
    return get_entry(type)->dm_id != DeviceUnknown;
}

int dm_is_4th_gen(dm_dev_id_t type)
{
    return (type == DeviceConnectX3 || type == DeviceConnectX3Pro);
}

int dm_is_5th_gen_hca(dm_dev_id_t type)
{
    return (dm_dev_is_hca(type) && !dm_is_4th_gen(type));
}

int dm_is_connectib(dm_dev_id_t type)
{
    return (type == DeviceConnectIB);
}

int dm_is_bw00(dm_dev_id_t type)
{
    return (type == DeviceBW00);
}

int dm_is_cx7(dm_dev_id_t type)
{
    return (type == DeviceConnectX7);
}

int dm_is_new_gen_switch(dm_dev_id_t type)
{
    return dm_dev_is_switch(type);
}

int dm_dev_is_raven_family_switch(dm_dev_id_t type)
{
    return (dm_dev_is_switch(type) &&
            (type == DeviceQuantum || type == DeviceQuantum2 || type == DeviceQuantum3 || type == DeviceBW00 ||
             type == DeviceSpectrum2 || type == DeviceSpectrum3 || type == DeviceSpectrum4));
}

int dm_dev_is_ib_switch(dm_dev_id_t type)
{
    return (dm_dev_is_switch(type) && (type == DeviceQuantum || type == DeviceQuantum2 || type == DeviceQuantum3 ||
                                       type == DeviceBW00 || type == DeviceSwitchIB || type == DeviceSwitchIB2));
}

int dm_dev_is_eth_switch(dm_dev_id_t type)
{
    return (dm_dev_is_switch(type) &&
            (type == DeviceSpectrum || type == DeviceSpectrum2 || type == DeviceSpectrum3 || type == DeviceSpectrum4));
}

int dm_dev_is_fs3(dm_dev_id_t type)
{
    return type == DeviceConnectIB || type == DeviceSwitchIB || type == DeviceConnectX4 || type == DeviceConnectX4LX ||
           type == DeviceSpectrum || type == DeviceSwitchIB2;
}

int dm_dev_is_fs4(dm_dev_id_t type)
{
    return type == DeviceConnectX5 || type == DeviceConnectX6 || type == DeviceConnectX6DX ||
           type == DeviceConnectX6LX || type == DeviceConnectX7 || type == DeviceBlueField ||
           type == DeviceBlueField2 || type == DeviceBlueField3 || type == DeviceQuantum || type == DeviceQuantum2 ||
           type == DeviceSpectrum4 || type == DeviceSpectrum2 || type == DeviceSpectrum3 || type == DeviceGearBox ||
           type == DeviceGearBoxManager;
}

int dm_dev_is_fs5(dm_dev_id_t type)
{
    return type == DeviceConnectX8 || type == DeviceQuantum3 || type == DeviceBlueField4;
}

int dm_is_ib_access(mfile* mf)
{
    return (mf->flags & MDEVS_IB);
}
