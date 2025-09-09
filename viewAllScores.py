import reviewer
import sqlite3

def viewAllScoresinSet(set, person=False):
    conn = sqlite3.connect(reviewer.FILENAME)
    c = conn.cursor()

    if person != False:
        c.execute(f"SELECT * FROM scores WHERE person={person}")

        scores = c.fetchall()

        conn.close()

        return scores
    else:
        c.execute("SELECT * FROM scores")

        scores = c.fetchall()

        conn.close()

        return scores

def main():
    pass