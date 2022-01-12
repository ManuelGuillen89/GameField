import json, sys
from warnings import catch_warnings
from gamefield_policy_processor_layer import *
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
            return {}
        else:
            process_validated_command(parsedCommand)
    return {}


def parse_validated_command(payload) -> Optional[Command]:
    cmdName = payload["commandName"]
    listOfCommands = list(EnabledCommand)
    for name in listOfCommands:
        if name == cmdName:
            commandClass = getattr(sys.modules[__name__], name)
            return commandClass(**payload)
    return None

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
        eventStore = dynamodb.Table("GameField_EventStrore")
        for commandName, eventName in COMMAND_EVENT_MAPPER.items():
            if commandName == command.commandName:
                # Create the Event
                eventClass = getattr(sys.modules["gamefield_schema_layer"], eventName)
                newEventAsDict = eventClass.create_as_dict_from_command(command)
                # Persist the Event
                try:
                    eventStore.put_item(Item=newEventAsDict, ConditionExpression="attribute_not_exists(id)")
                except Exception as e:
                    print(e)                   
              
                print(" Stored ! <<<<<<<<<<")
                # TODO: Publish the Event to a SQS Topic
                break
    else:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> NOT EverythingApproved")
        # TODO: Use the 'unsatisfiedPolicies' objet to build an error report
        # TODO: publish the error to an error handler
        pass
    print(">>>>>>>>>> {} <<<<<<<<<<<".format("END OK: process_validated_command"))
