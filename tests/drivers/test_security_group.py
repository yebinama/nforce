import unittest
from unittest.mock import patch, MagicMock

from openstack.exceptions import SDKException

from nforce.drivers.security_group import SecurityGroupDriver


class TestSecurityGroupDriver(unittest.TestCase):
    @patch("nforce.drivers.security_group.OpenstackClient")
    @patch("nforce.drivers.security_group.CONF")
    def test_infra_sg_returns_empty_set(self, mock_conf, mock_openstack_client):
        """Test method infra_sg"""
        mock_conf.nforce.retries = 1
        mock_conf.nforce.ttl = 1
        mock_openstack_client.return_value.network.security_groups.side_effect = (
            SDKException
        )

        driver = SecurityGroupDriver()

        self.assertEqual(set(), driver.infra_sg())

    @patch("nforce.drivers.security_group.OpenstackClient")
    @patch("nforce.drivers.security_group.CONF")
    def test_infra_sg(self, mock_conf, mock_openstack_client):
        """Test method infra_sg"""
        mock_conf.nforce.retries = 1
        mock_conf.nforce.ttl = 1
        mock_conf.nforce.project_id = "abcdef1234"
        mock_conf.nforce.tag = "sg_infra"
        mock_openstack_client.return_value.network.security_groups.return_value = [
            MagicMock(id=1),
            MagicMock(id=4),
        ]
        mock_openstack_client.return_value.network.rbac_policies.return_value = [
            MagicMock(object_id=1),
            MagicMock(object_id=2),
            MagicMock(object_id=4),
        ]

        driver = SecurityGroupDriver()

        self.assertEqual({1, 4}, driver.infra_sg())
        mock_openstack_client.return_value.network.rbac_policies.assert_called_once_with(
            object_type="security_group",
            action="access_as_shared",
            project_id="abcdef1234",
        )
        mock_openstack_client.return_value.network.security_groups.assert_called_once_with(
            tags="sg_infra", project_id="abcdef1234"
        )

    @patch("nforce.drivers.security_group.OpenstackClient")
    @patch("nforce.drivers.security_group.CONF")
    def test_enforce_security_groups_doesnt_update(
        self, mock_conf, mock_openstack_client
    ):
        """Test method enforce_security_groups"""
        mock_conf.nforce.retries = 1
        mock_conf.nforce.ttl = 1
        driver = SecurityGroupDriver()
        with patch.object(driver, "_cached_infra_sg") as mock_infra_sg:
            mock_infra_sg.return_value = {1, 3, 4}
            driver.enforce_security_groups("port_id", [1, 2, 3, 4])
        mock_openstack_client.return_value.network.update_port.assert_not_called()

    @patch("nforce.drivers.security_group.OpenstackClient")
    @patch("nforce.drivers.security_group.CONF")
    def test_enforce_security_groups_updates(self, mock_conf, mock_openstack_client):
        """Test method enforce_security_groups"""
        mock_conf.nforce.retries = 1
        mock_conf.nforce.ttl = 1
        driver = SecurityGroupDriver()
        with patch.object(driver, "_cached_infra_sg") as mock_infra_sg:
            mock_infra_sg.return_value = {1, 3, 4}
            driver.enforce_security_groups("port_id", [1, 2])
        mock_openstack_client.return_value.network.update_port.assert_called_once_with(
            "port_id", security_groups=[1, 2, 3, 4]
        )


if __name__ == "__main__":
    unittest.main()
