"""
    .. module:: refresolver
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: RefResolver — bidirectional cache translating XAPI opaque
        object references to/from stable uuids so opaque refs never leak
        through the public client surface.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


import os

from typing import Dict, Optional

from ccai.errors.exceptions import SemanticError


class RefResolver:
    """
        Bidirectional translation cache between XAPI opaque refs and uuids.

        XAPI returns opaque refs (``OpaqueRef:...``) from every call; a uuid
        is the only stable identity.  This resolver records each
        ``(opaque_ref, uuid)`` pairing it observes so subsequent calls can
        translate in either direction without an extra round-trip.

        Translation is total only for pairs the resolver has been told
        about; resolving an unknown value raises :class:`SemanticError` so a
        leaked or stale reference is loud rather than silent.
    """

    def __init__(self) -> None:
        """
            Construct an empty RefResolver.
        """
        self._ref_to_uuid: Dict[str, str] = {}
        self._uuid_to_ref: Dict[str, str] = {}
        return

    def remember(self, *, opaque_ref: str, uuid: str) -> None:
        """
            Record an ``(opaque_ref, uuid)`` pairing.

            :param opaque_ref: The XAPI opaque reference string.
            :param uuid: The stable object uuid.
        """
        self._ref_to_uuid[opaque_ref] = uuid
        self._uuid_to_ref[uuid] = opaque_ref
        return

    def uuid_for(self, *, opaque_ref: str) -> str:
        """
            Translate an opaque ref to its uuid.

            :param opaque_ref: The XAPI opaque reference string.

            :returns: The stable object uuid.
            :raises: SemanticError
        """
        if opaque_ref not in self._ref_to_uuid:
            err_msg_lines = ["RefResolver cannot resolve an unknown opaque "
                             "reference."]
            err_msg_lines.append("OPAQUE_REF: {!r}".format(opaque_ref))
            err_msg = os.linesep.join(err_msg_lines)
            raise SemanticError(err_msg)
        rtnval = self._ref_to_uuid[opaque_ref]
        return rtnval

    def ref_for(self, *, uuid: str) -> str:
        """
            Translate a uuid to its opaque ref.

            :param uuid: The stable object uuid.

            :returns: The XAPI opaque reference string.
            :raises: SemanticError
        """
        if uuid not in self._uuid_to_ref:
            err_msg_lines = ["RefResolver cannot resolve an unknown uuid."]
            err_msg_lines.append("UUID: {!r}".format(uuid))
            err_msg = os.linesep.join(err_msg_lines)
            raise SemanticError(err_msg)
        rtnval = self._uuid_to_ref[uuid]
        return rtnval

    def maybe_uuid_for(self, *, opaque_ref: str) -> Optional[str]:
        """
            Translate an opaque ref to a uuid, returning None when unknown.

            :param opaque_ref: The XAPI opaque reference string.

            :returns: The uuid, or None when the ref is not cached.
        """
        rtnval = self._ref_to_uuid.get(opaque_ref, None)
        return rtnval

    def maybe_ref_for(self, *, uuid: str) -> Optional[str]:
        """
            Translate a uuid to an opaque ref, returning None when unknown.

            Unlike :meth:`ref_for`, this lookup is total: it never raises a
            :class:`SemanticError`.  Idempotent delete/detach operations use
            it so an already-forgotten uuid resolves to a clean no-op rather
            than a loud failure.

            :param uuid: The stable object uuid.

            :returns: The opaque ref, or None when the uuid is not cached.
        """
        rtnval = self._uuid_to_ref.get(uuid, None)
        return rtnval

    def forget_uuid(self, *, uuid: str) -> None:
        """
            Drop a uuid (and its opaque ref) from the cache.

            Idempotent: forgetting an unknown uuid is a no-op.

            :param uuid: The object uuid to drop.
        """
        opaque_ref = self._uuid_to_ref.pop(uuid, None)
        if opaque_ref is not None:
            self._ref_to_uuid.pop(opaque_ref, None)
        return
