from model import AliasMapping

# return map from alias -> Player
# We choose the Player whose alias matches, or if none match exactly,
# the player with the shortest name


def get_top_suggestion_for_aliases(dao, aliases):
    suggestions_map = get_player_or_suggestions_from_player_aliases(
        dao, aliases)
    ret = {}

    for entry in suggestions_map.iteritems():
        if entry[1]["player"] is not None:
            ret[entry[0]] = entry[1]["player"]
        elif entry[1]['suggestions']:
            ret[entry[0]] = min(entry[1]["suggestions"],
                                key=lambda p: len(p.name))
        else:
            ret[entry[0]] = None

    return ret

# return the result of get_top_suggestion_for_aliases in the list format stored in the db
# TODO we should probably sanity check here to make sure we don't return
# the same player id for multiple aliases


def get_alias_to_id_map_in_list_format(dao, aliases):
    alias_to_id_map = get_top_suggestion_for_aliases(dao, aliases)
    list_format = []
    for alias, player in alias_to_id_map.iteritems():
        list_format.append(AliasMapping(
            player_alias=alias,
            player_id=player.id if player else None
        ))
    return list_format

# return a map from alias -> suggestions (a list of Players)


def get_player_suggestions_from_player_aliases(dao, aliases):
    alias_to_suggestion_map = {}

    for alias in aliases:
        alias_to_suggestion_map[
            alias] = dao.get_players_with_similar_alias(alias)

    return alias_to_suggestion_map

# return a map from alias -> {"player": Player with matches,
# "suggestions": list of Players}


def get_player_or_suggestions_from_player_aliases(dao, aliases):
    alias_to_player_or_suggestions_map = {}

    for alias in aliases:
        alias_to_player_or_suggestions_map[alias] = {
            "player": dao.get_player_by_alias(alias),
            "suggestions": dao.get_players_with_similar_alias(alias)
        }

    return alias_to_player_or_suggestions_map
