import unittest
from unittest.mock import patch

from openstack.exceptions import SDKException

from nforce.client.openstack import OpenstackClient


class TestOpenstackClient(unittest.TestCase):
    @patch("nforce.client.openstack.OpenstackClient.network")
    @patch("nforce.client.openstack.ks_loading")
    @patch("nforce.client.openstack.cfg")
    def test_get_project_id_returns_none(self, mock_cfg, mock_ks_loading, mock_network):
        mock_network.get_port.side_effect = SDKException
        client = OpenstackClient()
        self.assertIsNone(client.get_project_id("aaabbbccc"))

    @patch("nforce.client.openstack.OpenstackClient.network")
    @patch("nforce.client.openstack.ks_loading")
    @patch("nforce.client.openstack.cfg")
    def test_get_project_id(self, mock_cfg, mock_ks_loading, mock_network):
        client = OpenstackClient()
        self.assertEqual(
            client.get_project_id("aaabbbccc"),
            mock_network.get_port.return_value.project_id,
        )


if __name__ == "__main__":
    unittest.main()
