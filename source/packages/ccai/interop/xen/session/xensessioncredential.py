"""
    .. module:: xensessioncredential
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Credential carrier for an XAPI pool-master session login.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


import os

from ccai.errors.exceptions import ConfigurationError


class XenSessionCredential:
    """
        Credential bundle for an XAPI pool-master session.

        Carries the pool-master URL plus the username and password used by
        ``session.login_with_password``.  Construction validates that every
        field is present so a misconfigured venue fails fast with a
        :class:`ConfigurationError` rather than at first XML-RPC call.
    """

    def __init__(self, *, master_url: str, username: str,
                 password: str) -> None:
        """
            Construct an XenSessionCredential.

            :param master_url: The pool-master XML-RPC URL (https://host).
            :param username: The XAPI account username.
            :param password: The XAPI account password.

            :raises: ConfigurationError
        """
        missing = []
        if master_url is None or len(master_url) == 0:
            missing.append("master_url")
        if username is None or len(username) == 0:
            missing.append("username")
        if password is None or len(password) == 0:
            missing.append("password")

        if len(missing) > 0:
            err_msg_lines = ["XenSessionCredential is missing required "
                             "fields."]
            err_msg_lines.append("MISSING: {}".format(", ".join(missing)))
            err_msg = os.linesep.join(err_msg_lines)
            raise ConfigurationError(err_msg)

        self._master_url: str = master_url
        self._username: str = username
        self._password: str = password
        return

    @property
    def master_url(self) -> str:
        """
            Return the pool-master XML-RPC URL.

            :returns: The pool-master URL string.
        """
        rtnval = self._master_url
        return rtnval

    @property
    def username(self) -> str:
        """
            Return the XAPI account username.

            :returns: The username string.
        """
        rtnval = self._username
        return rtnval

    @property
    def password(self) -> str:
        """
            Return the XAPI account password.

            :returns: The password string.
        """
        rtnval = self._password
        return rtnval
