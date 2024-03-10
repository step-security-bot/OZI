# ozi/spec/_license.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""License specification constants."""
SPDX_LICENSE_MAP = {
    'Private': ('LicenseRef-Proprietary',),
    'DFSG approved': (
        'AGPL-3.0-only',
        'AGPL-3.0-or-later',
        'Apache-2.0',
        'Artistic-2.0',
        'BSD-3-Clause',
        'CC-BY-4.0',
        'CC-BY-SA-4.0',
        'EPL-1.0',
        'GPL-2.0-only',
        'GPL-2.0-or-later',
        'GPL-3.0-only',
        'GPL-3.0-or-later',
        'ISC',
        'LGPL-2.1-or-later',
        'LGPL-3.0-only',
        'LGPL-3.0-or-later',
        'MIT',
        'OFL-1.1',
        'WTFPL',
        'Zlib',
    ),
    'OSI Approved :: Academic Free License (AFL)': ('AFL-3.0',),
    'OSI Approved :: Apache Software License': ('Apache-2.0',),
    'OSI Approved :: Apple Public Source License': (
        'APSL-1.0',
        'APSL-1.1',
        'APSL-1.2',
        'APSL-2.0',
    ),
    'OSI Approved :: Artistic License': ('Artistic-2.0',),
    'OSI Approved :: BSD License': (
        '0BSD',
        'BSD-2-Clause',
        'BSD-3-Clause',
        'BSD-3-Clause-Clear',
        'BSD-4-Clause',
    ),
    'OSI Approved :: GNU Affero General Public License v3': (
        'AGPL-3.0-only',
        'AGPL-3.0-or-later',
    ),
    'OSI Approved :: GNU Free Documentation License (FDL)': (
        'GFDL-1.3-only',
        'GFDL-1.3-or-later',
    ),
    'OSI Approved :: GNU General Public License (GPL)': (
        'GPL-2.0-only',
        'GPL-2.0-or-later',
        'GPL-3.0-only',
        'GPL-3.0-or-later',
    ),
    'OSI Approved :: GNU General Public License v2 (GPLv2)': (
        'GPL-2.0-only',
        'GPL-2.0-or-later',
    ),
    'OSI Approved :: GNU General Public License v3 (GPLv3)': (
        'GPL-3.0-only',
        'GPL-3.0-or-later',
    ),
    'OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)': ('LGPL-2.0-only',),
    'OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)': (
        'LGPL-2.1-or-later',
    ),
    'OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)': (
        'LGPL-3.0-only',
        'LGPL-3.0-or-later',
    ),
    'OSI Approved :: GNU Library or Lesser General Public License (LGPL)': (
        'LGPL-2.1-or-later',
        'LGPL-3.0-only',
        'LGPL-3.0-or-later',
    ),
    'Public Domain': ('LicenseRef-Public-Domain', 'CC0-1.0', 'Unlicense'),
}
SPDX_LICENSE_EXCEPTIONS = (
    '389-exception',
    'Asterisk-exception',
    'Autoconf-exception-2.0',
    'Autoconf-exception-3.0',
    'Autoconf-exception-generic',
    'Autoconf-exception-macro',
    'Bison-exception-2.2',
    'Bootloader-exception',
    'Classpath-exception-2.0',
    'CLISP-exception-2.0',
    'cryptsetup-OpenSSL-exception',
    'DigiRule-FOSS-exception',
    'eCos-exception-2.0',
    'Fawkes-Runtime-exception',
    'FLTK-exception',
    'Font-exception-2.0',
    'freertos-exception-2.0',
    'GCC-exception-2.0',
    'GCC-exception-3.1',
    'GNAT-exception',
    'gnu-javamail-exception',
    'GPL-3.0-interface-exception',
    'GPL-3.0-linking-exception',
    'GPL-3.0-linking-source-exception',
    'GPL-CC-1.0',
    'GStreamer-exception-2005',
    'GStreamer-exception-2008',
    'i2p-gpl-java-exception',
    'KiCad-libraries-exception',
    'LGPL-3.0-linking-exception',
    'libpri-OpenH323-exception',
    'Libtool-exception',
    'Linux-syscall-note',
    'LLGPL',
    'LLVM-exception',
    'LZMA-exception',
    'mif-exception',
    'OCaml-LGPL-linking-exception',
    'OCCT-exception-1.0',
    'OpenJDK-assembly-exception-1.0',
    'openvpn-openssl-exception',
    'PS-or-PDF-font-exception-20170817',
    'QPL-1.0-INRIA-2004-exception',
    'Qt-GPL-exception-1.0',
    'Qt-LGPL-exception-1.1',
    'Qwt-exception-1.0',
    'SHL-2.0',
    'SHL-2.1',
    'SWI-exception',
    'Swift-exception',
    'u-boot-exception-2.0',
    'Universal-FOSS-exception-1.0',
    'vsftpd-openssl-exception',
    'WxWindows-exception-3.1',
    'x11vnc-openssl-exception',
)
