import json
import unittest

from base import SD_VM_Local_Test


class SD_SVS_Tests(SD_VM_Local_Test):
    def setUp(self):
        self.vm_name = "sd-svs"
        super(SD_SVS_Tests, self).setUp()

    def test_decrypt_sd_user_profile(self):
        contents = self._get_file_contents(
            "/etc/profile.d/sd-svs-qubes-gpg-domain.sh"
        )
        expected_content = 'export QUBES_GPG_DOMAIN="sd-gpg"\n'
        self.assertEqual(contents, expected_content)

    def test_open_in_dvm_desktop(self):
        contents = self._get_file_contents(
            "/usr/share/applications/open-in-dvm.desktop"
        )
        expected_content = "TryExec=/usr/bin/qvm-open-in-vm"
        self.assertTrue(expected_content in contents)

    def test_mimeapps(self):
        cmd = "perl -F= -lane 'print $F[1]' /usr/share/applications/mimeapps.list | sort | uniq -c"
        results = self._run(cmd)
        expected_results = "2 \n    294 open-in-dvm.desktop;"
        self.assertEqual(results, expected_results)

    def test_sd_client_package_installed(self):
        self.assertTrue(self._package_is_installed("securedrop-client"))

    def test_sd_client_dependencies_installed(self):
        self.assertTrue(self._package_is_installed("python3-pyqt5"))
        self.assertTrue(self._package_is_installed("python3-pyqt5.qtsvg"))

    def test_sd_client_config(self):
        with open("config.json") as c:
            config = json.load(c)
            submission_fpr = config['submission_key_fpr']

        line = '{{"journalist_key_fingerprint": "{}"}}'.format(submission_fpr)
        self.assertFileHasLine("/home/user/.securedrop_client/config.json", line)


def load_tests(loader, tests, pattern):
    suite = unittest.TestLoader().loadTestsFromTestCase(SD_SVS_Tests)
    return suite
