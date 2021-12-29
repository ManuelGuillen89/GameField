import json, sys
from gamefield_schema_layer import *
from gamefield_policy_layer import *


def lambda_handler(event, context):
    print(event)
    # ALL THE INPUT HERE IS ALREDY VALIDATED BY THE COMMAND VALIDATOR
    
    #parse command
    command = parse_validated_command(event)
    if (command == None):
        #TODO: rise error
        return {}
    
    #validate business rules here
    (isEverythingApproved, unsatisfiedPolicies) = PolicyProcessor.apply_policies_by_command_type(command)
    if (isEverythingApproved):
        #TODO: Create the Event
        #TODO: Persist the Event
        #TODO: Publish the Event to a SQS Topic 
        pass
    else:
        #TODO: Use the 'unsatisfiedPolicies' objet to build an error report
        #TODO: publish the error to an error handler
        pass
    return {}

def parse_validated_command(event) -> Optional[Command]:
    cmdPayload = get_command_payload_if_exist(event)
    cmdName = get_command_name_if_exist(event)
    listOfCommands = list(CommandName)
    for name in listOfCommands:
        if (name == cmdName):
            commandClass = getattr(sys.modules[__name__], name)
            return commandClass(**cmdPayload)
    return None
