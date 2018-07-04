import json


	
with open("logs/modeldict.txt", mode='r') as jsonfile:
	modeldict = json.load(jsonfile)
mdlnmbQU = modeldict['126']
mdlnmbBS = modeldict['121']
mdlnmbPU = modeldict['132']
	
def V_VAr_getter(sd):
	#zeigt nur die eingestellten Werte an
	values = []
	ActPt = 0

	sd.read()
	ActPt = sd.device.models_list[mdlnmbQU].blocks[1].points["ActPt"].value_getter()
			

	for index in range(ActPt):
	#sucht aktivierte Werte heraus

		searchV = "V" + str(index+1)
		searchVAr = "VAr" + str(index+1)

		v_value = sd.device.models_list[mdlnmbQU].blocks[1].points[searchV].value_getter()
		var_value = sd.device.models_list[mdlnmbQU].blocks[1].points[searchVAr].value_getter()
		quotientQWmax = round(float(var_value)/float(sd.device.models_list[mdlnmbBS].points['WMax'].value_getter()),3)

		#bildet Tupel aus den gewonnenen Werten und haengt es an Liste
		pov = (v_value, var_value, quotientQWmax)
		values.append(pov)

	return(values)
	
def V_VAr_setter(sd, values):
	sd.read()
	#schreibt V-Wert
	for index, v in enumerate(values["valuesV"]):
		print(v)
		strV = "V" + str(index+1)
		sd.volt_var.curve[1][strV] = v
	#schreibt VAr-Werte
	for index, var in enumerate(values["valuesVAr"]):
		strVAr = "VAr" + str(index+1)
		sd.volt_var.curve[1][strVAr] = var
		newActPt = index+1
	#setzt ActPt neu
	sd.device.models_list[mdlnmbQU].blocks[1].points['ActPt'].value_setter(newActPt)
	#sichert Aenderungen		
	sd.volt_var.write()
	return(values)
	
def V_W_getter(sd):
	#zeigt nur die eingestellten Werte an
	values = []
	ActPt = 0
	
	ActPt = sd.device.models_list[mdlnmbPU].blocks[1].points["ActPt"].value_getter()
			

	for index in range(ActPt):
	#sucht aktivierte Werte heraus
		searchV = "V" + str(index+1)
		searchW = "W" + str(index+1)
		
		v_value = sd.device.models_list[mdlnmbPU].blocks[1].points[searchV].value_getter()
		w_value = sd.device.models_list[mdlnmbPU].blocks[1].points[searchW].value_getter()
		

		#bildet Tupel aus den gewonnenen Werten und haengt es an Liste
		pov = (v_value, w_value)
		values.append(pov)

	return(values)
	
def V_W_setter(sd, values):
	#schreibt V-Werte
	for index, v in enumerate(values["valuesV"]):
		strV = "V" + str(index+1)
		sd.device.models_list[mdlnmbPU].blocks[1].points[strV].value_setter(v)
		if str(v) != str(sd.device.models_list[mdlnmbPU].blocks[1].points[strV].value_getter()):
			sd.device.models_list[mdlnmbPU].blocks[1].points[strV].value_setter(v*10)
	#schreibt W-Werte
	for index, watt in enumerate(values["valuesW"]):
		strW = "W" + str(index+1)
		sd.volt_watt.curve[1][strW] = watt
		newActPt = index+1
	#setzt ActPt neu
	sd.device.models_list[mdlnmbPU].blocks[1].points['ActPt'].value_setter(newActPt)
	#sichert Aenderungen	
	sd.volt_watt.write()
	return(values)
	
def V_quo_getter(sd):
	#zeigt nur die eingestellten Werte an
	values = []
	ActPt = 0

	sd.read()
	ActPt = sd.device.models_list[mdlnmbQU].blocks[1].points['ActPt'].value_getter()
			

	for index in range(ActPt):
	#sucht aktivierte Werte heraus

		searchV = "V" + str(index+1)
		searchVAr = "VAr" + str(index+1)

		v_value = sd.device.models_list[mdlnmbQU].blocks[1].points[searchV].value_getter()
		var_value = sd.device.models_list[mdlnmbQU].blocks[1].points[searchVAr].value_getter()
		quotientQWmax = round(float(var_value)/float(sd.device.models_list[mdlnmbBS].points['WMax'].value_getter()),3)

		#bildet Tupel aus den gewonnenen Werten und haengt es an Liste
		pov = (v_value, var_value, quotientQWmax)
		values.append(pov)

	return(values)
	
def V_Quo_setter(sd, values):
	sd.read()
	#schreibt V-Wert
	for index, v in enumerate(values["valuesV"]):
		strV = "V" + str(index+1)
		sd.volt_var.curve[1][strV] = v
	#schreibt VAr-Werte
	for index, quo in enumerate(values["valuesQuo"]):
		strVAr = "VAr" + str(index+1)
		sd.volt_var.curve[1][strVAr] = (quo * float(sd.device.models_list[mdlnmbBS].points['WMax'].value_getter()))
		newActPt = index+1
	#setzt ActPt neu
	sd.device.models_list[mdlnmbQU].blocks[1].points["ActPt"].value_setter(newActPt)
	#sichert Aenderungen	
	sd.volt_var.write()
	return(values)
	
def basic_settings_getter(sd):
	sd.read()
	values = []
	for point in sd.device.models_list[mdlnmbBS].blocks[0].points_list:
		if point.value is not None:
			pov = (point.point_type.label, point.value)
			values.append(pov)
	return(values)
