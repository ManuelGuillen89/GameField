if ! command -v <jq> &> /dev/null
then
    echo "<jq> IS NOT INSTALLED. INSTALL IT BEFORE RUN THIS SCRIPT"
    exit
fi

FUNCTION_ARN = "arn:aws:lambda:sa-east-1:176780489193:function:GameField_CommandProcessor"

echo "STARTED!" && 
echo "Generatin layer zip file" &&
cp ../gamefield_policies_for_commands_layer.py ./python && 
zip -r gamefield_policies_for_commands_layer.zip ./python && 
echo "Pushing layer to AWS" &&
aws lambda publish-layer-version --layer-name GameField_PoliciesForCommand_Python --description "Policies evaluation classes for GameField aggregate" --license-info "MIT" --zip-file fileb://gamefield_policies_for_commands_layer.zip --compatible-runtimes python3.9 > updated_layer.json && 
echo "Layer Pushed to AWS" && 
aws lambda get-function --function-name FUNCTION_ARN | jq .Configuration.Layers > layers_before_update_version.json && 
#TODO: 
echo "DONE!"

aws lambda get-function --function-name "arn:aws:lambda:sa-east-1:176780489193:function:GameField_CommandProcessor" | jq .Configuration.Layers