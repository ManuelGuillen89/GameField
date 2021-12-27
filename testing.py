from commands_and__events_schema import *

class UnsatisfiedPolicy(BaseModel):
    message: str

class AppliedPolicy(BaseModel):
    isSatisfied: bool
    policyError: Optional[UnsatisfiedPolicy]

class GameFieldPolicies():
    def policies_list(): 
        return [method for method in dir(GameFieldPolicies) if method.startswith('__') is False]

    def dummy_policy(command: Command) -> AppliedPolicy:
        return AppliedPolicy(False, UnsatisfiedPolicy("Dummy Error Okay"))
    
    def dummy_policy_2(command: Command) -> AppliedPolicy:
        return AppliedPolicy(False, UnsatisfiedPolicy("Dummy Error Okay 2"))
    
    def test(someArg):
        print(someArg)
    


lp = GameFieldPolicies.policies_list()
for policy in lp:
    print (policy)

x = getattr(GameFieldPolicies, 'test')

x("asdfaafadfada")

j = {
    'isSatisfied': True, 
    'policyError': None
}
y = AppliedPolicy(**j)

print (y)