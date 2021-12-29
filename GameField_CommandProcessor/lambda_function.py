import json, sys
from gamefield_schema_layer import *
from gamefield_policy_layer import *


def lambda_handler(event, context):
    # ALL THE INPUT HERE IS ALREDY VALIDATED BY THE COMMAND VALIDATOR
    #parse command
    for record in event['Records']:
        payload = json.loads(record["body"])
        parsedCommand = parse_validated_command(payload)
        print(parsedCommand)
        if (parsedCommand == None):
            print(">>>>>>>>>>>>>>>>>>> COMMAND NOT PARSED, EXITING.-")
            #TODO: rise and publish error
            return {}
        else: 
            process_validated_command(parsedCommand)
    return {}

def parse_validated_command(payload) -> Optional[Command]:
    cmdName = payload['commandName']
    listOfCommands = list(CommandName)
    for name in listOfCommands:
        if (name == cmdName):
            commandClass = getattr(sys.modules[__name__], name)
            return commandClass(**payload)
    return None

def process_validated_command(command: Command): 
    #validate business rules here
    (isEverythingApproved, unsatisfiedPolicies) = PolicyProcessor.apply_policies_by_command_type(command)
    if (isEverythingApproved):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> EverythingApproved")
        #TODO: Create the Event
        #TODO: Persist the Event
        #TODO: Publish the Event to a SQS Topic 
        pass
    else:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> NOT EverythingApproved")
        #TODO: Use the 'unsatisfiedPolicies' objet to build an error report
        #TODO: publish the error to an error handler
        pass