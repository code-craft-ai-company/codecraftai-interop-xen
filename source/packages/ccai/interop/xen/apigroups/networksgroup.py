"""
    .. module:: networksgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: NetworksGroup — XAPI network and PIF enumeration.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


from typing import List

from ccai.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from ccai.interop.xen.apigroups.basegroup import BaseGroup
from ccai.interop.xen.model.xennetwork import XenNetwork
from ccai.interop.xen.model.xenpif import XenPif


class NetworksGroup(BaseGroup):
    """
        XAPI ``network`` and ``PIF`` object-class operations.
    """

    def list(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
             ) -> List[XenNetwork]:
        """
            Enumerate networks as :class:`XenNetwork` records.

            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenNetwork` records.
        """
        records = self._call(method_path="network.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenNetwork] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                out.append(XenNetwork(
                    uuid=record.get("uuid", ""),
                    name_label=record.get("name_label", ""),
                    name_description=record.get("name_description", ""),
                    bridge=record.get("bridge", ""),
                    mtu=int(record.get("MTU", record.get("mtu", 1500))),
                ))
        rtnval = out
        return rtnval

    def get_by_name_label(self, *, name_label: str,
                          aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                          ) -> List[XenNetwork]:
        """
            Return networks whose ``name_label`` matches.

            :param name_label: The network name_label to match.
            :param aspects: Behaviour controls.

            :returns: A list of matching :class:`XenNetwork` records.
        """
        networks = self.list(aspects=aspects)
        matched = [net for net in networks if net.name_label == name_label]
        rtnval = matched
        return rtnval

    def list_pifs(self, *, host_uuid: str,
                  aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
                  ) -> List[XenPif]:
        """
            Enumerate PIFs for a host as :class:`XenPif` records.

            :param host_uuid: The uuid of the host to filter PIFs by.
            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenPif` records for the host.
        """
        records = self._call(method_path="PIF.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenPif] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                host_ref = record.get("host", None)
                resolved_host = None
                if host_ref is not None:
                    resolved_host = self._resolver.maybe_uuid_for(
                        opaque_ref=host_ref)
                network_ref = record.get("network", None)
                resolved_network = None
                if network_ref is not None:
                    resolved_network = self._resolver.maybe_uuid_for(
                        opaque_ref=network_ref)
                if resolved_host is not None and resolved_host != host_uuid:
                    continue
                out.append(XenPif(
                    uuid=record.get("uuid", ""),
                    device=record.get("device", ""),
                    host_uuid=resolved_host if resolved_host is not None
                    else "",
                    network_uuid=resolved_network if resolved_network
                    is not None else "",
                    management=bool(record.get("management", False)),
                ))
        rtnval = out
        return rtnval
