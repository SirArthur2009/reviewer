import reviewer
import sqlite3

def viewAllScoresinSet(person=None, set=None):
    conn = sqlite3.connect(reviewer.FILENAME)
    c = conn.cursor()

    if person is not None or set is not None:
        if (person is not None and not person.isidentifier()) or (set is not None and not set.isidentifier()):
            print("Invalid input. Please use only letters, numbers, and underscores for person and set names.")
            return []
            

    person = person.replace(" ", "_") if person is not None else None
    set = set.replace(" ", "_") if set is not None else None

    if person is not None and set is not None:
        c.execute(f"SELECT * FROM scores WHERE person='{person}' AND setName='{set}'")

        scores = c.fetchall()

        conn.close()

        return scores
    elif set is not None:
        c.execute(f"SELECT * FROM scores WHERE setName='{set}'")

        scores = c.fetchall()

        conn.close()

        return scores
    elif person is not None:
        c.execute(f"SELECT * FROM scores WHERE person='{person}'")

        scores = c.fetchall()

        conn.close()

        return scores
    else:
        c.execute("SELECT * FROM scores")

        scores = c.fetchall()

        conn.close()

        return scores

def main():
    print("Menu: \n1. View All Scores in Set\n2. View all socres for a person")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        set_name = input("Enter the set name: ")
        scores = viewAllScoresinSet(set=set_name)
        for i, score in enumerate(scores):
            print(f"{i+1}: {score[2]}\t\t\t{score[3]}%")
    elif choice == '2':
        person_name = input("Enter the person's name (use _ for blanks): ")
        set_name = input("Enter the set name (or leave blank to view all sets): ")
        scores = viewAllScoresinSet(person=person_name, set=set_name if set_name else None)
        for i, score in enumerate(scores):
            print(f"{score[1]}:\t{score[2]}\t\t\t{score[3]}%")

if __name__ == "__main__":
    main()