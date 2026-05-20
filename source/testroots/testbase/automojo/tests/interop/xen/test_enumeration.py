"""
    .. module:: test_enumeration
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Read-only enumeration tests for the Pool, Hosts, Networks,
        Sr and Templates api-groups.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


import pytest

from automojo.errors.exceptions import SemanticError

from automojo.interop.xen.model.xenhost import XenHost
from automojo.interop.xen.model.xennetwork import XenNetwork
from automojo.interop.xen.model.xenpool import XenPool
from automojo.interop.xen.model.xenpif import XenPif
from automojo.interop.xen.model.xenstoragerepository import (
    XenStorageRepository
)
from automojo.interop.xen.model.xenvmtemplate import XenVmTemplate


def test_pool_get_returns_typed_record(client, fast_aspects) -> None:
    """
        Pool.get returns a single typed XenPool record.
    """
    pool = client.Pool.get(aspects=fast_aspects)
    assert isinstance(pool, XenPool)
    assert pool.uuid == "pool-uuid-1"
    assert pool.name_label == "homelab-pool"
    return


def test_pool_get_raises_when_no_pool(client, transport, fast_aspects) -> None:
    """
        Pool.get raises SemanticError when no pool is present.
    """
    transport.pools.clear()
    with pytest.raises(SemanticError):
        client.Pool.get(aspects=fast_aspects)
    return


def test_hosts_list_returns_typed_records(client, fast_aspects) -> None:
    """
        Hosts.list returns typed XenHost records keyed by uuid.
    """
    hosts = client.Hosts.list(aspects=fast_aspects)
    assert len(hosts) == 1
    host = hosts[0]
    assert isinstance(host, XenHost)
    assert host.uuid == "host-uuid-1"
    assert host.address == "10.0.0.10"
    assert host.enabled is True
    return


def test_networks_list_returns_typed_records(client, fast_aspects) -> None:
    """
        Networks.list returns typed XenNetwork records.
    """
    networks = client.Networks.list(aspects=fast_aspects)
    assert len(networks) == 1
    net = networks[0]
    assert isinstance(net, XenNetwork)
    assert net.bridge == "xenbr0"
    assert net.mtu == 1500
    return


def test_networks_get_by_name_label_matches(client, fast_aspects) -> None:
    """
        Networks.get_by_name_label filters by exact name_label.
    """
    label = "Pool-wide network associated with eth0"
    matched = client.Networks.get_by_name_label(name_label=label,
                                                aspects=fast_aspects)
    assert len(matched) == 1
    assert matched[0].name_label == label

    none_matched = client.Networks.get_by_name_label(name_label="absent",
                                                     aspects=fast_aspects)
    assert len(none_matched) == 0
    return


def test_networks_list_pifs_filters_by_host(client, fast_aspects) -> None:
    """
        Networks.list_pifs resolves host/network refs and filters by host.
    """
    # The PIF references host-uuid-1; resolving its ref requires the host
    # record to have been enumerated first so the resolver knows the pair.
    client.Hosts.list(aspects=fast_aspects)
    client.Networks.list(aspects=fast_aspects)

    pifs = client.Networks.list_pifs(host_uuid="host-uuid-1",
                                     aspects=fast_aspects)
    assert len(pifs) == 1
    pif = pifs[0]
    assert isinstance(pif, XenPif)
    assert pif.device == "eth0"
    assert pif.host_uuid == "host-uuid-1"
    assert pif.network_uuid == "net-uuid-1"
    assert pif.management is True
    return


def test_networks_list_pifs_excludes_other_hosts(client,
                                                  fast_aspects) -> None:
    """
        Networks.list_pifs returns nothing for an unrelated host uuid.
    """
    client.Hosts.list(aspects=fast_aspects)
    pifs = client.Networks.list_pifs(host_uuid="host-uuid-other",
                                     aspects=fast_aspects)
    assert len(pifs) == 0
    return


def test_sr_list_returns_typed_records(client, fast_aspects) -> None:
    """
        Sr.list returns typed XenStorageRepository records.
    """
    srs = client.Sr.list(aspects=fast_aspects)
    assert len(srs) == 1
    sr = srs[0]
    assert isinstance(sr, XenStorageRepository)
    assert sr.type == "ext"
    assert sr.physical_size == 1099511627776
    assert sr.free == 1099511627776 - 107374182400
    return


def test_templates_list_returns_only_templates(client, fast_aspects) -> None:
    """
        Templates.list returns only VM records flagged is_a_template.
    """
    templates = client.Templates.list(aspects=fast_aspects)
    assert len(templates) == 1
    tmpl = templates[0]
    assert isinstance(tmpl, XenVmTemplate)
    assert tmpl.uuid == "tmpl-uuid-1"
    return
