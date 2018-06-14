def V_VAr_getter(sd):
	#zeigt nur die eingestellten Werte an
	values = []
	ActPt = 0

	sd.read()
	for key in sd.device.models_list[6].blocks[1].points:
		if key == "ActPt":
			ActPt = sd.device.models_list[6].blocks[1].points[key].value_getter()
			

	for index, key in enumerate(sd.device.models_list[6].blocks[1].points):
	#sucht aktivierte Werte heraus
		if index > ActPt-1:
			break

		searchV = "V" + str(index+1)
		searchVAr = "VAr" + str(index+1)

		v_value = sd.device.models_list[6].blocks[1].points[searchV].value_getter()
		var_value = sd.device.models_list[6].blocks[1].points[searchVAr].value_getter()
		quotientQWmax = round(float(var_value)/float(sd.device.models_list[3].points['WMax'].value_getter()),3)

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
	for key in sd.device.models_list[6].blocks[1].points:
		if key == "ActPt":
			sd.device.models_list[6].blocks[1].points[key].value_setter(newActPt)
			sd.volt_var.write()
	#sichert Aenderungen		
	sd.volt_var.write()
	return("test")
	
def V_W_getter(sd):
	#zeigt nur die eingestellten Werte an
	values = []
	ActPt = 0

	
	for key in sd.device.models_list[8].blocks[1].points:
		if key == "ActPt":
			ActPt = sd.device.models_list[8].blocks[1].points[key].value_getter()
			

	for index, key in enumerate(sd.device.models_list[8].blocks[1].points):
	#sucht aktivierte Werte heraus
		if index > ActPt-1:
			break

		searchV = "V" + str(index+1)
		searchW = "W" + str(index+1)

		v_value = sd.device.models_list[8].blocks[1].points[searchV].value_getter()
		w_value = sd.device.models_list[8].blocks[1].points[searchW].value_getter()
		

		#bildet Tupel aus den gewonnenen Werten und haengt es an Liste
		pov = (v_value, w_value)
		values.append(pov)

	return(values)
	
def V_W_setter(sd, values):
	#schreibt V-Werte
	print("vwsetter: ")
	print(values)
	for index, v in enumerate(values["valuesV"]):
		print(v)
		strV = "V" + str(index+1)
		sd.device.models_list[8].blocks[1].points[strV].value_setter(v)
		if str(v) != str(sd.device.models_list[8].blocks[1].points[strV].value_getter()):
			sd.device.models_list[8].blocks[1].points[strV].value_setter(v*10)
	#schreibt W-Werte
	for index, watt in enumerate(values["valuesW"]):
		strW = "W" + str(index+1)
		sd.volt_watt.curve[1][strW] = watt
		newActPt = index+1
	#setzt ActPt neu
	for key in sd.device.models_list[8].blocks[1].points:
		if key == "ActPt":
			sd.device.models_list[8].blocks[1].points[key].value_setter(newActPt)
			sd.volt_watt.write()
	#sichert Aenderungen	
	sd.volt_watt.write()
	return("test")
	
def V_quo_getter(sd):
	#zeigt nur die eingestellten Werte an
	values = []
	ActPt = 0

	sd.read()
	for key in sd.device.models_list[6].blocks[1].points:
		if key == "ActPt":
			ActPt = sd.device.models_list[6].blocks[1].points[key].value_getter()
			

	for index, key in enumerate(sd.device.models_list[6].blocks[1].points):
	#sucht aktivierte Werte heraus
		if index > ActPt-1:
			break

		searchV = "V" + str(index+1)
		searchVAr = "VAr" + str(index+1)

		v_value = sd.device.models_list[6].blocks[1].points[searchV].value_getter()
		var_value = sd.device.models_list[6].blocks[1].points[searchVAr].value_getter()
		quotientQWmax = round(float(var_value)/float(sd.device.models_list[3].points['WMax'].value_getter()),3)

		#bildet Tupel aus den gewonnenen Werten und haengt es an Liste
		pov = (v_value, var_value, quotientQWmax)
		values.append(pov)

	return(values)
	
def V_Quo_setter(sd, values):
	sd.read()
	print("factor: " + str(values))
	#schreibt V-Wert
	for index, v in enumerate(values["valuesV"]):
		print(v)
		strV = "V" + str(index+1)
		sd.volt_var.curve[1][strV] = v
	#schreibt VAr-Werte
	for index, quo in enumerate(values["valuesQuo"]):
		print(quo)
		strVAr = "VAr" + str(index+1)
		print (quo * float(sd.device.models_list[3].points['WMax'].value_getter()))
		sd.volt_var.curve[1][strVAr] = (quo * float(sd.device.models_list[3].points['WMax'].value_getter()))
		newActPt = index+1
	#setzt ActPt neu
	for key in sd.device.models_list[6].blocks[1].points:
		if key == "ActPt":
			sd.device.models_list[6].blocks[1].points[key].value_setter(newActPt)
			sd.volt_var.write()
	#sichert Aenderungen	
	print("end")	
	sd.volt_var.write()
	return("test")
	
def basic_settings_getter(sd):
	sd.read()
	values = []
	for point in sd.device.models_list[3].blocks[0].points_list:
		pov = (point.point_type.label, point.value)
		values.append(pov)
	return(values)
