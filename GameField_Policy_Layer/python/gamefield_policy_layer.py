from gamefield_schema_layer import *

#########################################################################################
# TODO: Dividir este archivo , convertirlo en 2 capas distintas
#########################################################################################

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
        return [method for method in dir(self) if method.startswith("_") is False]


######################## END OF DEFINITIONS AND CONTROLLERS BLOCK ######################
########################################################################################

####################### POLICIES EVALUETION CLASESS ####################################

# TODO: LINK HERE THE POLICIES FOR EVERY ENABLED COMMAND


class CreateGameFieldPolicies(PoliciesContainer):
    def dummy_policy(command: Command) -> AppliedPolicy:
        return GameFieldPolicies.a_dummy_policy(command)


# TODO: PUT HERE THE EVALUATION FOR EVERY POLICY


class GameFieldPolicies:
    def a_dummy_policy(command: Command) -> AppliedPolicy:
        unsatisfiedPolicie = UnsatisfiedPolicy(
            **{"message": "Dummy Error Okay", "commandName": command.commandName}
        )
        appliedPolicyPayload = {"isSatisfied": False, "policyError": unsatisfiedPolicie}
        return AppliedPolicy(**appliedPolicyPayload)
