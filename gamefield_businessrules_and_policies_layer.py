from gamefield_schema_layer import Command
from typing import Optional
from pydantic import BaseModel
import sys

##########################################################################################
######################## DONT TOUCH THIS BLOCK ###########################################
def get_policy_evaluation_class(name):
    return getattr(sys.modules[__name__], "{}Policies".format(name)) 

class PoliciesContainer:
    def _policies_list(self):
        return [method for method in dir(self) if method.startswith('_') is False]
        
    def policies_class_by_command_name(commandName):
        return getattr(sys.modules[__name__], "{}Policies".format(commandName))

class UnsatisfiedPolicy(BaseModel):
    commandName: str
    message: str


class AppliedPolicy(BaseModel):
    isSatisfied: bool
    policyError: Optional[UnsatisfiedPolicy]
######################## END OF STATIC THE BLOCK #######################################
########################################################################################

###################### POLICIES EVALUETION CLASES ######################################
#TODO: PUT HERE THE POLICIES FOR EVERY ENABLED COMMAND

class CreateGameFieldPolicies(PoliciesContainer):
    def dummy_policy(command: Command) -> AppliedPolicy:
        unsatisfiedPolicie = UnsatisfiedPolicy(**{
            "message":"Dummy Error Okay",
            "commandName": command.commandName
            })
        appliedPolicyPayload = {
            'isSatisfied': False,
            'policyError': unsatisfiedPolicie
        }
        return AppliedPolicy(**appliedPolicyPayload)




