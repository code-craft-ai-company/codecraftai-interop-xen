"""
    .. module:: templatesgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: TemplatesGroup — XAPI VM template enumeration.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from typing import List

from automojo.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
from automojo.interop.xen.apigroups.basegroup import BaseGroup
from automojo.interop.xen.model.xenvmtemplate import XenVmTemplate


class TemplatesGroup(BaseGroup):
    """
        XAPI VM-template enumeration.

        Templates are VM objects whose ``is_a_template`` field is true; this
        group filters them out of the ``VM.get_all_records`` result.
    """

    def list(self, *, aspects: AspectsXapi = DEFAULT_XEN_ASPECTS
             ) -> List[XenVmTemplate]:
        """
            Enumerate VM templates as :class:`XenVmTemplate` records.

            :param aspects: Behaviour controls.

            :returns: A list of :class:`XenVmTemplate` records.
        """
        records = self._call(method_path="VM.get_all_records", args=[],
                              aspects=aspects)
        out: List[XenVmTemplate] = []
        if isinstance(records, dict):
            for opaque_ref, record in records.items():
                self._record_ref(opaque_ref=opaque_ref, record=record)
                if bool(record.get("is_a_template", False)) is not True:
                    continue
                other_config = record.get("other_config", {})
                os_hint = ""
                if isinstance(other_config, dict):
                    os_hint = other_config.get("install-distro", "")
                out.append(XenVmTemplate(
                    uuid=record.get("uuid", ""),
                    name_label=record.get("name_label", ""),
                    name_description=record.get("name_description", ""),
                    os_version_hint=os_hint,
                ))
        rtnval = out
        return rtnval
