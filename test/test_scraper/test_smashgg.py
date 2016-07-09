import unittest
import os
import json
from scraper.smashgg import SmashGGScraper

TEST_URL_1 = 'https://smash.gg/tournament/htc-throwdown/brackets/10448/2096/6529'
TEST_URL_2 = 'https://smash.gg/tournament/tiger-smash-4/brackets/11097/21317/70949'
TEST_URL_3 = 'https://smash.gg/tournament/ceo-2016/brackets/11789/45259/150418'
TEST_DATA1 = os.path.abspath('test' + os.sep + 'test_scraper' + os.sep + 'data' + os.sep + 'smashgg.json')
TEST_DATA2 = os.path.abspath('test' + os.sep + 'test_scraper' + os.sep + 'data' + os.sep + 'smashgg2.json')
TEST_EVENT_ID_1 = 10448
TEST_EVENT_ID_2 = 11097
TEST_EVENT_ID_3 = 11789
TEST_PHASE_ID_1 = 2096
TEST_PHASE_ID_2 = 21317
TEST_PHASE_ID_3 = 45259
TEST_PHASE_GROUP_ID_1 = 11226
TEST_PHASE_GROUP_ID_2 = 70949
TEST_PHASE_GROUP_ID_3 = 83088
TEST_PLAYER_ENTRANTID_1 = 16081
TEST_PLAYER_ENTRANTID_2 = 110555
TEST_PLAYER_ENTRANTID_3 = 52273
TEST_PLAYER_SMASHGGID_1 = 1000
TEST_PLAYER_SMASHGGID_2 = 4442
TEST_PLAYER_SMASHGGID_3 = 13932

# TO ACCESS THE SMASHGG DUMPS USED HERE, THE FOLLOWING LINKS WILL GET YOU THERE
# https://api.smash.gg/phase_group/11226?expand[0]=sets&expand[1]=seeds&expand[2]=entrants&expand[3]=matches TEST API

# https://api.smash.gg/phase_group/6529?expand[0]=sets&expand[1]=seeds&expand[2]=entrants&expand[3]=matches
# https://api.smash.gg/phase_group/70949?expand[0]=sets&expand[1]=seeds&expand[2]=entrants&expand[3]=matches

