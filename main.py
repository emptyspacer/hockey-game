import random, json, os

# this function is for clearing the console of text
def clearScreen():
  os.system("clear")


# this function is for updating the data variable seen below to keep it consistant with the teams.json file
def updateData():
  return json.load(open("teams.json"))


# this function is used to save a data (dict) object to the teams.json file
def dumpData(data):
  json.dump(data,open("teams.json","w"))


# this function pauses the program using an input
def pause():
  input("\nPress enter to continue ")


data = updateData()


# this function prints the main menu cover art
def coverArt():
  print(
    """
HOCKEY GAME PROJECT
 by joseph preston
    
  __O         O__
  \/\         /\/
  |\ \       / /|
 /  | \_ = _/ |  \ 
~   ~         ~   ~"""[1:]
  )
  # hockey stick ASCII art by llizard - https://www.asciiart.eu/sports-and-outdoors/ice-hockey


# this function is for printing the data about a team in a readable way for the user
def printTeamData(teamName):

  clearScreen()

  print("Name: ",teamName,"\n",sep="")

  teamData = data[teamName]

  for key in list(teamData.keys())[:-1]:
    print(key.title() + ":", teamData[key])

  players = teamData["players"]

  print("\nPlayers:")

  for player in players:
    for key in player.keys():
      print(" ", key.title() + ":", player[key])

    print()


# this function is for validating a name (player name, team name, etc. ) and will return a valid string. It takes in a required variable (message) and then optional variables for the minimum character length, what strings should not be allowed, and the error message if the string the user enters is in the filter list    
def validName(message, requiredLength = 7, filter=[], filterErrorMessage = ""):

  while True:
    name = input(message)

    if len(name) < requiredLength:
      print(f"Please enter a team name with {requiredLength} or more characters")

    elif not all(c.isalpha() for c in name.split()):
      print(f"Please do not include any special characters or integers in your team name (except spaces)")

    elif name[0] == " " or name[-1] == " ":
      print("Please make sure the first and last characters of the name are not spaces")

    elif name.count(" ") > 2:
      print("Please do not include more than 2 spaces")

    elif name in filter:
      print(filterErrorMessage)

    else:
      return name

      
# this function takes in a message, mininum and maximum and returns a valid integer that is >= min and <= max
def validInt(message, min, max):

  while True:
    userInput = input(message)

    if userInput.isnumeric():
      if int(userInput) <= max and int(userInput) >= min:
        return int(userInput)

      else:
        print(f"Please enter an integer between {min} and {max}")

    else:
      print("Please enter an integer")


# this function is for creating a team, and saving the team to the teams.json file. It returns the team name, which is used later on
def createTeam(data = data):

  teamName = validName(
    "Enter team name: ",
    6,
    list(data.keys()),
    "Please enter a name that has not been taken"
  )

  print("\nThe total of all your players attack and defence scores must equal 35. Attack score can be an integer between 0 and 10, and defence score can be an integer between 0 and 7")

  input("\nPress enter to continue ")

  players = []
  total = 0
  playerNames = []

  for i in range(6):
    clearScreen()

    print("Remaining points:",35-total)

    requiredLeft = 0

    player = {}

    print(f"\nPlayer #{i+1}")

    playerName = validName(
      "Please enter a player name: ",
      1,
      playerNames,
      "Please enter a unique player name for this team"
    )
    
    requiredLeft = 35-total-(17*(5-len(players)))

    if requiredLeft > 0:
      print("\nThis players stats must add to (at least)", requiredLeft,"\n")

    remainingPoints = 35 - total

    if remainingPoints > 0:
      if remainingPoints < 17:
        print("\nThis players stats cannot add to more than",remainingPoints,"\n")

      valid = False

      while not valid:
          if remainingPoints < 10:
              attack = validInt("Enter players's attack: ",0,remainingPoints)

          else:
              attack = validInt("Enter player's attack: ",0,10)

          if remainingPoints - attack > 0:
            if remainingPoints < 17:
              defence = validInt("Enter player's defence: ",0,remainingPoints-attack)

            else:
              defence = validInt("Enter player's defence: ",0,7)

          else:
              print("You have used all your remaining points on this players attack, their defence has been set to 0")
              defence = 0

          if defence + attack >= requiredLeft:
            valid = True

          else:
            print("\nPlease re-enter the values, see above message to see number of required points\n")

    else:
      print("Players attack and defence set to 0 as you have no points remaining")

      defence, attack  = 0, 0

    player = {
      "name":playerName,
      "attack":attack,
      "defence":defence
    }

    playerNames.append(playerName)

    players.append(player)

    total += attack
    total += defence

    print("Player saved")
    
    pause()

  readJsonFile = open("teams.json")

  data = updateData()

  readJsonFile.close()

  data[teamName] = {
    "wins":0,
    "losses":0,
    "draws":0,
    "goals scored":0,
    "goals conceded":0,
    "players":players
  }

  dumpData(data)

  return teamName


