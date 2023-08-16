from keystoneauth1 import loading as ks_loading
from oslo_config import cfg

from oslo_log import log as logging

from openstack import connection
from openstack.exceptions import SDKException

LOG = logging.getLogger(__name__)


class OpenstackClient(connection.Connection):
    CONF = cfg.ConfigOpts()

    def __init__(self, section="openstack"):
        """
        Init

        :param section: configuration section
        """
        auth = ks_loading.load_auth_from_conf_options(self.CONF, section)
        session = ks_loading.load_session_from_conf_options(
            self.CONF, section, auth=auth
        )
        super().__init__(session=session, oslo_conf=self.CONF)

    def get_project_id(self, os_port_id):
        """
        Retrieve project id associated to OpenStack port id

        :param os_port_id: OpenStack port id
        """
        try:
            return self.network.get_port(os_port_id).project_id
        except SDKException:
            LOG.error("Can't retrieve project_id for OpenStack port %s", os_port_id)
            return None
