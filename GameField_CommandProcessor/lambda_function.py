import json, sys
from gamefield_policy_processor_layer import *


def lambda_handler(event, context):
    # ALL THE INPUT HERE IS ALREDY VALIDATED BY THE COMMAND VALIDATOR
    #parse command
    for record in event['Records']:
        payload = json.loads(record["body"])
        parsedCommand = parse_validated_command(payload)
        if (parsedCommand == None):
            print(">>>>>>>>>>>>>>>>>>> COMMAND NOT PARSED, EXITING.-")
            #TODO: rise and publish error
            return {}
        else: 
            process_validated_command(parsedCommand)
    return {}

def parse_validated_command(payload) -> Optional[Command]:
    cmdName = payload['commandName']
    listOfCommands = list(EnabledCommand)
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
        for commandName, eventName in COMMAND_EVENT_MAPPER.items():
            if (commandName == command.commandName):
                # Create the Event
                eventClass = getattr(sys.modules["gamefield_schema_layer"], eventName)
                newEvent = eventClass.create_from_command(command)
                print (">>>>>>>>>>")
                print (newEvent)
                print ("<<<<<<<<<<")
                #TODO: Persist the Event
                #TODO: Publish the Event to a SQS Topic 
    else:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> NOT EverythingApproved")
        #TODO: Use the 'unsatisfiedPolicies' objet to build an error report
        #TODO: publish the error to an error handler
        pass