# this function is passed in the two team names, and is used to actually play the game
def playGame(team1Name, team2Name):

  data = updateData()

  team1 = data[team1Name]
  team2 = data[team2Name]

  team1Players = team1["players"]
  team2Players = team2["players"]

  goalkeepers = []
  attackers = []

  teams = [team1,team2]
  goalsScored = [0,0]

  for team in teams:
    clearScreen()

    print(f"Player {teams.index(team)+1} ({[team1Name,team2Name][teams.index(team)]})")

    players = team["players"][:]

    for i in range(6):
      player = players[i]

      print(f"{i+1}.) {player['name']}, attack = {player['attack']}, defence = {player['defence']}")

    selection = validInt("\nEnter number for player you want to play in goal: ",1,6)

    goalkeepers.append(players[selection-1])

    print(f"{players[selection-1]['name']} will be playing in goal")

    players.pop(selection-1)
    attackers.append(players)

    input("\nPress enter to continue ")

  penalties = 0

  while penalties < 5:
    clearScreen()

    print(f"Penalty {penalties+1}, Player {penalties%2+1}'s go")

    print(f"\n{team1Name}    {'*'*goalsScored[0]}{' '*(15-(goalsScored[0]+goalsScored[1]))}{'*'*goalsScored[1]}    {team2Name}\n")

    defendingGoalkeeper = goalkeepers[penalties%2-1]

    teamAttackers = attackers[penalties%2]

    for i in range(len(teamAttackers)):
      player = teamAttackers[i]

      print(f"{i+1}.) {player['name']}, attack = {player['attack']}, defence = {player['defence']}")

    selection = validInt("Enter number for attacker you want to take the penalty with: ",1,5)

    attacker = teamAttackers[selection-1]

    attackers[penalties%2].pop(selection-1)

    difference = attacker["attack"]-defendingGoalkeeper["defence"]

    difference += random.randint(1,4)

    if difference < 0:
      print(f"{defendingGoalkeeper['name']} saved the penalty!")

    else:
      print(f"{attacker['name']} scored!")

      goalsScored[penalties%2] += 1

    input("\nPress enter to continue ")

    penalties += 1

  data = updateData()

  teamNames = [team1Name,team2Name]

  for team in teamNames:
    data[team]["goals scored"] += goalsScored[teamNames.index(team)]

  for team in teamNames:
    data[team]["goals conceded"] += goalsScored[teamNames.index(team)-1]
  
  if goalsScored[0] == goalsScored[1]:
    print("The game was a draw")

    for team in teamNames:
      data[team]["draws"] += 1

  elif goalsScored[0] > goalsScored[1]:
    print(f"Player 1 ({team1Name}) won!")

    data[team1Name]["wins"] += 1
    data[team2Name]["losses"] += 1

  else:
    print(f"Player 2 ({team2Name})")

    data[team2Name]["wins"] += 1
    data[team1Name]["losses"] += 1

  data[team1Name]["players"] = team1Players
  data[team2Name]["players"] = team2Players

  dumpData(data)


# this function is used to display a menu that lets the user either create their own team or select a pre-existing team
def teamSelection(playerName, filter = ""):

  clearScreen()

  print(f"{playerName} = TEAM SELECTION MENU") 

  print("1. Select team\n2. Create team")

  choice = validInt("> ",1,2)

  if choice == 2:
    return createTeam()

  while True:
    clearScreen()

    teams = list(data.keys())

    try:
      teams.remove(filter)
    except:
      pass

    for i in range(len(teams)):
      print(f"{i+1}.) {teams[i]}")

    print(f"{len(teams)+1}.) Return to team selection menu")

    choice = validInt("> ",1,len(teams)+1)-1

    if choice == len(teams):
      return teamSelection(playerName, filter)

    team = teams[choice]

    print("\n1. Select this team\n2. View this teams stats")

    choice = validInt("> ",1,2)

    if choice == 1:
      return team

    os.system("clear")
    
    printTeamData(team)

    input("\nPress enter to return to team viewer menu ")
    
    
# this is the main menu function, and allows the user to decide whether or not to play the game. It lets the users enter their names, select their teams and then play the game using all the previously created functions  
def mainMenu():

  clearScreen()

  coverArt()

  print("1. play game (2 player)\n2. quit")
  choice = validInt("> ",1,2)

  if choice == 2:
    quit()

  clearScreen()

  playerName1 = validName(
    "Enter player name 1: ",
    7
  )

  playerName2 = validName(
    "Enter player name 2: ",
    7,
    [playerName1],
    "Please enter an unique player name"
  )

  players = [playerName1,playerName2]
  random.shuffle(players)

  print(f"\n{players[0]} is player 1 (playing first))")
  print(f"{players[1]} is player 2")

  teams = []
  teams.append(teamSelection(players[0]))
  teams.append(teamSelection(players[1],teams[0]))
    
  playGame(*teams)
  
mainMenu()