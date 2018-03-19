import mock
from django.test import TestCase, override_settings
from data_finder.helpers import EveryElectionWrapper


# mock get_data() functions
def get_data_exception(self, query_url):
    raise Exception()

def get_data_no_elections(self, query_url):
    return []

def get_data_only_group(self, query_url):
    return [
        { 'election_title': 'some election', 'group_type': 'election' },
        { 'election_title': 'some election', 'group_type': 'organisation' }
    ]

def get_data_group_and_ballot(self, query_url):
    return [
        { 'election_title': 'some election', 'group_type': 'organisation' },
        { 'election_title': 'some election', 'group_type': None }
    ]

def get_data_with_elections(self, query_url):
    return [
        {
            'election_title': 'some election',
            'group_type': 'organisation'
        },  # no explanation key
        {
            'election_title': 'some election',
            'group_type': None,
            'explanation': None  # null explanation key
        },
        {
            'election_title': 'some election',
            'group_type': None,
            'explanation': 'some text'  # explanation key contains text
        },
    ]

class EveryElectionWrapperTest(TestCase):

    @override_settings(EVERY_ELECTION={'CHECK': True, 'HAS_ELECTION': True})
    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_exception)
    def test_exception(self):
        ee = EveryElectionWrapper(postcode='AA11AA')
        self.assertFalse(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertEqual([], ee.get_explanations())

    @override_settings(EVERY_ELECTION={'CHECK': True, 'HAS_ELECTION': True})
    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_no_elections)
    def test_no_elections(self):
        ee = EveryElectionWrapper(postcode='AA11AA')
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        self.assertEqual([], ee.get_explanations())

    @override_settings(EVERY_ELECTION={'CHECK': True, 'HAS_ELECTION': True})
    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_with_elections)
    def test_elections(self):
        ee = EveryElectionWrapper(postcode='AA11AA')
        self.assertTrue(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertEqual([
            {'title': 'some election', 'explanation': 'some text'}
        ], ee.get_explanations())

    @override_settings(EVERY_ELECTION={'CHECK': True, 'HAS_ELECTION': True})
    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_only_group)
    def test_elections_only_group(self):
        ee = EveryElectionWrapper(postcode='AA11AA')
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        self.assertEqual([], ee.get_explanations())

    @override_settings(EVERY_ELECTION={'CHECK': True, 'HAS_ELECTION': True})
    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_group_and_ballot)
    def test_elections_group_and_ballot(self):
        ee = EveryElectionWrapper(postcode='AA11AA')
        self.assertTrue(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertEqual([], ee.get_explanations())

    @override_settings(EVERY_ELECTION={'CHECK': True, 'HAS_ELECTION': False})
    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_group_and_ballot)
    def test_settings_override1(self):
        ee = EveryElectionWrapper(postcode='AA11AA')
        # election is really happening here
        self.assertTrue(ee.has_election())
        # manually override it to false
        with override_settings(EVERY_ELECTION={'CHECK': False, 'HAS_ELECTION': False}):
            ee = EveryElectionWrapper(postcode='AA11AA')
            self.assertFalse(ee.has_election())

    @override_settings(EVERY_ELECTION={'CHECK': True, 'HAS_ELECTION': False})
    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_only_group)
    def test_settings_override2(self):
        ee = EveryElectionWrapper(postcode='AA11AA')
        # election is not really happening here
        self.assertFalse(ee.has_election())
        # manually override it to true
        with override_settings(EVERY_ELECTION={'CHECK': False, 'HAS_ELECTION': True}):
            ee = EveryElectionWrapper(postcode='AA11AA')
            self.assertTrue(ee.has_election())
