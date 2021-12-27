from commands_and__events_schema import *
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

def apply_policy(
    policy,  # (Command) -> Union[bool, Optional[UnsatisfiedPolicy]]
    command: Command,
    appliedPolicies: List[AppliedPolicy],
) -> List[AppliedPolicy]:
    appliedPolicy = policy(command)
    appliedPolicies.append(appliedPolicy)
    return appliedPolicies

def policies_for_CreateGameField_command(command: CreateGameField) -> Union[bool, Optional[List[UnsatisfiedPolicy]]]:
    appliedPolicies = []
    for policy in GameFieldPolicies._policies_list():
        appliedPolices = apply_policy(getattr(GameFieldPolicies, policy), command, appliedPolicies)
    isEverythingApproved = all(list(map(lambda x: x.isSatisfied, appliedPolices)))
    if(isEverythingApproved):
        return True, None
    else:
        unsatisfiedPolicies = list(map(lambda x: x.policyError, appliedPolices))
        return False, unsatisfiedPolicies

def apply_policies_by_command_type(command) -> Union[bool, Optional[List[UnsatisfiedPolicy]]]:
    if(command.commandName == CommandName.CreateGameField):
        return policies_for_CreateGameField_command(command)
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
(bool1, list1) = apply_policies_by_command_type(command) 

print(bool1)
print(list1)