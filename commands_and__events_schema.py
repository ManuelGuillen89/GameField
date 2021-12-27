from pydantic import BaseModel
from typing import Optional
from enum import Enum

##################### COMMON ENUMS AND TYPES ############################
class CommandName(str, Enum):
    CreateGameField = "CreateGameField"

class EventName(str, Enum):
    GameFieldCreated = "GameFieldCreated"
    GameFieldNameChanged = "GameFieldNameChanged"
    GameFieldMinMaxPlayersChanged = "GameFieldMinMaxPlayersChanged"
    GameFieldTypeChanged = "GameFieldTypeChanged"
    GameFieldStatusChanged = "GameFieldStatusChanged"
 
class GameFieldStatus(str, Enum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    DELETED = "DELETED"

class GameFieldType(str, Enum):
    FOOTBALL = "FOOTBALL"
    TENNIS = "TENNIS"
    BASKETBALL = "BASKETBALL"

class CommandStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"

############################### COMMANDS ##################################
class Command(BaseModel): 
    pass

class AggregateCommandInfo(BaseModel):
    id: str
    version: int

class CommandValidatorResponse(BaseModel):
    message: str
    status: CommandStatus
    errorAsJson: Optional[str]
    pushedCommandInfo: Optional[str]

class CreateGameField(Command):
    commandName: CommandName = CommandName.CreateGameField
    id: str
    fieldName: str
    fieldType: GameFieldType
    minPlayers: int
    maxPlayers: int
    status: GameFieldStatus

############################### EVENTS ##################################
class Event(BaseModel): 
    pass 

class AggregateEventInfo(BaseModel):
    id: str
    seqNumber: int

class GameFieldCreated(Event):
    eventName: EventName = EventName.GameFieldCreated
    fieldName: str
    fieldType: GameFieldType
    minPlayers: int
    maxPlayers: int
    status: GameFieldStatus
    aggregateEventInfo: AggregateEventInfo


######################### COMMON UTILITY FUNCTIONS ############################
def get_command_payload_if_exist(event) -> Optional[dict]:
    return event['arguments']['payload'] if 'payload' in event['arguments'] else None

def get_command_name_if_exist(event) -> Optional[dict]:
    return event['arguments']['commandName'] if 'commandName' in event['arguments'] else None

