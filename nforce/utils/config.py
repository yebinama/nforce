from keystoneauth1 import loading as ks_loading

from oslo_config import cfg

from nforce.client.openstack import OpenstackClient

CONF = cfg.ConfigOpts()

nforce_opts = [
    cfg.StrOpt("tag", help="Security Groups tag."),
    cfg.StrOpt("project_id", help="Security Groups project id."),
    cfg.IntOpt("ttl", help="TTL for requesting mandatory security groups."),
    cfg.IntOpt("retries", help="Number of retries for OpenStack requests."),
]


def register_opts():
    """
    Register configuration options

    """
    CONF.register_opts(nforce_opts, group="nforce")
    # OpenStack configuration
    ks_loading.register_auth_conf_options(OpenstackClient.CONF, "openstack")
    ks_loading.register_session_conf_options(OpenstackClient.CONF, "openstack")
    ks_loading.register_adapter_conf_options(OpenstackClient.CONF, "neutron")


def init(args=None):
    """
    Load configuration

    :param args: oslo config arguments
    """
    register_opts()
    CONF(args, project="nforce")
    OpenstackClient.CONF(args, project="nforce")
