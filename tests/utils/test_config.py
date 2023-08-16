from unittest.case import TestCase
from unittest.mock import patch

import nforce.utils.config as config


class TestConfig(TestCase):
    @patch("nforce.utils.config.OpenstackClient")
    @patch("nforce.utils.config.ks_loading")
    @patch("nforce.utils.config.CONF")
    def test_register_opts(self, mock_cfg, mock_ks_loading, mock_os_client):
        """Test function register_opts"""
        config.register_opts()

        mock_cfg.register_opts.assert_called_once_with(
            config.nforce_opts, group="nforce"
        )

        mock_ks_loading.register_auth_conf_options.assert_called_once_with(
            mock_os_client.CONF, "openstack"
        )
        mock_ks_loading.register_session_conf_options.assert_called_once_with(
            mock_os_client.CONF, "openstack"
        )
        mock_ks_loading.register_adapter_conf_options.assert_called_once_with(
            mock_os_client.CONF, "neutron"
        )

    @patch("nforce.utils.config.register_opts")
    @patch("nforce.utils.config.CONF")
    @patch("nforce.utils.config.OpenstackClient")
    def test_init(
        self,
        mock_os_client,
        mock_cfg,
        mock_register_opts,
    ):
        """Test function init"""
        config.init()

        mock_cfg.assert_called_once_with(None, project="nforce")
        mock_os_client.CONF.assert_called_once_with(None, project="nforce")

        mock_register_opts.assert_called_once()
