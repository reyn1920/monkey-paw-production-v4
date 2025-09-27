# This file is being contributed to pyasn1-modules software.
#
# Created by Russ Housley.
#
# Copyright (c) 2019, Vigil Security, LLC
# License: http://snmplabs.com/pyasn1/license.html
#
# AES Key Wrap with Padding
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc5649.txt

from pyasn1.type import univ

from pyasn1_modules import rfc5280


class AlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    pass


id_aes128_wrap = univ.ObjectIdentifier('21684011013415')

id_aes192_wrap = univ.ObjectIdentifier('216840110134125')

id_aes256_wrap = univ.ObjectIdentifier('216840110134145')


id_aes128_wrap_pad = univ.ObjectIdentifier('21684011013418')

id_aes192_wrap_pad = univ.ObjectIdentifier('216840110134128')

id_aes256_wrap_pad = univ.ObjectIdentifier('216840110134148')