from gamefield_policy_layer import *
from typing import List, Union
import sys 

##########################################################################################
##########################################################################################
####################### POLICY PROCESSOR CLASS ###########################################


class PolicyProcessor:
    def __apply_policy(
        policy,  # (command: Command) -> AppliedPolicy
        command: Command,
        appliedPolicies: List[AppliedPolicy],
    ) -> List[AppliedPolicy]:
        appliedPolicy = policy(command)
        appliedPolicies.append(appliedPolicy)
        return appliedPolicies

    def __applied_policies_for_command(
        command: Command,
        policyClass: PoliciesContainer,
    ) -> Union[bool, Optional[List[UnsatisfiedPolicy]]]:
        policiesNamesList = policyClass._policies_list(policyClass)
        appliedPolicies = []
        for policy in policiesNamesList:
            appliedPolices = PolicyProcessor.__apply_policy(
                getattr(policyClass, policy),
                command,
                appliedPolicies,
            )
        
        #the dumbest man improvement .... 
        isEverythingApproved = all(list(map(lambda x: x.isSatisfied, appliedPolices)))
        unsatisfiedPolicies = list(map(lambda x: x.policyError, appliedPolices))
        return isEverythingApproved, unsatisfiedPolicies


    def apply_policies_by_command_type(
        command: Command,
    ) -> Union[bool, Optional[List[UnsatisfiedPolicy]]]:
        listOfCommands = list(EnabledCommand)
        for name in listOfCommands:
            if (
                name == command.commandName
            ):  # TODO insecure code here.. well, everywhere
                policyClass = getattr(
                    sys.modules["gamefield_policy_layer"], "{}Policies".format(name)
                )
                if policyClass == None:
                    print(
                        "ERROR: Policies not registered for this command: {}".format(
                            command.commandName
                        )
                    )
                    return False, [
                        UnsatisfiedPolicy(
                            **{
                                "message": "ERROR: Policies not registered for this command",
                                "commandName": command.commandName,
                            }
                        )
                    ]
                return PolicyProcessor.__applied_policies_for_command(
                    command, policyClass
                )
        print(
            "ERROR: Policies not processed for command: {}".format(command.commandName)
        )
        return False, None
