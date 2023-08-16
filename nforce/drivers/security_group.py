import tenacity
import nforce.utils.config as cfg

from openstack import exceptions

from nforce.client.openstack import OpenstackClient
from nforce.utils.cache import lru_cache_ttl


from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class SecurityGroupDriver:
    def __init__(self, conf=None):
        """
        Constructor

        :param conf: oslo configuration
        """
        self._client = OpenstackClient()
        self.conf = conf or CONF
        self._retry = tenacity.retry(
            stop=tenacity.stop_after_attempt(self.conf.nforce.retries),
            wait=tenacity.wait_exponential(multiplier=0.02, max=1),
            reraise=True,
        )
        self._cached_infra_sg = lru_cache_ttl(ttl=self.conf.nforce.ttl)(self.infra_sg)

    def infra_sg(self):
        """
        Return all tagged infra security groups
        """
        try:
            security_groups_ids = {
                sg.id
                for sg in self._retry(self._client.network.security_groups)(
                    tags=self.conf.nforce.tag,
                    project_id=self.conf.nforce.project_id,
                )
            }
            return {
                rbac.object_id
                for rbac in self._retry(self._client.network.rbac_policies)(
                    object_type="security_group",
                    action="access_as_shared",
                    project_id=self.conf.nforce.project_id,
                )
                if rbac.object_id in security_groups_ids
            }
        except exceptions.SDKException:
            LOG.error(
                "Can't read infra sg from project %s", self.conf.nforce.project_id
            )
            return set()

    def enforce_security_groups(self, port_id, security_groups):
        """
        Enforce tagged security groups for port

        :param port_id: port id
        :param security_groups: current security groups
        """
        if missing_sg := list(self._cached_infra_sg().difference(security_groups)):
            try:
                self._retry(self._client.network.update_port)(
                    port_id,
                    security_groups=(security_groups + missing_sg),
                )
            except exceptions.SDKException:
                LOG.error("Can't add infra sg %s to port %s", missing_sg, port_id)
            else:
                LOG.info("Successfully added sg %s to port %s", missing_sg, port_id)
