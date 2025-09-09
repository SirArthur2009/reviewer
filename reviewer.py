import random
import sqlite3

FILENAME = "C:/Users/levig/OneDrive/Documents/Coding/Python/Complex_Programs/reviewer/vocaber.db"

# ======= FOR LOGGING AND RETRIEVING SCORES INTO A DATABASE =======
def logScore(setName, person, score):
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, setName TEXT, person TEXT, score INTEGER)")

    c.execute("""INSERT INTO scores (setName, person, score) VALUES (?, ?, ?)""", (setName, person, score))

    conn.commit()
    conn.close()    

def retrieveTopTen(setName):
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, setName TEXT, person TEXT, score INTEGER)")

    c.execute("SELECT * FROM scores WHERE setName = ? ORDER BY score DESC LIMIT 10", (setName,))

    topScores = c.fetchall() or None

    conn.close()

    return topScores

# ======= FOR CREATING SETS AND ADDING TERMS =======
def addTable(name, path):
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS allTables (id INTEGER PRIMARY KEY, tableName TEXT, subpath TEXT)")
    
    # I dont want it to log it if it's already in it
    c.execute("SELECT * FROM allTables WHERE tableName = ?", (name,))
    if c.fetchone() is not None:
        conn.commit()
        conn.close()
        return

    c.execute("""INSERT INTO allTables (tableName, subpath) VALUES (?, ?)""", (name, path))
    
    conn.commit()
    conn.close()

def createSet():
    name = input("What would you like to name this set? ")

    path = input("What is the sub path for this set? If you do not know type in, 'I do not know'\n")

    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()
    # Using f-string to create table name dynamically, but ensuring it's a valid identifier to prevent SQL injection
    if not name.lower().isidentifier():
        print("Invalid table name. Please use only letters, numbers, and underscores.")
        return
    c.execute(f"""CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY, term TEXT, answers TEXT)""")

    conn.commit()
    conn.close()

    addTable(name, path)

    addTerms = input("Would you like to add terms to this set? ").lower()
    if addTerms in ['y', 'yes', 'sure']:
        addTermsToTable(name)

def addTermsToTable(table):
    while True:
        print("\nq to quit\n")
        term = input("What's the term? \n")
        answers = input("What's the answer? \n")

        if term.lower() in ['q', 'quit'] or answers.lower() in ['q', 'quit']:
            break

        addTermToTable(term, answers, table)

def addTermToTable(term, answers, table):
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    # Using f-string to create table name dynamically, but ensuring it's a valid identifier to prevent SQL injection
    if not table.lower().isidentifier():
        print("Invalid table name. Please use only letters, numbers, and underscores.")
        return "Invalid table name. Please use only letters, numbers, and underscores."
    
    c.execute(f"""INSERT INTO {table} (term, answers) VALUES
              (?, ?)
              """, (term, answers))
    
    conn.commit()
    conn.close()

# ======= Misc =======
def getAllSets():
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    c.execute("SELECT * FROM allTables")

    tables = c.fetchall()

    conn.close()

    return tables

def getTermsFromSet(set):
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    if not set.lower().isidentifier():
        print("Invalid table name. Please use only letters, numbers, and underscores.")
        return "Invalid table name. Please use only letters, numbers, and underscores."
    c.execute(f"SELECT * FROM {set}")

    terms = c.fetchall()

    conn.close()

    return terms

# ======= FOR WORKING WITH PREMADE SETS =======
def openVocabSet():
    score = 0

    missedTerms = []

    sets = getAllSets()

    if not sets:
        print("No sets available. Create one first.")
        return

    setName = selectSet(sets)
    terms = getTermsFromSet(setName)

    if not isinstance(terms, list) or not terms:
        print(terms)
        return

    random.shuffle(terms)

    for term in terms:
        answersLeft = term[2].strip().lower().split(", ")
        if not isinstance(answersLeft, list):
            answersLeft = [answersLeft]

        messedUp = False
        firstLoop = True
        while answersLeft:
            if firstLoop:
                answer = input(f"What is an answer for {term[1]}? \n")
            else:
                answer = input(f"What is another answer for {term[1]}? \n")

            if answer.lower() in ['q', 'quit']:
                break
            if answer.strip().lower() in answersLeft:
                print("Correct!\n")
                answersLeft.remove(answer.strip().lower())
            else:
                input(f"Wrong. Correct answer was: {answersLeft}\n")
                missedTerms.append(term)
                messedUp = True

            firstLoop = False

        if not messedUp:
            score += 1

    if not missedTerms:
        print("No missed terms.")
    else:
        choice = input("Do you want to run through the missed terms? (y/n) ")
        if choice.lower() in ['y', 'yes', 'sure']:
            runThroughMissed(missedTerms)

    #This needs to be percentage below
    myScore = round(score/len(terms)*100, 2)
    print(f"Your final score is: {myScore}%")

    handleScore(myScore, setName)

    showLeaderboard(setName)

