# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains DRF permission classes."""
from rest_framework import permissions


SAFE_METHODS = ["GET", "OPTIONS", "HEAD"]


class ReadOnly(permissions.BasePermission):
    """Allows to use SAFE METHODS."""

    def has_permission(self, request, view):
        """Allows to access content if method is considered as safe."""
        if request.method in SAFE_METHODS:
            return True
        return False


class IsBoss(permissions.BasePermission):
    """Allow boss of an object to edit or read it."""

    def has_object_permission(self, request, view, obj):
        """If Administrator is a PM's boss."""
        if not obj.boss:
            return False
        return obj.boss == request.user


class IsProductOwner(permissions.BasePermission):
    """Object-level permission to only allow PM edit or read it."""

    def has_object_permission(self, request, view, obj):
        """If user is a product administrator.

        Or a PM, which boss is administrator of product.
        """
        if request.user.groups.filter(name="Administrator").exists():
            return obj.owner == request.user
        elif request.user.groups.filter(name="PM").exists():
            return obj.owner == request.user.boss
        return False


class IsAccountOwner(permissions.BasePermission):
    """Object-level permission to only allow owner for editting."""

    def has_object_permission(self, request, view, obj):
        """Allow self edit for account owner."""
        return request.user == obj


class IsAdministrator(permissions.BasePermission):
    """Object-level permission to only allow administrators for access."""

    def has_permission(self, request, view):
        """If Administrator."""
        return request.user.groups.filter(name="Administrator").exists()


class IsPM(permissions.BasePermission):
    """Object-level permission to only allow PMs for access."""

    def has_permission(self, request, view):
        """If PM."""
        return request.user.groups.filter(name="PM").exists()
