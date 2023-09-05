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


class IsCompanyAdministrator(permissions.BasePermission):
    """Allow company admin of a PM to edit or read it."""

    def has_object_permission(self, request, view, obj):
        """If Administrator and PM in the same company."""
        if not request.user.groups.filter(name="Administrator").exists():
            return False

        # If obj is a company and administrator is in that company
        # Or if obj is a PM/SCTR, then admin can access it
        # if belongs to the same company
        return obj == request.user.company or obj.company == request.user.company


class IsSCTROwner(permissions.BasePermission):
    """Object-level permission to only allow PM(Admin) edit or read it."""

    def has_object_permission(self, request, view, obj):
        """If user's company is the same as SCTR company."""
        return obj.company == request.user.company


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


class IsComponentOwner(permissions.BasePermission):
    """Object permissions to update component."""

    def has_object_permission(self, request, view, obj):
        """Allow self edit for account owner."""
        return request.user.company == obj.parent_sctr.company
