echo "STARTED!" && 
echo "Generatin layer zip file" && 
zip -r gamefield_common_layer.zip ./python && 
echo "Pushing layer to AWS" &&
aws lambda publish-layer-version --layer-name GameField_Common_Python --description "Common layer for GameField aggregate" --license-info "MIT" --zip-file fileb://gamefield_common_layer.zip --compatible-runtimes python3.9 && 
echo "Layer Pushed to AWS" && 
echo "DONE!"