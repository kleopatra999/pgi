# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from glib import *
from ctypes import *
from _util import load, wrap_class

_gobject = load("gobject-2.0")


class GSignalFlags(Flags):
    RUN_FIRST = 1 << 0
    RUN_LAST = 1 << 1
    RUN_CLEANUP = 1 << 2
    NO_RECURSE = 1 << 3
    DETAILED = 1 << 4
    ACTION = 1 << 5
    NO_HOOKS = 1 << 6
    MUST_COLLECT = 1 << 7

g_type_init = _gobject.g_type_init
g_type_init.argtypes = []
g_type_init.resttype = None


class GTypeFundamentalFlags(Flags):
    CLASSED = 1 << 0
    INSTANTIATABLE = 1 << 1
    DERIVABLE = 1 << 2
    DEEP_DERIVABLE = 1 << 3


class GTypeFlags(Flags):
    ABSTRACT = 1 << 4
    VALUE_ABSTRACT = 1 << 5


class GType(guint):
    def __repr__(self):
        return "<GType %r>" % repr(self.value)

_methods = [
    ("name", gchar_p, [GType]),
    ("depth", guint, [GType]),
    ("parent", GType, [GType]),
    ("from_name", GType, [gchar_p]),
    ("check_is_value_type", gboolean, [GType]),
    ("test_flags", gboolean, [GType, GTypeFlags]),
    ("value_table_peek", gpointer, [GType]),  # returns GTypeValueTable
    ("is_a", gboolean, [GType, GType]),
    ("fundamental", GType, [GType]),
    ("children", POINTER(GType), [GType, POINTER(guint)]),
    ("interfaces", POINTER(GType), [GType, POINTER(guint)]),
    ("class_peek", gpointer, [GType]),
]

wrap_class(_gobject, GType, GType, "g_type_", _methods)


_methods = [
    ("newv", gpointer, [GType, guint]),
    ("new", gpointer, [GType, guint]),
    ("unref", None, [gpointer]),
    ("ref_sink", gpointer, [gpointer]),
    ("is_floating", gboolean, [gpointer]),
]

for (name, ret, args) in _methods:
    h = getattr(_gobject, "g_object_" + name)
    h.argtypes = args
    h.resttype = ret
    globals()[name] = h

free = _gobject.g_free
free.argtypes = [gpointer]
free.resttype = None



class GTypeClass(Structure):
    _fields_ = [
        ("g_type", GType),
    ]


class GTypeClassPtr(POINTER(GTypeClass)):
    _type_ = GTypeClass


class GTypeInstance(Structure):
    _fields_ = [
        ("g_class", GTypeClassPtr),
    ]


class GTypeInstancePtr(POINTER(GTypeInstance)):
    _type_ = GTypeInstance


class GObject(Structure):
    _fields_ = [
        ("g_type_instance", GTypeInstance),
        ("ref_count", guint32),
    ]

GObjectPtr = POINTER(GObject)


# GValue


class GValue(Structure):
    pass


class GValuePtr(POINTER(GValue)):
    _type_ = GValue

GValueTransform = CFUNCTYPE(None, GValuePtr, GValuePtr)

_methods = [
    ("init", GValuePtr, [GValuePtr, GType]),
    ("copy", None, [GValuePtr, GValuePtr]),
    ("reset", GValuePtr, [GValuePtr]),
    ("unset", None, [GValuePtr]),
    ("set_instance", None, [GValuePtr, gpointer]),
    ("fits_pointer", gboolean, [GValuePtr]),
    ("peek_pointer", gpointer, [GValuePtr]),
    ("type_compatible", gboolean, [GType, GType]),
    ("type_transformable", gboolean, [GType, GType]),
    ("transform", gboolean, [GValuePtr, GValuePtr]),
    ("register_transform_func", None, [GType, GType, GValueTransform]),
    ("set_string", None, [GValuePtr, gchar_p]),
    ("set_boxed", None, [GValuePtr, gpointer]),
    ("set_pointer", None, [GValuePtr, gpointer]),
    ("set_object", None, [GValuePtr, gpointer]),
    ("set_boolean", None, [GValuePtr, gboolean]),
    ("set_char", None, [GValuePtr, gchar]),
    ("set_uchar", None, [GValuePtr, guchar]),
    ("set_int", None, [GValuePtr, gint]),
    ("set_uint", None, [GValuePtr, guint]),
    ("set_long", None, [GValuePtr, glong]),
    ("set_ulong", None, [GValuePtr, gulong]),
    ("set_int64", None, [GValuePtr, gint64]),
    ("set_uint64", None, [GValuePtr, guint64]),
    ("set_float", None, [GValuePtr, gfloat]),
    ("set_double", None, [GValuePtr, gdouble]),
    ("set_enum", None, [GValuePtr, gint]),
    ("set_flags", None, [GValuePtr, guint]),
]

wrap_class(_gobject, GValue, GValuePtr, "g_value_", _methods)


class GParamFlags(Flags):
    READABLE = 1 << 0
    WRITABLE = 1 << 1
    CONSTRUCT = 1 << 2
    CONSTRUCT_ONLY = 1 << 3
    LAX_VALIDATION = 1 << 4
    STATIC_NAME = 1 << 5
    STATIC_NICK = 1 << 6
    STATIC_BLURB = 1 << 7
    DEPRECATED = 1 << 31


class GParamSpec(Structure):
    _fields_ = [
        ("g_type_instance", GTypeInstance),
        ("name", gchar_p),
        ("flags", GParamFlags),
        ("value_type", GType),
        ("owner_type", GType),
    ]


class GParamSpecPtr(POINTER(GParamSpec)):
    _type_ = GParamSpec


_methods = [
    ("get_name", gchar_p, [GParamSpecPtr]),
    ("get_nick", gchar_p, [GParamSpecPtr]),
    ("get_blurb", gchar_p, [GParamSpecPtr]),
]

wrap_class(_gobject, GParamSpec, GParamSpecPtr, "g_param_spec_", _methods)


class GObjectClass(Structure):
    pass


class GObjectClassPtr(POINTER(GObjectClass)):
    _type_ = GObjectClass

_methods = [
    ("find_property", GParamSpecPtr, [GObjectClassPtr, gchar_p]),
]

wrap_class(_gobject, GObjectClass, GObjectClassPtr, "g_object_class_", _methods)


def G_TYPE_FROM_INSTANCE(instance):
    return instance.g_class.contents.g_type


__all__ = ["GType", "g_type_init", "GParamFlags", "GValue", "GValuePtr",
           "GValueTransform", "GSignalFlags", "GTypeFlags",
           "GTypeFundamentalFlags", "GObjectPtr", "GParamSpec",
           "GParamSpecPtr", "GObjectClassPtr", "G_TYPE_FROM_INSTANCE"]
