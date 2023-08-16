import unittest
from unittest.mock import patch, MagicMock

from nforce.neutron.extension import NforceNeutronAgentExtension


class TestNforceNeutronAgentExtension(unittest.TestCase):
    @patch("nforce.neutron.extension.hub")
    def test_handle_port_device_owner(self, mock_hub):
        """Test method handle_port"""
        extension = NforceNeutronAgentExtension()
        extension.handle_port(
            None, {"device_owner": "network:dhcp", "port_id": "aaabbbcccddd"}
        )
        mock_hub.spawn.assert_not_called()

    @patch("nforce.neutron.extension.hub")
    def test_handle_port_migrating_to(self, mock_hub):
        """Test method handle_port"""
        extension = NforceNeutronAgentExtension()
        extension.handle_port(
            None,
            {
                "device_owner": "compute:nova",
                "port_id": "aaabbbcccddd",
                "migrating_to": "hypervisor2",
            },
        )
        mock_hub.spawn.assert_not_called()

    @patch("nforce.neutron.extension.hub")
    def test_handle_port(self, mock_hub):
        """Test method handle_port"""
        extension = NforceNeutronAgentExtension()
        extension._driver = MagicMock()
        extension.handle_port(
            None,
            {
                "device_owner": "compute:nova",
                "port_id": "aaabbbcccddd",
                "migrating_to": None,
                "security_groups": ["id1", "id2"],
            },
        )
        mock_hub.spawn.assert_called_once_with(
            extension._driver.enforce_security_groups, "aaabbbcccddd", ["id1", "id2"]
        )

    @patch("nforce.neutron.extension.SecurityGroupDriver")
    @patch("nforce.neutron.extension.config")
    @patch("nforce.neutron.extension.cfg")
    @patch("nforce.neutron.extension.hub")
    def test_initialize(self, mock_hub, mock_cfg, mock_config, mock_driver):
        """Test method initialize"""
        extension = NforceNeutronAgentExtension()
        extension.initialize(None, "openvswitch")
        self.assertEqual(extension._driver, mock_driver.return_value)
        mock_config.init.assert_called_once_with(
            ["--config-file", mock_cfg.CONF.nforce.config_file]
        )


if __name__ == "__main__":
    unittest.main()
