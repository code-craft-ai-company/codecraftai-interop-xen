"""
    .. module:: test_refresolver
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Property-based and unit tests for the RefResolver
        opaque-ref/uuid translation cache.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import pytest

from hypothesis import given, strategies as st

from automojo.errors.exceptions import SemanticError

from automojo.interop.xen.refs.refresolver import RefResolver


def test_remember_then_translate_both_directions() -> None:
    """
        A remembered pair translates in both directions.
    """
    resolver = RefResolver()
    resolver.remember(opaque_ref="OpaqueRef:abc", uuid="uuid-abc")
    assert resolver.uuid_for(opaque_ref="OpaqueRef:abc") == "uuid-abc"
    assert resolver.ref_for(uuid="uuid-abc") == "OpaqueRef:abc"
    return


def test_unknown_ref_raises_semantic_error() -> None:
    """
        Resolving an unknown opaque ref raises SemanticError.
    """
    resolver = RefResolver()
    with pytest.raises(SemanticError):
        resolver.uuid_for(opaque_ref="OpaqueRef:missing")
    return


def test_unknown_uuid_raises_semantic_error() -> None:
    """
        Resolving an unknown uuid raises SemanticError.
    """
    resolver = RefResolver()
    with pytest.raises(SemanticError):
        resolver.ref_for(uuid="uuid-missing")
    return


def test_maybe_uuid_for_returns_none_when_unknown() -> None:
    """
        maybe_uuid_for returns None for an unknown ref rather than raising.
    """
    resolver = RefResolver()
    assert resolver.maybe_uuid_for(opaque_ref="OpaqueRef:missing") is None
    return


def test_forget_uuid_drops_both_directions() -> None:
    """
        forget_uuid removes a pair so both directions become unknown again.
    """
    resolver = RefResolver()
    resolver.remember(opaque_ref="OpaqueRef:abc", uuid="uuid-abc")
    resolver.forget_uuid(uuid="uuid-abc")
    assert resolver.maybe_uuid_for(opaque_ref="OpaqueRef:abc") is None
    with pytest.raises(SemanticError):
        resolver.ref_for(uuid="uuid-abc")
    return


def test_forget_unknown_uuid_is_noop() -> None:
    """
        forget_uuid on an unknown uuid is a harmless no-op.
    """
    resolver = RefResolver()
    resolver.forget_uuid(uuid="never-seen")
    return


_REF_TEXT = st.text(min_size=1, max_size=20)


@given(opaque_ref=_REF_TEXT, uuid=_REF_TEXT)
def test_property_round_trip_is_total_for_remembered_pairs(
        opaque_ref, uuid) -> None:
    """
        For any remembered (opaque_ref, uuid) pair, translation in both
        directions round-trips back to the original values.
    """
    resolver = RefResolver()
    resolver.remember(opaque_ref=opaque_ref, uuid=uuid)
    assert resolver.uuid_for(opaque_ref=opaque_ref) == uuid
    assert resolver.ref_for(uuid=uuid) == opaque_ref
    # ref -> uuid -> ref returns the original ref.
    round_tripped = resolver.ref_for(
        uuid=resolver.uuid_for(opaque_ref=opaque_ref))
    assert round_tripped == opaque_ref
    return


@given(pairs=st.dictionaries(keys=_REF_TEXT, values=_REF_TEXT,
                             min_size=1, max_size=8))
def test_property_forget_leaves_other_pairs_intact(pairs) -> None:
    """
        Forgetting one uuid never disturbs the translation of any other
        remembered pair.
    """
    resolver = RefResolver()
    # Each uuid value maps to one opaque_ref key; build a uuid -> ref view
    # so forgetting one uuid is unambiguous.
    uuid_to_ref = {}
    for opaque_ref, uuid in pairs.items():
        resolver.remember(opaque_ref=opaque_ref, uuid=uuid)
        uuid_to_ref[uuid] = opaque_ref

    victim_uuid = next(iter(uuid_to_ref.keys()))
    resolver.forget_uuid(uuid=victim_uuid)

    for uuid, opaque_ref in uuid_to_ref.items():
        if uuid == victim_uuid:
            continue
        assert resolver.ref_for(uuid=uuid) == opaque_ref
    return
