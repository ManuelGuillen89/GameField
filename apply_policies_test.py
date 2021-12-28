from gamefield_schema_layer import *
from typing import List, Union
from gamefield_policy_layer import *

jsonCommand = {
    "commandName": "CreateGameField",
    "id": "1", 
    "fieldName": "gameField",
    "fieldType": "FOOTBALL",
    "minPlayers": 10, 
    "maxPlayers": 10, 
    "status": "ENABLED"
}

command = CreateGameField(**jsonCommand)
print(command)
(bool1, list1) = PolicyProcessor.apply_policies_by_command_type(command) 

print(bool1)
print(list1)