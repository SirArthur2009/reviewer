import random
import sqlite3
import time

FILENAME = "C:/Users/levig/OneDrive/Documents/Coding/Python/Complex_Programs/reviewer/vocaber.db"

# ======= FOR LOGGING AND RETRIEVING SCORES INTO A DATABASE =======
def logScore(setName: str, person: str, score: int, time: float):
    """Logs a score into the database"""
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, setName TEXT, person TEXT, score INTEGER, time FLOAT)")

    c.execute("""INSERT INTO scores (setName, person, score, time) VALUES (?, ?, ?, ?)""", (setName, person, score, time))

    conn.commit()
    conn.close()    

def retrieveTopTen(setName):
    """Pulls the top ten scores from the database"""
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, setName TEXT, person TEXT, score INTEGER, time FLOAT)")

    #First order by score and then order by time, basically whoever with the high score and lowest time wins
    c.execute("SELECT * FROM scores WHERE setName = ? ORDER BY score DESC, time ASC LIMIT 10", (setName,))

    topScores = c.fetchall() or None

    conn.close()

    return topScores

# ======= FOR CREATING SETS AND ADDING TERMS =======
def addTable(name, path):
    """Adds a table to the database with the name and path"""
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
    """GUI For creating a set"""
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
    """For adding terms to a table in the database (GUI)"""
    while True:
        print("\nq to quit\n")
        term = input("What's the term? \n")
        answers = input("What's the answer? \n")

        if term.lower() in ['q', 'quit'] or answers.lower() in ['q', 'quit']:
            break

        addTermToTable(term, answers, table)

def addTermToTable(term, answers, table):
    """Adds a single term to the database"""
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
    """Retrieves the names of all the sets"""
    conn = sqlite3.connect(FILENAME)
    c = conn.cursor()

    c.execute("SELECT * FROM allTables")

    tables = c.fetchall()

    conn.close()

    return tables

def getTermsFromSet(set):
    """Gets all the terms from a single set"""
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
    """Basic GUI for running thorugh the terms"""

    score = 0 # Set score
    missedTerms = [] # Start a missedTerms array
    sets = getAllSets() # Grab the name of all the sets available
    compiled = False

    # If there's no sets, print and return
    if not sets:
        print("No sets available. Create one first.")
        return

    setName = selectSet(sets)  # Select a set from the available sets
    terms = getTermsFromSet(setName) #Get all the terms from the set selected
    if input("Do you wish to compile 2 sets? (y/n)").lower() == "y":
        setName2 = selectSet(sets)
        terms2 = getTermsFromSet(setName2)
        # Only combine if both are valid lists
        if isinstance(terms, list) and isinstance(terms2, list):
            terms += terms2
            compiled = True
        else:
            print("Error: One or both sets could not be loaded.")
            return

    # If the terms are not in list form, print and return
    if not isinstance(terms, list) or not terms:
        print(terms)
        return

    startTime = time.time()
    score, missedTerms = runThrough(terms) # Run through terms
    endtime = time.time()
    totalTime = endtime - startTime
    
    # Double check for missed turns and give option to run through missed ones only
    if not missedTerms:
        print("No missed terms.")
    else:
        choice = input("Do you want to run through the missed terms? (y/n) ")
        if choice.lower() in ['y', 'yes', 'sure']:
            runThrough(missedTerms)

    # Get score and ask if wanted saved
    myScore = round(score/len(terms)*100, 2)
    print(f"Your final score is: {myScore}%")
    
    if not compiled:
        handleScore(myScore, setName, totalTime)

    showLeaderboard(setName) # Show leaderboard

def runThrough(terms):
    """GUI for actually running through the terms"""
    missedTerms = []
    score = 0
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
    
    return score, missedTerms

def handleScore(score, setName, time):
    """Asks for and logs score"""
    choice = input("Do you wish to log your score? (y/n) ")
    if choice.lower() in ['y', 'yes', 'sure']:
        name = input("What is your name? ")
        logScore(setName, name, score, time)
    
def selectSet(sets):
    """Select set function, it was partially AI generated"""
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
    """Display leaderboard"""
    allScores = retrieveTopTen(setName)

    if allScores == None:
        print("No scores found")
        input()
        return

    print(f"\n{' '*17}Leaderboard")
    for score in allScores:
        print(f"{score[2]}; Time: {score[4]:.2f}{'-' * (50 - (len(score[2])+len(str(round(score[4], 2)))+8))}{score[3]}%")
    
    
    input("\nPress Enter to Continue")

def handleLeaderboard():
    showLeaderboard(setName=selectSet(getAllSets()))
# ======= Exit function =======
def exit_program(): 
    """Exit"""
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
    '3':handleLeaderboard,
    'handle':handleLeaderboard,
    'scores':handleLeaderboard,
    'exit': exit_program,
    'q': exit_program,
    '4': exit_program
}

# ======= (drum roll) Main! =======
def main():
    """Let's get rolling!"""
    global running
    print("Welcome to the reviewer!")
    running = True

    while running:
        print("""
Menu
1. Create New/Add to Set
2. Open Sets
3. See scores for a set
4. Exit""")
        choice = input("Choice: ").lower()
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Command not recognized.")

if __name__ == "__main__":
    main()

