layerName="GameField_Common_Python"
fileName="gamefield_common_layer"
layerDescription="Common Libraries Layer for GameField aggregate"
updatedLayerFile="./tmp/updated_layer.json"
tempLayersFile="./tmp/temp_layers.json"

echo "STARTED!" && 
echo "Generatin layer zip file" &&
zip -r ${fileName}.zip ./python && 
echo "Pushing layer to AWS" &&
aws lambda publish-layer-version --layer-name ${layerName} --description "$layerDescription" --license-info "MIT" --zip-file fileb://${fileName}.zip --compatible-runtimes python3.9 > $updatedLayerFile && 
echo "Layer Pushed to AWS" && 

for i in "GameField_CommandProcessor" "GameField_EventHandler_StateProjector" "GameField_CommandValidator" 
do
    echo "Updating layer version on consumer function configuration:  $i ..." || break 
    aws lambda get-function --function-name $i | jq .Configuration.Layers | jq 'map({"Arn": .Arn})' > $tempLayersFile || break 
    unchangedLayers=$(cat $tempLayersFile | jq --arg layerName "$layerName" '[.[] | select(.Arn | contains($layerName) | not )]' | jq -r 'map(.Arn) | join(" ")') || break
    changedLayer=$(cat $updatedLayerFile | jq .LayerVersionArn | tr -d '"') || break
    layersUpdatedString="$unchangedLayers $changedLayer" || break
    echo "Pushing new layers configuration to consumer function: $i ..." || break 
    aws lambda update-function-configuration --function-name $i --layers ${layersUpdatedString} || break
    echo "pushed!" || break
done &&

echo "DONE!"