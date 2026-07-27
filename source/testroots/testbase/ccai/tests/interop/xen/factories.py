"""
    .. module:: factories
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Shared fixtures for the Xen interop client tests.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from collections.abc import Generator

from ccai import testbase

from ccai.interop.xen.aspectsxen import AspectsXapi
from ccai.interop.xen.session.xensessioncredential import (
    XenSessionCredential
)
from ccai.interop.xen.xenclient import XenClient

from ccai.tests.interop.xen._mockxapi import MockXapiTransport

@testbase.register.resource_factory()
def create_xen_credential(constraints=None) -> Generator[XenSessionCredential, None, None]:
    """
        Return a deterministic XenSessionCredential.
    """
    rtnval = XenSessionCredential(
        master_url="https://xen-master.lab", username="root",
        password="secret-value",
    )
    yield rtnval


@testbase.register.resource_factory()
def create_xen_fast_aspects(constraints=None) -> Generator[AspectsXapi, None, None]:
    """
        Return AspectsXapi with a tight poll loop for tests.
    """
    rtnval = AspectsXapi(completion_interval=0.001, completion_timeout=5.0,
                         max_attempts=3)
    yield rtnval


@testbase.register.resource_factory()
def create_xen_transport(constraints=None) -> Generator[MockXapiTransport, None, None]:
    """
        Return a fresh MockXapiTransport.
    """
    rtnval = MockXapiTransport()
    yield rtnval


@testbase.register.resource_factory()
def create_xen_client(credential, transport, fast_aspects, constraints=None) -> Generator[XenClient, None, None]:
    """
        Return a XenClient wired to the mock transport.
    """
    rtnval = XenClient(
        credential=credential,
        transport_factory=lambda *, master_url: transport,
        aspects=fast_aspects,
    )
    yield rtnval
