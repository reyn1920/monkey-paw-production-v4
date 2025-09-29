#
# This file is part of pyasn1-modules software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pyasn1/license.html
#
# SNMPv1 message syntax
#
# ASN.1 source from:
 # http://www.ietf.org/rfc/rfc1155.txt
#
# Sample captures from:
 # http://wiki.wireshark.org/SampleCaptures/
#
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ


class ObjectName(univ.ObjectIdentifier):
 pass


class SimpleSyntax(univ.Choice):
 componentType = namedtype.NamedTypes()
 namedtype.NamedType('number', univ.Integer()),
 namedtype.NamedType('string', univ.OctetString()),
 namedtype.NamedType('object', univ.ObjectIdentifier()),
 namedtype.NamedType('empty', univ.Null())
# BRACKET_SURGEON: disabled
# )


class IpAddress(univ.OctetString):
 tagSet = univ.OctetString.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueSizeConstraint()
 4, 4
# BRACKET_SURGEON: disabled
# )


class NetworkAddress(univ.Choice):
 componentType = namedtype.NamedTypes()
 namedtype.NamedType('internet', IpAddress())
# BRACKET_SURGEON: disabled
# )


class Counter(univ.Integer):
 tagSet = univ.Integer.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 1)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 0, 4294967295
# BRACKET_SURGEON: disabled
# )


class Gauge(univ.Integer):
 tagSet = univ.Integer.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 2)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 0, 4294967295
# BRACKET_SURGEON: disabled
# )


class TimeTicks(univ.Integer):
 tagSet = univ.Integer.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 3)
# BRACKET_SURGEON: disabled
# )
 subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint()
 0, 4294967295
# BRACKET_SURGEON: disabled
# )


class Opaque(univ.OctetString):
 tagSet = univ.OctetString.tagSet.tagImplicitly()
 tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 4)
# BRACKET_SURGEON: disabled
# )


class ApplicationSyntax(univ.Choice):
 componentType = namedtype.NamedTypes()
 namedtype.NamedType('address', NetworkAddress()),
 namedtype.NamedType('counter', Counter()),
 namedtype.NamedType('gauge', Gauge()),
 namedtype.NamedType('ticks', TimeTicks()),
 namedtype.NamedType('arbitrary', Opaque())
# BRACKET_SURGEON: disabled
# )


class ObjectSyntax(univ.Choice):
 componentType = namedtype.NamedTypes()
 namedtype.NamedType('simple', SimpleSyntax()),
 namedtype.NamedType('application-wide', ApplicationSyntax())
# BRACKET_SURGEON: disabled
# )