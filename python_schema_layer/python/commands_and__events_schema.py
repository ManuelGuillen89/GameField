from pydantic import BaseModel, ValidationError
from typing import Union, Optional
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
    validationError: Optional[str]
    pushedCommandInfo: Optional[str]

class CreateGameField(Command):
    __commandName: CommandName = CommandName.CreateGameField
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
    __eventName: EventName = EventName.GameFieldCreated
    fieldName: str
    fieldType: GameFieldType
    minPlayers: int
    maxPlayers: int
    status: GameFieldStatus
    aggregateEventInfo: AggregateEventInfo
    

class GameFieldNameChanged(Event):
    __eventName: EventName = EventName.GameFieldNameChanged
    fieldName: str
    eventCommonInfo: AggregateEventInfo
    

class GameFieldMinMaxPlayersChanged(Event):
    __eventName: EventName = EventName.GameFieldMinMaxPlayersChanged
    minPlayers: int
    maxPlayers: int
    eventCommonInfo: AggregateEventInfo

class GameFieldTypeChanged(Event):
    __eventName: EventName = EventName.GameFieldTypeChanged
    fieldType: GameFieldType
    eventCommonInfo: AggregateEventInfo
    

class GameFieldStatusChanged(Event):
    __eventName: EventName = EventName.GameFieldStatusChanged
    status: GameFieldStatus
    eventCommonInfo: AggregateEventInfo


######################### COMMON UTILITY FUNCTIONS ############################
def get_event_input_if_exist(event) -> Optional[dict]:
    return event['arguments']['input']

