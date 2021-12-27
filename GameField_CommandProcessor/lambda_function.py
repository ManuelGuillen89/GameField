import json

def lambda_handler(event, context):
    print(event)
    #TODO: ALL THIS NEXT STEPS needs to be put in the CommandsProcessor Lambda
    
    #TODO: validate business rules here
    #TODO: If rules are okay, generate a new event (new aggregate)
    #TODO: Save the event to hte event store
    #TODO:  propagate the event through an SQS TOPIC
    return {}