class TestSmashGGScraper(unittest.TestCase):
    def setUp(self):
        self.tournament1 = TestSmashGGScraper.tournament1
        self.tournament2 = TestSmashGGScraper.tournament2
        #self.tournament3 = SmashGGScraper(TEST_URL_3)
        #list = self.tournament3.get_matches()
        #print 'hello'

    # query tons of URLs just once, not for each test
    @classmethod
    def setUpClass(cls):
        print 'Pulling tournaments from smash.gg ...'
        super(TestSmashGGScraper, cls).setUpClass()
        cls.tournament1 = SmashGGScraper(TEST_URL_1)
        cls.tournament2 = SmashGGScraper(TEST_URL_2)


    def tearDown(self):
        self.tournament1 = None
        self.tournament2 = None

    @unittest.skip('skipping test_get_raw1 until api is complete')
    def test_get_raw1(self):
        with open(TEST_DATA1) as data1:
            self.tournament1_json_dict = json.load(data1)
        self.assertEqual(self.tournament1.get_raw()['smashgg'], self.tournament1_json_dict)

    @unittest.skip('skipping test_get_raw2 until api is complete')
    def test_get_raw2(self):
        with open(TEST_DATA2) as data2:
            self.tournament2_json_dict = json.load(data2)
        self.assertEqual(self.tournament2.get_raw()['smashgg'], self.tournament2_json_dict)

    # @unittest.skip('test is failing, May be API agile iterations manipulating data. Need to revisit')
    def test_get_raw_sub(self):
        raw = self.tournament1.get_raw()

        self.assertTrue('event' in raw)
        self.assertTrue('groups' in raw)
        self.assertEqual(len(raw['groups']), 35)

        entrants = raw['event']['entities']['entrants']
        for entrant in entrants:
            self.assertIsNotNone(entrant['id'])

        # TODO: add more stuff

        raw = self.tournament2.get_raw()

        self.assertTrue('event' in raw)
        self.assertTrue('groups' in raw)
        self.assertEqual(len(raw['groups']), 10)

        entrants = raw['event']['entities']['entrants']
        for entrant in entrants:
            self.assertIsNotNone(entrant['id'])

        # TODO: add more stuff

    def test_player_lookup(self):
        player = self.tournament1.player_lookup[TEST_PLAYER_ENTRANTID_1]
        self.assertEqual(player.smash_tag, 'C9 | Mango')

        player = self.tournament2.player_lookup[TEST_PLAYER_ENTRANTID_2]
        self.assertEqual(player.smash_tag, 'Druggedfox')

    def test_get_players(self):
        self.assertEqual(len(self.tournament1.get_players()), 386)
        self.assertEquals(len(self.tournament2.get_players()), 75)

    def test_get_matches(self):
        self.assertEqual(len(self.tournament1.get_matches()), 731)
        # spot check that mang0 got double elim'd
        mango_count = 0
        for m in self.tournament1.get_matches():
            if m.loser == 'C9 | Mango':
                mango_count += 1
        print mango_count
        self.assertEqual(2, mango_count, msg="mango didnt get double elim'd?")

        self.assertEquals(len(self.tournament2.get_matches()), 436)
        # spot check that Druggedfox was only in 5 matches, and that he won all of them
        sami_count = 0
        for m in self.tournament2.get_matches():
            if m.winner == 'Druggedfox':
                sami_count += 1
            self.assertFalse(m.loser == 'Druggedfox')
        self.assertEqual(14, sami_count)

    def test_get_date(self):
        date = self.tournament1.get_date()
        self.assertEqual(date.year, 2015)
        self.assertEqual(date.month, 9)
        self.assertEqual(date.day, 19)

        date = self.tournament2.get_date()
        self.assertEqual(date.year, 2016)
        self.assertEqual(date.month, 3)
        self.assertEqual(date.day, 26)

    def test_get_name(self):
        self.assertEqual(self.tournament1.get_name(), 'htc throwdown')
        self.assertEqual(self.tournament2.get_name(), 'tiger smash 4')

    def test_duplicate_tags(self):
        tags = self.tournament1.get_players()
        self.assertEqual(len(tags), len(set(tags)))
        tags = self.tournament2.get_players()
        self.assertEqual(len(tags), len(set(tags)))

    def test_get_group_ids(self):
        group_ids = self.tournament1.get_group_ids()
        self.assertEqual(len(group_ids), 35)
        group_ids = self.tournament2.get_group_ids()
        self.assertEqual(len(group_ids), 10)

    def test_get_tournament_phase_id_from_url(self):
        self.assertEqual(SmashGGScraper.get_tournament_phase_id_from_url(TEST_URL_1), 6529)
        self.assertEqual(SmashGGScraper.get_tournament_phase_id_from_url(TEST_URL_2), 70949)

    def test_get_tournament_name_from_url(self):
        self.assertEqual(SmashGGScraper.get_tournament_name_from_url(TEST_URL_1), 'htc throwdown')
        self.assertEqual(SmashGGScraper.get_tournament_name_from_url(TEST_URL_2), 'tiger smash 4')

    def test_get_event_name(self):
        self.assertEqual(SmashGGScraper.get_event_name(TEST_EVENT_ID_1), 'Melee Singles')
        self.assertEqual(SmashGGScraper.get_event_name(TEST_EVENT_ID_2), 'Melee Singles')

    def test_get_phase_name(self):
        self.assertEqual(SmashGGScraper.get_phase_bracket_name(TEST_PHASE_ID_1), 'Round 2 Bracket')
        self.assertEqual(SmashGGScraper.get_phase_bracket_name(TEST_PHASE_ID_2), 'Final Bracket')

    def test_get_phasename_id_map(self):
        self.assertEqual(len(SmashGGScraper.get_phasename_id_map(TEST_EVENT_ID_1)), 3)
        self.assertEqual(len(SmashGGScraper.get_phasename_id_map(TEST_EVENT_ID_2)), 3)