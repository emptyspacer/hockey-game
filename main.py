import random, json, os, time


# hockey stick main menu art and intro screen art by llizard
# -> https://www.asciiart.eu/sports-and-outdoors/ice-hockey


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


# this function is for printing the intro screen animation
def introScreen():

  final = [
    "              _                                  ",
    "                \                                ",
    "                 \          \                    ",
    "  ==0        ==0_/\     ==0_/\                   ",
    "   /\         /\_        /\   \_       _==0_/\   ",
    "  |\ \        |\        |\ \          |\ \_   \  ",
    " /  | \_     /  |      /  |          / /       \_",
    "--  --      --  --    --  --        -- -         "
  ]

  # indexing each line in final to create 4 stages
  stages = [
    [line[:12] for line in final],
    [line[:22] for line in final],
    [line[:36] for line in final],
    final
  ]

  # going through each stage, clearing the screen and then printing each line of the stage
  for stage in stages:
    clearScreen()

    for line in stage:
      print(line)

    time.sleep(1.1)

  pause()

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

  # repeating code 6 times (for the 6 team players)
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
    remainingPoints = 35 - total

    minimum = False
    maximum = False

    # checking if the current player requires a certain number of minimum points (so any later players stats are valid)
    if requiredLeft > 0:
      minimum = True

    # checking if the required points for this player is 17 (the maximum), and if it is setting attack and defence to 10 and 7
    if requiredLeft == 17:
      print("This player's stats must add to exactly 17, so their attack and defence have been set to 10 and 7 respectively")
      attack = 10
      defence = 7
    
    elif remainingPoints > 0:
      if remainingPoints < 17:
        maximum = True

      # displaying appropriate warning message (if any is required)

      if minimum and maximum:
        print(f"This players stats must add to exactly {requiredLeft}")

      elif minimum:
        print(f"This players stats must add to (at least) {requiredLeft}")

      elif maximum: 
        print(f"This players stats cannot add to more than {remainingPoints}")


      if remainingPoints < 10:
          attack = validInt("Enter players's attack: ",0,remainingPoints)

      elif requiredLeft > 7:
          attack = validInt("Enter player's attack: ",requiredLeft-7,10)

      else:
          attack = validInt("Enter player's attack: ",0,10)


      if remainingPoints - attack > 0:
        # checking if after the attack is added to the total, there needs to be a limit on the number of defence points the player can have
        if remainingPoints - attack < 7:
          defence = validInt("Enter player's defence: ",0,remainingPoints-attack)

        elif attack < requiredLeft:
          defence = validInt("Enter player's defence: ",requiredLeft-attack,7)
        
        else:
          defence = validInt("Enter player's defence: ",0,7)

      # if the player has no more points to spend on this players attack, set attack to 0 and display message
      else:
          print("You have used all your remaining points on this players attack, their defence has been set to 0")
          defence = 0

    # if there are remaining points, setting player's attack and defence both to 0 
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

  # creating the team in the dict
  data[teamName] = {
    "wins":0,
    "losses":0,
    "draws":0,
    "goals scored":0,
    "goals conceded":0,
    "players":players
  }

  # saving the team to the teams.json file by dumping the data variable
  dumpData(data)

  return teamName


# this function is passed in the two team names, and is used to actually play the game
def playGame(team1Name, team2Name):
  
  # updating the data variable so that it includes any newly created teams
  data = updateData()

  team1 = data[team1Name]
  team2 = data[team2Name]

  team1Players = team1["players"]
  team2Players = team2["players"]

  goalkeepers = []
  attackers = []

  teams = [team1,team2]
  goalsScored = [0,0]

  # getting each user to select a player to play in goal
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


  for penalties in range(5):
    clearScreen()

    print(f"Penalty {penalties+1}, Player {penalties%2+1}'s go")

    print(f"\n{team1Name}    {'*'*goalsScored[0]}{' '*(15-(goalsScored[0]+goalsScored[1]))}{'*'*goalsScored[1]}    {team2Name}\n")

    defendingGoalkeeper = goalkeepers[penalties%2-1]

    teamAttackers = attackers[penalties%2]

    # printing a list of available attackers for the user to choose from
    for i in range(len(teamAttackers)):
      player = teamAttackers[i]

      print(f"{i+1}.) {player['name']}, attack = {player['attack']}, defence = {player['defence']}")

    selection = validInt("Enter number for attacker you want to take the penalty with: ",1,5)

    attacker = teamAttackers[selection-1]

    attackers[penalties%2].pop(selection-1)

    # getting difference between attacker and other team's goalkeeper
    difference = attacker["attack"]-defendingGoalkeeper["defence"]

    # adding a random integer between 1 and 4 to the difference
    difference += random.randint(1,4)

    # checking if the penalty has been scored or not and updating the goalsScored list accordingly

    if difference < 0:
      print(f"{defendingGoalkeeper['name']} saved the penalty!")

    else:
      print(f"{attacker['name']} scored!")

      goalsScored[penalties%2] += 1

    input("\nPress enter to continue ")

  data = updateData()

  teamNames = [team1Name,team2Name]

  # editing data variable to add match data

  for team in teamNames:
    data[team]["goals scored"] += goalsScored[teamNames.index(team)]

  for team in teamNames:
    data[team]["goals conceded"] += goalsScored[teamNames.index(team)-1]
  
  if goalsScored[0] == goalsScored[1]:
    print("The game was a draw")

    for team in teamNames:
      data[team]["draws"] += 1

  # checking which team has won and updating data accordingly

  elif goalsScored[0] > goalsScored[1]:
    print(f"Player 1 ({team1Name}) won!")

    data[team1Name]["wins"] += 1
    data[team2Name]["losses"] += 1

  else:
    print(f"Player 2 ({team2Name})")

    data[team2Name]["wins"] += 1
    data[team1Name]["losses"] += 1

  # resetting the players lists of each team so that the changes made during the match to make sure the same attacker is not selected twice are not saved
  data[team1Name]["players"] = team1Players
  data[team2Name]["players"] = team2Players

  # saving the new data object to the teams.json file
  dumpData(data)


# this function is used to display a menu that lets the user either create their own team or select a pre-existing team
def teamSelection(playerName, filter = ""):

  clearScreen()

  print(f"{playerName} = TEAM SELECTION MENU") 

  # checking if user wants to view team or create team

  print("1. Select team\n2. Create team")

  choice = validInt("> ",1,2)

  if choice == 2:
    return createTeam()

  while True:
    clearScreen()

    teams = list(data.keys())

    # making sure the team selected by the previous user (if there has been one) is not selected by current user
    try:
      teams.remove(filter)
    except:
      pass

    # printing out list of teams
    for i in range(len(teams)):
      print(f"{i+1}.) {teams[i]}")

    # giving user option to return to main team selection menu in case they have changed their mind once seeing the teams and want to create their own
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
  
  
introScreen()

while True:
  mainMenu()