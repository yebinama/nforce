from oslo_log import log as logging
from oslo_config import cfg

from neutron_lib.agent import l2_extension

from os_ken.lib import hub

import nforce.utils.config as config
from nforce.drivers.security_group import SecurityGroupDriver

LOG = logging.getLogger(__name__)


class NforceNeutronAgentExtension(l2_extension.L2AgentExtension):
    def initialize(self, connection, driver_type):
        """Initialize agent extension."""
        nforce_opts = [
            cfg.StrOpt("config_file", help="Nforce Agent Extension configuration file.")
        ]
        cfg.CONF.register_opts(nforce_opts, group="nforce")

        # Initialize config
        config.init(["--config-file", cfg.CONF.nforce.config_file])

        self._driver = SecurityGroupDriver()

    def handle_port(self, context, data):
        """Handle a port add/update event.

        This can be called on either create or update, depending on the
        code flow. Thus, it's this function's responsibility to check what
        actually changed.

        :param context: RPC context.
        :param data: Port data.
        """
        LOG.info("Received update notification %s", data)

        if not data.get("device_owner", "").startswith("compute:"):
            LOG.info("Not treating port %s as it's not a vm port", data["port_id"])
            return

        if data.get("migrating_to") is not None:
            LOG.info("Not treating port %s as it is migrating", data["port_id"])
            return

        try:
            hub.spawn(
                self._driver.enforce_security_groups,
                data["port_id"],
                data["security_groups"],
            )
        except KeyError as err:
            LOG.error("Can't retrieve key %s from port data", err)

    def delete_port(self, context, data):
        """Handle a port delete event.

        :param context: RPC context.
        :param data: Port data.
        """
        pass
