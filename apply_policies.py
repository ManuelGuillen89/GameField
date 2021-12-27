def appply_policies(command) -> Union[bool, List[str]]
    applicationResults: List[bool] = []
    errors: List[str] = []
    if(command.__commandName == CommandName.GameField):
        pass
    return all(applicationResults), errors