import unittest
import os
import json
from scraper.smashgg import SmashGGScraper

TEST_URL_1 = 'https://smash.gg/tournament/htc-throwdown/brackets/10448/2096/6529'
TEST_URL_2 = 'https://smash.gg/tournament/tiger-smash-4/brackets/11097/21317/70949'
TEST_DATA1 = os.path.abspath('test' + os.sep + 'test_scraper' + os.sep + 'data' + os.sep + 'smashgg.json')
TEST_DATA2 = os.path.abspath('test' + os.sep + 'test_scraper' + os.sep + 'data' + os.sep + 'smashgg2.json')
TEST_TOURNAMENT_ID_1 = 11226
TEST_TOURNAMENT_ID_2 = 70949
TEST_TOURNAMENT_ID_3 = 83088
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
        self.tournament1 = SmashGGScraper(TEST_URL_1)
        self.tournament2 = SmashGGScraper(TEST_URL_2)
        # self.tournament3 = SmashGGScraper(TEST_TOURNAMENT_ID_3)

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
    def test_get_raw_sub1(self):
        tournament = self.tournament1
        self.assertIsNotNone(tournament.get_raw()['smashgg']['entities']['sets'])
        seeds = self.assertIsNotNone(tournament.get_raw()['smashgg']['entities']['seeds'])
        seeds = tournament.get_raw()['smashgg']['entities']['seeds']
        sets = tournament.get_raw()['smashgg']['entities']['sets']
        for seed in seeds:
            self.assertIsNotNone(seed['entrantId'])
            self.assertIsNotNone(seed['mutations']['players'])
            this_player = seed['mutations']['players']
            for player_id in this_player:
                id = player_id

            self.assertIsNotNone(this_player[id]['gamerTag'].strip())

        #for set in sets:
        #    self.assertIsNotNone(set['winnerId'])
            # loserId is allowed to be None because of a Bye

    # @unittest.skip('test is failing, May be API agile iterations manipulating data. Need to revisit')
    def test_get_raw_sub2(self):
        tournament = self.tournament2
        self.assertIsNotNone(tournament.get_raw()['smashgg']['entities']['sets'])
        seeds = self.assertIsNotNone(tournament.get_raw()['smashgg']['entities']['seeds'])
        seeds = tournament.get_raw()['smashgg']['entities']['seeds']
        sets = tournament.get_raw()['smashgg']['entities']['sets']
        for seed in seeds:
            self.assertIsNotNone(seed['entrantId'])
            self.assertIsNotNone(seed['mutations']['players'])
            this_player = seed['mutations']['players']
            for player_id in this_player:
                id = player_id

            self.assertIsNotNone(this_player[id]['gamerTag'].strip())

        #for set in sets:
        #    self.assertIsNotNone(set['winnerId'])
            # loserId is allowed to be None because of a Bye

    def test_get_tournament_id_from_url1(self):
        self.assertEqual(SmashGGScraper.get_tournament_id_from_url(TEST_URL_1), 6529)

    def test_get_tournament_id_from_url2(self):
        self.assertEqual(SmashGGScraper.get_tournament_id_from_url(TEST_URL_2), 70949)

    def test_get_tournament_name_from_url1(self):
        self.assertEqual(SmashGGScraper.get_tournament_name_from_url(TEST_URL_1), 'htc throwdown')

    def test_get_tournament_name_from_url2(self):
        self.assertEqual(SmashGGScraper.get_tournament_name_from_url(TEST_URL_2), 'tiger smash 4')

    def test_get_player_by_entrant_id1(self):
        player = self.tournament1.get_player_by_entrant_id(TEST_PLAYER_ENTRANTID_1)
        self.assertEqual(player.name, 'Joseph Marquez')
        self.assertEqual(player.smash_tag, 'Mango')
        self.assertEqual(player.region, 'SoCal')

    def test_get_player_by_entrant_id2(self):
        player = self.tournament2.get_player_by_entrant_id(TEST_PLAYER_ENTRANTID_2)
        self.assertEqual(player.name, 'Sami Muhanna')
        self.assertEqual(player.smash_tag, 'Druggedfox')
        self.assertEqual(player.region, 'GA')

    def test_get_player_by_smashgg_id1(self):
        player = self.tournament1.get_player_by_smashgg_id(TEST_PLAYER_SMASHGGID_1)
        self.assertEqual(player.name, 'Joseph Marquez')
        self.assertEqual(player.smash_tag, 'Mango')
        self.assertEqual(player.region, 'SoCal')

    def test_get_player_by_smashgg_id2(self):
        player = self.tournament2.get_player_by_smashgg_id(TEST_PLAYER_SMASHGGID_2)
        self.assertEqual(player.name, 'Sami Muhanna')
        self.assertEqual(player.smash_tag, 'Druggedfox')
        self.assertEqual(player.region, 'GA')

    def test_get_players1(self):
        self.assertEqual(len(self.tournament1.get_players()), 48)

    def test_get_players2(self):
        self.assertEquals(len(self.tournament2.get_players()), 24)

    def test_get_matches1(self):
        self.assertEqual(len(self.tournament1.get_matches()), 58)

    def test_get_matches2(self):
        self.assertEquals(len(self.tournament2.get_matches()), 46)

    def test_get_smashgg_matches1(self):
        self.assertEqual(len(self.tournament1.get_smashgg_matches()), 58)

    def test_get_smashgg_matches2(self):
        self.assertEqual(len(self.tournament2.get_smashgg_matches()), 46)