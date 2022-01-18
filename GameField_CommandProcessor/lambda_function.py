import json, sys
from warnings import catch_warnings
from gamefield_policy_processor_layer import *
import itertools
import boto3



def lambda_handler(event, context):
    # ALL THE INPUT HERE IS ALREDY VALIDATED BY THE COMMAND VALIDATOR
    # parse command
    for record in event["Records"]:
        payload = json.loads(record["body"])
        parsedCommand = parse_validated_command(payload)
        if parsedCommand == None:
            print(">>>>>>>>>>>>>>>>>>> COMMAND NOT PARSED, EXITING.-")
            # TODO: rise and publish error
        else:
            process_validated_command(parsedCommand)
    return {}


def parse_validated_command(payload: dict) -> Optional[Command]:
    cmdName = payload["commandName"]
    match = itertools.takewhile(lambda cName: cmdName == cName, list(EnabledCommand))
    if not match:
        return None 
    else:
        commandClass = getattr(sys.modules[__name__], match[0])
        return commandClass(**payload)
            

def process_validated_command(command: Command):
    # validate business rules here
    (
        isEverythingApproved,
        unsatisfiedPolicies,
    ) = PolicyProcessor.apply_policies_by_command_type(command)
    if isEverythingApproved:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> EverythingApproved")
        # Get the service resource.
        dynamodb = boto3.resource("dynamodb")
        eventStoreTable = dynamodb.Table("GameField_EventStrore")
        
        # Remember: One command can generate more than one event at same time
        for commandName, eventName in COMMAND_EVENT_MAPPER.items():
            if commandName == command.commandName:
                # Create the Event
                eventClass = getattr(sys.modules["gamefield_schema_layer"], eventName)
                newEvent = eventClass.create_from_command(command)
                newEventAsDict = json.loads(newEvent.json())
                # Persist the Event
                try:
                    eventStoreTable.put_item(Item=newEventAsDict)
                except Exception as e:
                    # TODO: Derivar error a sistema de notificacion de errores
                    print(e)                   
                
                print(" Stored ! <<<<<<<<<<")
                # TODO: Publish the Event to a SNS Topic
                
    else:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> NOT EverythingApproved")
        # TODO: Use the 'unsatisfiedPolicies' objet to build an error report
        # TODO: publish the error to an error handler
        pass
    print(">>>>>>>>>> {} <<<<<<<<<<<".format("END OK: process_validated_command"))





