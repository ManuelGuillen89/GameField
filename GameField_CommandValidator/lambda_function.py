from gamefield_schema_layer import *
import json, uuid, boto3, sys
from typing import Union
from pydantic import ValidationError

def lambda_handler(event, context):
    #check if the payload is in
    if(get_command_payload_if_exist(event) == None):
        return CommandValidatorResponse(
            message='ERROR: Command payload doesnt exist', 
            status=CommandStatus.INVALID).dict()
    #try to parse the command, reject the command if it is invalid
    (parsedCommand, errorAsJson) = parse_command(event)
    if (errorAsJson != None):
        return CommandValidatorResponse(
            message='ERROR: Validation error', 
            errorAsJson = errorAsJson, 
            status = CommandStatus.INVALID,
            ).dict()
    elif (parsedCommand == None): 
        #Return a CommandHanlderResponese with an error message.
        return CommandValidatorResponse(
            message = 'ERROR: Command not handled by this aggregate', 
            status = CommandStatus.INVALID, 
            ).dict()
    #SEND THE VALIDATED COMMAND TO THE FIFO Commands SQS 
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='GameField_CommandHandler_Queue.fifo')
    queueResponse = queue.send_message(
        MessageBody=parsedCommand.json(), 
        MessageGroupId=parsedCommand.id)
    #return the CommandValidatorResponse objet to the caller (Graphql mutation)
    return CommandValidatorResponse(
        message = 'OK: Command validated and pushed', 
        status = CommandStatus.VALID, 
        pushedCommandInfo = json.dumps(queueResponse)
        ).dict()

def parse_command(event) -> Union[Optional[Command], Optional[str]]:
    payload = get_command_payload_if_exist(event)
    commandName = get_command_name_from_graphql_mutation_if_exist(event)
    if (commandName == None or payload == None):
        return None, None
    elif (commandName not in list(EnabledCommand)):
        return None, None
    parsedCommand = None
    errorAsJson = None
    try:
        listOfCommands = list(EnabledCommand)
        for name in listOfCommands:
            if (name == commandName):
                commandClass = getattr(sys.modules[__name__], name)
                parsedCommand = commandClass(**payload)
#TODO: Enable this...
        #if(not is_valid_uuid(parsedCommand.id)):
        #    raise ValueError("INVALID UUID")
    except ValidationError as e:
        print(e.json())
        errorAsJson = e.json()
    except ValueError as e:
        print(e)
        errorAsJson = e.json() #"Value Error" #TODO: corregir
    return parsedCommand, errorAsJson

def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False