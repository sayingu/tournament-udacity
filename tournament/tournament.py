#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cur = connect()

    cur.execute("DELETE FROM Matches;")

    db.commit()

    cur.close()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cur = connect()

    cur.execute("DELETE FROM Players;")

    db.commit()

    cur.close()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cur = connect()

    cur.execute("SELECT COUNT (id) FROM Players;")

    row = cur.fetchone()

    cur.close()
    db.close()

    return row[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cur = connect()

    cur.execute("INSERT INTO Players (name) VALUES (%s)", (name, ))

    db.commit()

    cur.close()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cur = connect()

    sql = '''
    SELECT id, name, SUM (wins) AS wins, SUM (wins + loses) AS matches
      FROM (SELECT Players.id, Players.name, COUNT (Matches.winner) AS wins, 0 AS loses
              FROM Players LEFT OUTER JOIN Matches ON (Players.id = Matches.winner)
             GROUP BY Players.id, Players.name
             UNION
            SELECT Players.id, Players.name, 0 AS wins, COUNT (Matches.loser) AS loses
              FROM Players LEFT OUTER JOIN Matches ON (Players.id = Matches.loser)
             GROUP BY Players.id, Players.name) T
     GROUP BY id, name
     ORDER BY wins DESC;
    '''
    cur.execute(sql)

    rows = cur.fetchall()

    cur.close()
    db.close()

    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cur = connect()

    cur.execute(
        "INSERT INTO Matches (winner, loser) VALUES (%s, %s)", (winner, loser))

    db.commit()

    cur.close()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    rows = playerStandings()

    i = 0
    pairs = []
    while i < len(rows):
        id1 = rows[i][0]
        name1 = rows[i][1]
        id2 = rows[i + 1][0]
        name2 = rows[i + 1][1]
        pairs.append((id1, name1, id2, name2))
        i += 2

    return pairs