def handleScore(score, setName):
    choice = input("Do you wish to log your score? (y/n) ")
    if choice.lower() in ['y', 'yes', 'sure']:
        name = input("What is your name? ")
        logScore(setName, name, score)

def selectSet(sets):
    # Turn each subpath into a list of parts
    path_map = {tableName: subpath.split("/") for _, tableName, subpath in sets}

    current_level = 0
    current_filter = list(path_map.items())

    while True:
        # Collect unique options at this depth
        options = []
        for _, parts in current_filter:
            if current_level < len(parts):
                if parts[current_level] not in options:
                    options.append(parts[current_level])

        # Show options
        print("\nChoose from:")
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt}")

        choice = input("Choice (number, or q to quit): ")
        if choice.lower() in ["q", "quit"]:
            return None

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                chosen = options[idx]

                # Narrow down to only paths that match this choice
                new_filter = []
                for tableName, parts in current_filter:
                    if current_level < len(parts) and parts[current_level] == chosen:
                        new_filter.append((tableName, parts))

                current_filter = new_filter
                current_level += 1

                # If every remaining path ends here → these are "files"
                if all(len(parts) == current_level for _, parts in current_filter):
                    # If multiple sets, list them so user picks one
                    if len(current_filter) > 1:
                        print("\nChoose a set:")
                        for i, (tableName, _) in enumerate(current_filter, start=1):
                            print(f"{i}. {tableName}")
                        while True:
                            file_choice = input("Which set (number)? ")
                            try:
                                idx = int(file_choice) - 1
                                if 0 <= idx < len(current_filter):
                                    return current_filter[idx][0]
                            except ValueError:
                                pass
                            print("Invalid choice, try again.")
                    else:
                        # Only one → auto-return
                        return current_filter[0][0]
            else:
                print("Number out of range, try again.")
        except ValueError:
            print("Not a number, try again.")

def showLeaderboard(setName):
    allScores = retrieveTopTen(setName)

    if allScores == None:
        print("No scores found")
        input()
        return

    print(f"\n{' '*17}Leaderboard")
    for score in allScores:
        print(f"{score[2]}{'-' * (30 - len(score[2]))}{score[3]}%")
    
    
    input("\nPress Enter to Continue")

def runThroughMissed(missedSets):
    allTerms = missedSets.copy()
    random.shuffle(allTerms)

    while len(allTerms) > 0:
        print(f"What is the answer for {allTerms[0][1]}? \n")
        guess = input()
        if guess.lower() in allTerms[0][2].lower().split(", "):
            print("Correct!\n")
            allTerms.remove(allTerms[0])
        else:
            print(f"Wrong. Correct answer was: {allTerms[0][2]}\n")

# ======= Exit function =======
def exit_program(): 
    global running
    running = False

# ======= Menu Actions =======
menu_actions = {
    '1': createSet,
    'create':createSet,
    'new':createSet,
    '2':openVocabSet,
    'open':openVocabSet,
    'open set':openVocabSet,
    'exit': exit_program,
    'q': exit_program,
    '3': exit_program
}

# ======= (drum roll) Main! =======
def main():
    global running
    print("Welcome to the reviewer!")
    running = True

    while running:
        print("""
Menu
1. Create New/Add to Set
2. Open Set
3. Exit""")
        choice = input("Choice: ").lower()
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Command not recognized.")

if __name__ == "__main__":
    main()

