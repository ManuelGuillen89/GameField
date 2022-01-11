from gamefield_schema_layer import *
from typing import List, Union
import sys

##########################################################################################
######################## DEFINITIONS AND CONTROLLERS #####################################

class UnsatisfiedPolicy(BaseModel):
    commandName: str
    message: str


class AppliedPolicy(BaseModel):
    isSatisfied: bool
    policyError: Optional[UnsatisfiedPolicy]


class PoliciesContainer:
    def _policies_list(self):
        return [method for method in dir(self) if method.startswith('_') is False]

    def policies_class_by_command_name(commandName):
        return getattr(sys.modules[__name__], "{}Policies".format(commandName))


class PolicyProcessor():

    def __apply_policy(
        policy,  # (command: Command) -> AppliedPolicy
        command: Command,
        appliedPolicies: List[AppliedPolicy],
    ) -> List[AppliedPolicy]:
        appliedPolicy = policy(command)
        appliedPolicies.append(appliedPolicy)
        return appliedPolicies

    def __applied_policies_for_command(command: Command, policiesNamesList: List[str]) -> Union[bool, Optional[List[UnsatisfiedPolicy]]]:
        appliedPolicies = []
        for policy in policiesNamesList:
            appliedPolices = PolicyProcessor.__apply_policy(
                getattr(PolicyProcessor.policies_classname_by_command(command.commandName), policy), command, appliedPolicies)
        isEverythingApproved = all(
            list(map(lambda x: x.isSatisfied, appliedPolices)))
        if(isEverythingApproved):
            return True, None
        else:
            unsatisfiedPolicies = list(
                map(lambda x: x.policyError, appliedPolices))
            return False, unsatisfiedPolicies

    def apply_policies_by_command_type(command: Command) -> Union[bool, Optional[List[UnsatisfiedPolicy]]]:
        listOfCommands = list(EnabledCommand)
        for name in listOfCommands:
            if (name == command.commandName):  # TODO insecure code here.. well, everywhere
                policiesClass = getattr(
                    sys.modules[__name__], "{}Policies".format(name))
                if(policiesClass == None):
                    print("ERROR: Policies not registered for this command: {}".format(
                        command.commandName))
                    return False, [UnsatisfiedPolicy(**{
                        "message": "ERROR: Policies not registered for this command",
                        "commandName": command.commandName
                    })]
                return PolicyProcessor.__applied_policies_for_command(command, policiesClass._policies_list(policiesClass))
        print("ERROR: Policies not processed for command: {}".format(
            command.commandName))
        return False, None

######################## END OF DEFINITIONS AND CONTROLLERS BLOCK ######################################
########################################################################################################

####################### POLICIES EVALUETION CLASES #####################################################
# TODO: PUT HERE THE POLICIES FOR EVERY ENABLED COMMAND

class CreateGameFieldPolicies(PoliciesContainer):
    def dummy_policy(command: Command) -> AppliedPolicy:
        unsatisfiedPolicie = UnsatisfiedPolicy(**{
            "message": "Dummy Error Okay",
            "commandName": command.commandName
        })
        appliedPolicyPayload = {
            'isSatisfied': False,
            'policyError': unsatisfiedPolicie
        }
        return AppliedPolicy(**appliedPolicyPayload)
