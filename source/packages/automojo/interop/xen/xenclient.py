"""
    .. module:: xenclient
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Provides :class:`XenClient`, the typed client over the XAPI
        XML-RPC interface of an XCP-ng / XenServer pool master.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from typing import Any, Callable, Optional

from automojo.interop.xen.aspectsxen import AspectsXapi, DEFAULT_XEN_ASPECTS
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
from automojo.interop.xen.model.xentaskhandle import XenTaskHandle
from automojo.interop.xen.refs.refresolver import RefResolver
from automojo.interop.xen.session.xensessioncredential import (
    XenSessionCredential
)
from automojo.interop.xen.session.xensessionmanager import XenSessionManager


class XenClient:
    """
        Typed client over the XAPI XML-RPC interface of an XCP-ng /
        XenServer pool master.

        XAPI rides over HTTPS but serialises as XML-RPC — not REST — so this
        client does not extend ``RestClientBase``.  The single-transport rule
        still holds: this client speaks XAPI XML-RPC and nothing else.

        Opaque XAPI object references never leak through the public surface;
        every group resolves refs to stable uuids through a shared
        :class:`RefResolver`.  Async XAPI operations return a
        :class:`XenTaskHandle` whose poll loop is driven by
        :class:`AspectsXapi`.

        The API surface is exposed through lazily-constructed group
        properties: ``Pool``, ``Hosts``, ``Networks``, ``Sr``, ``Vdi``,
        ``Templates``, ``Vms``, ``Vbds``, ``Vifs``, ``Snapshots`` and
        ``Tasks``.
    """

    def __init__(self, *, credential: XenSessionCredential,
                 transport_factory: Optional[Callable[..., Any]] = None,
                 aspects: AspectsXapi = DEFAULT_XEN_ASPECTS) -> None:
        """
            Construct a XenClient.

            :param credential: The :class:`XenSessionCredential` carrying the
                               pool-master URL, username and password.
            :param transport_factory: Optional callable building the XML-RPC
                                      transport.  Tests inject a mock
                                      transport so no real host is contacted.
            :param aspects: The default :class:`AspectsXapi` instance.
        """
        self._credential: XenSessionCredential = credential
        self._aspects: AspectsXapi = aspects
        self._session_manager: XenSessionManager = XenSessionManager(
            credential=credential, transport_factory=transport_factory)
        self._resolver: RefResolver = RefResolver()

        self._pool: Optional[PoolGroup] = None
        self._hosts: Optional[HostsGroup] = None
        self._networks: Optional[NetworksGroup] = None
        self._sr: Optional[SrGroup] = None
        self._vdi: Optional[VdiGroup] = None
        self._templates: Optional[TemplatesGroup] = None
        self._vms: Optional[VmsGroup] = None
        self._vbds: Optional[VbdsGroup] = None
        self._vifs: Optional[VifsGroup] = None
        self._snapshots: Optional[SnapshotsGroup] = None
        self._tasks: Optional[TasksGroup] = None
        return

    @property
    def session_manager(self) -> XenSessionManager:
        """
            Return the owning :class:`XenSessionManager`.

            :returns: The session manager.
        """
        rtnval = self._session_manager
        return rtnval

    @property
    def resolver(self) -> RefResolver:
        """
            Return the shared :class:`RefResolver`.

            :returns: The ref resolver.
        """
        rtnval = self._resolver
        return rtnval

    def login(self, *, aspects: Optional[AspectsXapi] = None) -> str:
        """
            Log in to the pool master and cache the session.

            :param aspects: Behaviour controls; the client default is used
                            when omitted.

            :returns: The session reference string.
        """
        effective = aspects if aspects is not None else self._aspects
        rtnval = self._session_manager.login(aspects=effective)
        return rtnval

    def logout(self, *, aspects: Optional[AspectsXapi] = None) -> None:
        """
            Release the cached pool-master session.

            :param aspects: Behaviour controls; the client default is used
                            when omitted.
        """
        effective = aspects if aspects is not None else self._aspects
        self._session_manager.logout(aspects=effective)
        return

    def _make_task_handle(self, task_uuid: str) -> XenTaskHandle:
        """
            Build a :class:`XenTaskHandle` for an XAPI task uuid.

            :param task_uuid: The XAPI task uuid.

            :returns: A :class:`XenTaskHandle` bound to the Tasks group.
        """
        tasks_group = self.Tasks

        def _fetch(uuid: str):
            rtnval = tasks_group.get_status(task_uuid=uuid,
                                            aspects=self._aspects)
            return rtnval

        rtnval = XenTaskHandle(task_uuid=task_uuid, status_fetcher=_fetch)
        return rtnval

    @property
    def Pool(self) -> PoolGroup:
        """
            Return the lazily-constructed :class:`PoolGroup`.

            :returns: The PoolGroup.
        """
        if self._pool is None:
            self._pool = PoolGroup(session_manager=self._session_manager,
                                   resolver=self._resolver)
        rtnval = self._pool
        return rtnval

    @property
    def Hosts(self) -> HostsGroup:
        """
            Return the lazily-constructed :class:`HostsGroup`.

            :returns: The HostsGroup.
        """
        if self._hosts is None:
            self._hosts = HostsGroup(session_manager=self._session_manager,
                                     resolver=self._resolver)
        rtnval = self._hosts
        return rtnval

    @property
    def Networks(self) -> NetworksGroup:
        """
            Return the lazily-constructed :class:`NetworksGroup`.

            :returns: The NetworksGroup.
        """
        if self._networks is None:
            self._networks = NetworksGroup(
                session_manager=self._session_manager,
                resolver=self._resolver)
        rtnval = self._networks
        return rtnval

    @property
    def Sr(self) -> SrGroup:
        """
            Return the lazily-constructed :class:`SrGroup`.

            :returns: The SrGroup.
        """
        if self._sr is None:
            self._sr = SrGroup(session_manager=self._session_manager,
                               resolver=self._resolver)
        rtnval = self._sr
        return rtnval

    @property
    def Vdi(self) -> VdiGroup:
        """
            Return the lazily-constructed :class:`VdiGroup`.

            :returns: The VdiGroup.
        """
        if self._vdi is None:
            self._vdi = VdiGroup(session_manager=self._session_manager,
                                 resolver=self._resolver)
        rtnval = self._vdi
        return rtnval

    @property
    def Templates(self) -> TemplatesGroup:
        """
            Return the lazily-constructed :class:`TemplatesGroup`.

            :returns: The TemplatesGroup.
        """
        if self._templates is None:
            self._templates = TemplatesGroup(
                session_manager=self._session_manager,
                resolver=self._resolver)
        rtnval = self._templates
        return rtnval

    @property
    def Vms(self) -> VmsGroup:
        """
            Return the lazily-constructed :class:`VmsGroup`.

            :returns: The VmsGroup.
        """
        if self._vms is None:
            self._vms = VmsGroup(session_manager=self._session_manager,
                                 resolver=self._resolver,
                                 task_handle_factory=self._make_task_handle)
        rtnval = self._vms
        return rtnval

    @property
    def Vbds(self) -> VbdsGroup:
        """
            Return the lazily-constructed :class:`VbdsGroup`.

            :returns: The VbdsGroup.
        """
        if self._vbds is None:
            self._vbds = VbdsGroup(session_manager=self._session_manager,
                                   resolver=self._resolver)
        rtnval = self._vbds
        return rtnval

    @property
    def Vifs(self) -> VifsGroup:
        """
            Return the lazily-constructed :class:`VifsGroup`.

            :returns: The VifsGroup.
        """
        if self._vifs is None:
            self._vifs = VifsGroup(session_manager=self._session_manager,
                                   resolver=self._resolver)
        rtnval = self._vifs
        return rtnval

    @property
    def Snapshots(self) -> SnapshotsGroup:
        """
            Return the lazily-constructed :class:`SnapshotsGroup`.

            :returns: The SnapshotsGroup.
        """
        if self._snapshots is None:
            self._snapshots = SnapshotsGroup(
                session_manager=self._session_manager,
                resolver=self._resolver)
        rtnval = self._snapshots
        return rtnval

    @property
    def Tasks(self) -> TasksGroup:
        """
            Return the lazily-constructed :class:`TasksGroup`.

            :returns: The TasksGroup.
        """
        if self._tasks is None:
            self._tasks = TasksGroup(session_manager=self._session_manager,
                                     resolver=self._resolver)
        rtnval = self._tasks
        return rtnval
