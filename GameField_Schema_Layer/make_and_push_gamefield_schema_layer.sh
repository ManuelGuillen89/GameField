#echo "STARTED!" & cp ../gamefield_schema_layer.py ./python & zip -r gamefield_schema_layer.zip ./python & echo "DONE!"
echo "STARTED!" && 
echo "Generatin layer zip file" &&
cp ../gamefield_schema_layer.py ./python && 
zip -r gamefield_schema_layer.zip ./python && 
echo "Pushing layer to AWS" &&
aws lambda publish-layer-version --layer-name GameField_Schema_Python --description "Schema layer for GameField aggregate" --license-info "MIT" --zip-file fileb://gamefield_schema_layer.zip --compatible-runtimes python3.9 && 
echo "Layer Pushed to AWS" && 
echo "DONE!"