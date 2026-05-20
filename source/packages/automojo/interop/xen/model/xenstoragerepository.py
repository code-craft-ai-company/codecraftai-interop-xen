"""
    .. module:: xenstoragerepository
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Typed record for an XAPI SR (storage repository) object.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from dataclasses import dataclass


@dataclass
class XenStorageRepository:
    """
        Typed record describing an XAPI storage repository.

        :param uuid: The SR uuid.
        :param name_label: The human-readable SR label.
        :param type: The SR backend type (lvmoiscsi, nfs, ext, zfs, ...).
        :param physical_size: The total SR capacity in bytes.
        :param physical_utilisation: The currently used capacity in bytes.
        :param shared: Whether the SR is shared across the pool.
    """
    uuid: str
    name_label: str
    type: str = ""
    physical_size: int = 0
    physical_utilisation: int = 0
    shared: bool = False

    @property
    def free(self) -> int:
        """
            Return the free capacity in bytes.

            :returns: The number of free bytes on the SR.
        """
        rtnval = self.physical_size - self.physical_utilisation
        return rtnval
