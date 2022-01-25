import random, json, os

file = open("teams.json")
data = json.load(file)
file.close()

def printTeamData(teamName):
  print(teamName,"\n")
  teamData = data[teamName]
  for key in list(teamData.keys())[:-1]:
    print(key + ":", teamData[key])
  players = teamData["players"]
  print("\nPlayers:")
  for player in players:
    for key in player.keys():
      print(" ", key + ":", player[key])
    print()

    
def validName(message,requiredLength=20,filter=[],filterErrorMessage=""):
  while True:
    name = input(message)
    if len(name) < requiredLength:
      print(f"Please enter a team name with {requiredLength} or more characters")
    elif not all(c.isalnum() for c in name):
      print(f"Please do not include any special characters in your team name")
    elif name in filter:
      print(filterErrorMessage)
    else:
      return name

      

def validInt(message,min,max):
  while True:
    userInput = input(message)
    if userInput.isnumeric():
      if int(userInput) <= max and int(userInput) >= min:
        return int(userInput)
      else:
        print(f"Please enter an integer between {min} and {max}")
    else:
      print("Please enter an integer")

def createTeam(data=data):
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
    os.system("clear")
    print("Remaining points:",35-total)
    min = 0
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
      min = requiredLeft
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
          if defence + attack >= min:
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
    input("Player saved.\n\nPress enter to continue ")
  readJsonFile = open("teams.json")
  data = json.load(readJsonFile)
  readJsonFile.close()
  data[teamName] = {
    "wins":0,
    "losses":0,
    "goals scored":0,
    "goals conceded":0,
    "players":players
  }
  writeToFile = open("teams.json","w")
  json.dump(data,writeToFile)
  writeToFile.close()



def playGame(team1Name,team2Name):
  team1 = data[team1Name]
  team2 = data[team2Name]
  team1players = team1["players"]
  team2players = team2["players"]
  goalkeepers = []
  attackers = []
  teams = [team1,team2]
  goalsScored = [0,0]
  for team in teams:
    os.system("clear")
    print(f"Player {teams.index(team)+1} ({[team1Name,team2Name][teams.index(team)]})")
    players = team["players"]
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
    os.system("clear")
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

  

  data[team1Name]["goals conceded"] += goalsScored[1]
  data[team2Name]["goals conceded"] += goalsScored[0]
  
  if goalsScored[0] == goalsScored[1]:
    print("The game was a draw")
    data[team1Name]["draws"] += 1
    data[team2Name]["draws"] += 1
  elif goalsScored[0] > goalsScored[1]:
    print(f"Player 1 ({team1Name}) won!")
    data[team1Name]["wins"] += 1
    data[team2Name]["losses"] += 1
  else:
    print(f"Player 2 ({team2Name})")
    data[team2Name]["wins"] += 1
    data[team1Name]["losses"] += 1

  writeToFile = open("teams.json","w")
  json.dump(data,writeToFile)
  writeToFile.close()

  
playGame("The Red Lions","ejrejrjejr")