echo "STARTED!" && 
echo "Generatin layer zip file" &&
cp ../gamefield_policy_layer.py ./python && 
zip -r gamefield_policy_layer.zip ./python && 
echo "Pushing layer to AWS" &&
aws lambda publish-layer-version --layer-name GameField_Policy_Python --description "Policy layer for GameField aggregate" --license-info "MIT" --zip-file fileb://gamefield_policy_layer.zip --compatible-runtimes python3.9 && 
echo "Layer Pushed to AWS" && 
echo "DONE!"