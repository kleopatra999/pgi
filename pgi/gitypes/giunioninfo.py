# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from glib import gint, gboolean, gchar_p, gsize
from gibaseinfo import GIInfoType
from gifieldinfo import GIFieldInfoPtr
from gicallableinfo import GIFunctionInfoPtr
from gitypeinfo import GITypeInfoPtr
from giconstantinfo import GIConstantInfoPtr
from giregisteredtypeinfo import GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_union_info(base_info, _type=GIInfoType.UNION):
    return base_info.get_type().value == _type


class GIUnionInfo(GIRegisteredTypeInfo):
    pass


class GIUnionInfoPtr(GIRegisteredTypeInfoPtr):
    _type_ = GIUnionInfo

_methods = [
    ("get_n_fields", gint, [GIUnionInfoPtr]),
    ("get_field", GIFieldInfoPtr, [GIUnionInfoPtr, gint]),
    ("get_n_methods", gint, [GIUnionInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIUnionInfoPtr, gint]),
    ("is_discriminated", gboolean, [GIUnionInfoPtr]),
    ("get_discriminator_offset", gint, [GIUnionInfoPtr]),
    ("get_discriminator_type", GITypeInfoPtr, [GIUnionInfoPtr]),
    ("get_discriminator", GIConstantInfoPtr, [GIUnionInfoPtr, gint]),
    ("find_method", GIFunctionInfoPtr, [GIUnionInfoPtr, gchar_p]),
    ("get_size", gsize, [GIUnionInfoPtr]),
    ("get_alignment", gsize, [GIUnionInfoPtr]),
]

wrap_class(_gir, GIUnionInfo, GIUnionInfoPtr, "g_union_info_", _methods)

__all__ = ["GIUnionInfo", "GIUnionInfoPtr", "gi_is_union_info"]
