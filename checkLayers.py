import plutora

f = open('deletedLayers.txt','r')

for layer in f:
	layerGuid = layer.strip()
	layerdata = plutora.api("GET","layers/"+layerGuid)
	if layerdata=="":
		print layerGuid

