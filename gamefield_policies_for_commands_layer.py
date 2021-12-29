from gamefield_policy_layer import *

class PoliciesContainer:
    def _policies_list(self):
        return [method for method in dir(self) if method.startswith('_') is False]
        
    def policies_class_by_command_name(commandName):
        return getattr(sys.modules[__name__], "{}Policies".format(commandName))


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