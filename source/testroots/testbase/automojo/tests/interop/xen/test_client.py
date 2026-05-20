"""
    .. module:: test_client
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Construction and lazy api-group property tests for
        :class:`XenClient`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from automojo.interop.xen.apigroups.hostsgroup import HostsGroup
from automojo.interop.xen.apigroups.networksgroup import NetworksGroup
from automojo.interop.xen.apigroups.poolgroup import PoolGroup
from automojo.interop.xen.apigroups.snapshotsgroup import SnapshotsGroup
from automojo.interop.xen.apigroups.srgroup import SrGroup
from automojo.interop.xen.apigroups.tasksgroup import TasksGroup
from automojo.interop.xen.apigroups.templatesgroup import TemplatesGroup
from automojo.interop.xen.apigroups.vbdsgroup import VbdsGroup
from automojo.interop.xen.apigroups.vdigroup import VdiGroup
from automojo.interop.xen.apigroups.vifsgroup import VifsGroup
from automojo.interop.xen.apigroups.vmsgroup import VmsGroup
from automojo.interop.xen.refs.refresolver import RefResolver
from automojo.interop.xen.session.xensessionmanager import XenSessionManager


def test_client_exposes_session_manager_and_resolver(client) -> None:
    """
        The client exposes its owning session manager and shared resolver.
    """
    assert isinstance(client.session_manager, XenSessionManager)
    assert isinstance(client.resolver, RefResolver)
    return


def test_client_group_properties_have_expected_types(client) -> None:
    """
        Every api-group property returns the correct group type.
    """
    assert isinstance(client.Pool, PoolGroup)
    assert isinstance(client.Hosts, HostsGroup)
    assert isinstance(client.Networks, NetworksGroup)
    assert isinstance(client.Sr, SrGroup)
    assert isinstance(client.Vdi, VdiGroup)
    assert isinstance(client.Templates, TemplatesGroup)
    assert isinstance(client.Vms, VmsGroup)
    assert isinstance(client.Vbds, VbdsGroup)
    assert isinstance(client.Vifs, VifsGroup)
    assert isinstance(client.Snapshots, SnapshotsGroup)
    assert isinstance(client.Tasks, TasksGroup)
    return


def test_client_groups_are_lazily_constructed_and_cached(client) -> None:
    """
        Each api-group property is constructed once and cached thereafter.
    """
    first_pool = client.Pool
    second_pool = client.Pool
    assert first_pool is second_pool

    first_vms = client.Vms
    second_vms = client.Vms
    assert first_vms is second_vms
    return


def test_client_groups_share_one_resolver(client) -> None:
    """
        Every api-group shares the client's single RefResolver instance.
    """
    resolver = client.resolver
    assert client.Pool._resolver is resolver
    assert client.Vms._resolver is resolver
    assert client.Vdi._resolver is resolver
    return


def test_client_groups_share_one_session_manager(client) -> None:
    """
        Every api-group shares the client's single XenSessionManager.
    """
    manager = client.session_manager
    assert client.Hosts._session_manager is manager
    assert client.Networks._session_manager is manager
    return
