import requests
from terminaltables import GithubFlavoredMarkdownTable as GFMT


def profile(username: str):
    """Return information about a particular user of lichess.org
        :username: Name of the lichess user for which the
                    info is displayed
    """
    user_name = "".join(username)
    if user_name:
        url = " https://lichess.org/api/user/" + user_name
    else:
        return "Please use the format <b>/profile username</b>"
    data = requests.get(url).json()

    name = data['username']
    followers = data['nbFollowers']
    following = data['nbFollowing']
    losses = data['count']['loss']
    wins = data['count']['win']

    table_data = [['Name', 'Followers', 'Following', 'wins', 'loss']]
    table_data.append([name, followers, following, wins, losses])
    table = handle_tables(table_data)

    return table


def top_players(variant: str):
    """List down top 10 player for a particular variant
        :variant: Chess variation.Eg blitz, rapid, bullet etc.
    """
    args = "".join(variant)

    if args:
        url = "https://lichess.org/player/top/10/{argv}".format(argv=args)
    else:
        return "Please use the format <b>/top chess_variant</b>"

    data = requests.get(url, headers={"Accept": "application/vnd.lichess.v3+json"}).json()

    table_data = [['Name', 'Rating']]
    for i in range(10):
        name = data["users"][i]["username"]
        rating = data["users"][i]["perfs"][variant]["rating"]
        table_data.append([name, rating])

    table = handle_tables(table_data)

    return table


def is_online(username):
    """Check if a particular user is online or not
        :username: name of users. This can take name of multiple
                    users separated by a comma.
                    Ex- mzfr,ugtan,fins
    """
    if username:
        url = "https://lichess.org/api/users/status?ids=" + username
    else:
        return "Please sue the format <b>/online usernam(s)</b>"

    data = requests.get(url).json()
    names = username.split(",")
    active = []
    for index, user in enumerate(names):
        if names[index] == user and 'online' in data[index]:
            active.append('%s is online ' % user)
        else:
            active.append('%s is not online' % user)
    active = "\n".join(active)
    return active


def streamers():
    """Get name and link of all the live streamers on lichess.org"""
    stream = "https://lichess.org/streamer/"
    url = stream + "live"
    data = requests.get(url).json()
    table = []

    for index, streamers_name in enumerate(data):
        name = streamers_name['name']
        link = stream + name
        table.append(name)
        table.append(link)

    table = "\n".join(table)
    return table


def handle_tables(table_data: list):
    """Creates a table for all the list data is passed to it
        :table_data: Data in a list format.
    """
    table = GFMT(table_data)
    table.inner_row_border = True
    table = table = "<pre>{}</pre>".format(table.table)
    return table


if __name__ == "__main__":
    streamers()
    is_online("mzfr")
