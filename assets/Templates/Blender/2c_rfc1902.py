#
# This file is part of pyasn1-modules software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pyasn1/license.html
#
# SNMPv2c message syntax
#
# ASN.1 source from:
 # http://www.ietf.org/rfc/rfc1902.txt
#
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ


class Integer(univ.Integer):
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 -2147483648, 2147483647
# BRACKET_SURGEON: disabled
# )


class Integer32(univ.Integer):
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 -2147483648, 2147483647
# BRACKET_SURGEON: disabled
# )


class OctetString(univ.OctetString):
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueSizeConstraint()
 0, 65535
# BRACKET_SURGEON: disabled
# )


class IpAddress(univ.OctetString):
 tagSet = univ.OctetString.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0x00)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.OctetString.subtypeSpec + constraint.ValueSizeConstraint()
 4, 4
# BRACKET_SURGEON: disabled
# )


class Counter32(univ.Integer):
 tagSet = univ.Integer.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0x01)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 0, 4294967295
# BRACKET_SURGEON: disabled
# )


class Gauge32(univ.Integer):
 tagSet = univ.Integer.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0x02)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 0, 4294967295
# BRACKET_SURGEON: disabled
# )


class Unsigned32(univ.Integer):
 tagSet = univ.Integer.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0x02)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 0, 4294967295
# BRACKET_SURGEON: disabled
# )


class TimeTicks(univ.Integer):
 tagSet = univ.Integer.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0x03)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 0, 4294967295
# BRACKET_SURGEON: disabled
# )


class Opaque(univ.OctetString):
 tagSet = univ.OctetString.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0x04)
# BRACKET_SURGEON: disabled
# )


class Counter64(univ.Integer):
 tagSet = univ.Integer.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0x06)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 0, 18446744073709551615
# BRACKET_SURGEON: disabled
# )


class Bits(univ.OctetString):
 pass


class ObjectName(univ.ObjectIdentifier):
 pass


class SimpleSyntax(univ.Choice):
 componentType = namedtype.NamedTypes()
 namedtype.NamedType('integer-value', Integer()),
 namedtype.NamedType('string-value', OctetString()),
 namedtype.NamedType('objectID-value', univ.ObjectIdentifier())
# BRACKET_SURGEON: disabled
# )


class ApplicationSyntax(univ.Choice):
 componentType = namedtype.NamedTypes()
 namedtype.NamedType('ipAddress-value', IpAddress()),
 namedtype.NamedType('counter-value', Counter32()),
 namedtype.NamedType('timeticks-value', TimeTicks()),
 namedtype.NamedType('arbitrary-value', Opaque()),
 namedtype.NamedType('big-counter-value', Counter64()),
 # This conflicts with Counter32
 # namedtype.NamedType('unsigned-integer-value', Unsigned32()),
 namedtype.NamedType('gauge32-value', Gauge32())
# BRACKET_SURGEON: disabled
# ) # BITS misplaced?


class ObjectSyntax(univ.Choice):
 componentType = namedtype.NamedTypes()
 namedtype.NamedType('simple', SimpleSyntax()),
 namedtype.NamedType('application-wide', ApplicationSyntax())
# BRACKET_SURGEON: disabled
# )