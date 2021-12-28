from gamefield_schema_layer import *
from typing import List, Union

class UnsatisfiedPolicy(BaseModel):
    message: str

class AppliedPolicy(BaseModel):
    isSatisfied: bool
    policyError: Optional[UnsatisfiedPolicy]

class GameFieldPolicies():
    def _policies_list(): 
        return [method for method in dir(GameFieldPolicies) if method.startswith('_') is False]

    def dummy_policy(command: Command) -> AppliedPolicy:
        unsatisfiedPolicie = UnsatisfiedPolicy(**{"message":"Dummy Error Okay"})
        appliedPolicyPayload = {
            'isSatisfied': False,
            'policyError': unsatisfiedPolicie
        }
        return AppliedPolicy(**appliedPolicyPayload)


class PolicyProcessor():

    def __apply_policy(
        policy,  # (Command) -> Union[bool, Optional[UnsatisfiedPolicy]]
        command: Command,
        appliedPolicies: List[AppliedPolicy],
    ) -> List[AppliedPolicy]:
        appliedPolicy = policy(command)
        appliedPolicies.append(appliedPolicy)
        return appliedPolicies

    def __applied_policies_for_command(command: Command, policiesNamesList: List[str]) -> Union[bool, Optional[List[UnsatisfiedPolicy]]]:
        appliedPolicies = []
        for policy in policiesNamesList:
            appliedPolices = PolicyProcessor.__apply_policy(getattr(GameFieldPolicies, policy), command, appliedPolicies)
        isEverythingApproved = all(list(map(lambda x: x.isSatisfied, appliedPolices)))
        if(isEverythingApproved):
            return True, None
        else:
            unsatisfiedPolicies = list(map(lambda x: x.policyError, appliedPolices))
            return False, unsatisfiedPolicies

    def apply_policies_by_command_type(command) -> Union[bool, Optional[List[UnsatisfiedPolicy]]]:
        if(command.commandName == CommandName.CreateGameField):
            return PolicyProcessor.__applied_policies_for_command(command, GameFieldPolicies._policies_list())
        elif(False): # TODO put other commands here
            print("pass") 
        print("pass")    
        return False, None


jsonCommand = {
    "commandName": "CreateGameField",
    "id": "1", 
    "fieldName": "gameField",
    "fieldType": "FOOTBALL",
    "minPlayers": 10, 
    "maxPlayers": 10, 
    "status": "ENABLED"
}

command = CreateGameField(**jsonCommand)
print(command)
(bool1, list1) = PolicyProcessor.apply_policies_by_command_type(command) 

print(bool1)
print(list1)