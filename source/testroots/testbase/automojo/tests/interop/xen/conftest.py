"""
    .. module:: conftest
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Shared fixtures for the Xen interop client tests.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import pytest

from automojo.interop.xen.aspectsxen import AspectsXapi
from automojo.interop.xen.session.xensessioncredential import (
    XenSessionCredential
)
from automojo.interop.xen.xenclient import XenClient

from ._mockxapi import MockXapiTransport


@pytest.fixture
def credential() -> XenSessionCredential:
    """
        Return a deterministic XenSessionCredential.
    """
    rtnval = XenSessionCredential(
        master_url="https://xen-master.lab", username="root",
        password="secret-value",
    )
    return rtnval


@pytest.fixture
def fast_aspects() -> AspectsXapi:
    """
        Return AspectsXapi with a tight poll loop for tests.
    """
    rtnval = AspectsXapi(completion_interval=0.001, completion_timeout=5.0,
                         max_attempts=3)
    return rtnval


@pytest.fixture
def transport() -> MockXapiTransport:
    """
        Return a fresh MockXapiTransport.
    """
    rtnval = MockXapiTransport()
    return rtnval


@pytest.fixture
def client(credential, transport, fast_aspects) -> XenClient:
    """
        Return a XenClient wired to the mock transport.
    """
    rtnval = XenClient(
        credential=credential,
        transport_factory=lambda *, master_url: transport,
        aspects=fast_aspects,
    )
    return rtnval
