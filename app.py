from flask import Flask, render_template, jsonify, request, redirect, Response
import json

import sys
import time
import sunspec.core.client as client
import sunspec.core.suns as suns
from optparse import OptionParser

import modules.RWmodels as func

slaveid = 1#126
ipaddr = '127.0.0.1'#'192.168.0.111'
ipport = 502
timeout = 2.0
transtype = 'tcp'

app = Flask(__name__)

try:
	sd = client.SunSpecClientDevice(client.TCP, slaveid, ipaddr=ipaddr, ipport=ipport, timeout=timeout)

except client.SunSpecClientError as e:
	print('Error: %s'%(e))
	sys.exit(1)

if sd is not None:
	print('\nTimestamp: %s' % (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))

sd.read()
modeldict = {}
for num, model in enumerate(sd.device.models_list):
			if model.model_type.label:
				label = '%s (%s)' % (model.model_type.label, str(model.id))
			else:
				label = '(%s)' % (str(model.id))
			modeldict.update({model.id:num})
with open("logs/modeldict.txt", mode='w') as jsonfile:
		json.dump(modeldict, jsonfile)
		
with open("logs/modeldict.txt", mode='r') as jsonfile:
		modeldict = json.load(jsonfile)
mdlnmbQU = modeldict['126']
mdlnmbBS = modeldict['121']
mdlnmbINV = 1#modeldict['103']
mdlnmbPU = modeldict['132']
mdlnmbNAME = modeldict['120']
@app.route('/<html>')
@app.route('/')
def index(html="quregelung.html"):
	sd.read()
	if html == "maxpregelung.html":
		maxPFile = open('logs/maxP.txt', 'r')
		for line in maxPFile:
			values = {'valueMaxP':line}
		values.update({'wmax': float(sd.device.models_list[mdlnmbNAME].points['WRtg'].value_getter())})
		result=float(sd.device.models_list[mdlnmbNAME].points['WRtg'].value_getter())*float(values['valueMaxP'])*0.01
		values.update({'result': result})
	elif html == "puregelung.html":
		values = {'valuesvwatt':func.V_W_getter(sd)}
		values.update({'wmax': sd.device.models_list[mdlnmbBS].points['WMax'].value_getter(), 'vref': sd.device.models_list[mdlnmbBS].points['VRef'].value_getter()})
	elif html == "quouregelung.html":
		values = {'valuesquo':func.V_quo_getter(sd)}
		values.update({'wmax': sd.device.models_list[mdlnmbBS].points['WMax'].value_getter(), 'vref': sd.device.models_list[mdlnmbBS].points['VRef'].value_getter()})
	else:
		values = {'valuesvvar':func.V_VAr_getter(sd)}
		values.update({'vref': sd.device.models_list[mdlnmbBS].points['VRef'].value_getter()})
	status = get_status()
	actCntrl = get_control()
	return render_template(html, values = values, status = status, actCntrl = json.dumps(actCntrl))
	
@app.route('/control', methods = ['POST'])
def control():
	values = request.get_json(force=True)
	currentValues = func.V_VAr_getter(sd)
	#Code fuer QU-Regelung
	if 'valuesV' in values and 'valuesVAr' in values:
		#wandelt alle Werte in int
		for key in values:
			if key == 'checklist':
				continue
			values[key] = [float(x) for x in values[key]]
		#sortiert nach Spannung
		values["valuesV"], values["valuesVAr"] = (list(t) for t in zip(*sorted(zip(values["valuesV"], values["valuesVAr"]))))
		#schreibt werte
		func.V_VAr_setter(sd, values)
		html = "quregelung.html"
	#code fuer maxP-Regelung 
	if 'maxPvalue' in values:
		wmax = float(sd.device.models_list[mdlnmbNAME].points['WRtg'].value_getter())
		sd.device.models_list[mdlnmbBS].points['WMax'].value_setter(float(values['maxPvalue'])*wmax*0.01)
		sd.device.models_list[mdlnmbBS].write_points()
		maxPFile = open('logs/maxP.txt', 'w')
		maxPFile.write(values['maxPvalue'])
		maxPFile.close()
		html = "maxpregelung.html"
		return "200:ok"
	#code fuer PU-Regelung
	if 'valuesV' in values and 'valuesW' in values:
		#wandelt alle Werte in float
		for key in values:
			if key == 'checklist':
				continue
			values[key] = [float(x) for x in values[key]]
		#sortiert nach Spannung
		values["valuesV"], values["valuesW"] = (list(t) for t in zip(*sorted(zip(values["valuesV"], values["valuesW"]))))
		#schreibt werte
		func.V_W_setter(sd, values)
		html = "puregelung.html"
	#code fuer Q/P(U)-Regelung
	if 'valuesV' in values and 'valuesQuo' in values:
		#wandelt alle Werte in float
		print(values)
		for key in values:
			if key == 'checklist':
				continue
			values[key] = [float(x) for x in values[key]]
		#sortiert nach Spannung
		values["valuesV"], values["valuesQuo"] = (list(t) for t in zip(*sorted(zip(values["valuesV"], values["valuesQuo"]))))
		#schreibt werte
		func.V_Quo_setter(sd, values)
		html = "quouregelung.html"
	#code fuer regelungswahl
	if 'controltype' in values:
		if values["controltype"] == 'max-P':
			html = "maxpregelung.html"
		elif values["controltype"] == 'P(U)':
			html = "puregelung.html"
		elif values["controltype"] == 'Q/Pmax(U)':
			html = "quouregelung.html"
		else:
			html = "quregelung.html"
	#code fuer regelungsaktivierung
	if 'checklist' in values:
		set_control(values["checkname"], values["checklist"])
		return "switched"
	return index(html)
	
@app.route('/deleteEntry', methods = ['POST'])
def deleteEntry():
	values = request.get_json(force=True)
	target = int(values['target'])
	if 'valuesV' in values and 'valuesW' in values:
		for key in values:
			if key == 'target':
				continue
			values[key] = [float(x) for x in values[key]]
		for key in values:
			if key == 'target':
				continue
			element=values[key][target]
			del values[key][target]
			values[key].append(element)
		func.V_W_setter(sd, values)
		ActPt = sd.device.models_list[mdlnmbPU].blocks[1].points["ActPt"].value_getter()
		sd.device.models_list[mdlnmbPU].blocks[1].points["ActPt"].value_setter(ActPt-1)
		sd.volt_watt.write()
	elif 'valuesV' in values and 'valuesQuo' in values:
		for key in values:
			if key == 'target':
				continue
			values[key] = [float(x) for x in values[key]]
		for key in values:
			if key == 'target':
				continue
			element=values[key][target]
			del values[key][target]
			values[key].append(element)
		func.V_Quo_setter(sd, values)
		ActPt = sd.device.models_list[mdlnmbQU].blocks[1].points["ActPt"].value_getter()
		sd.device.models_list[mdlnmbQU].blocks[1].points["ActPt"].value_setter(ActPt-1)
		sd.volt_var.write()
	else:
		for key in values:
			if key == 'target':
				continue
			values[key] = [int(x) for x in values[key]]
		for key in values:
			if key == 'target':
				continue
			element=values[key][target]
			del values[key][target]
			values[key].append(element)
		func.V_VAr_setter(sd, values)
		ActPt = sd.device.models_list[mdlnmbQU].blocks[1].points["ActPt"].value_getter()
		sd.device.models_list[mdlnmbQU].blocks[1].points["ActPt"].value_setter(ActPt-1)
		sd.volt_var.write()
	return jsonify(newvalues = values)
	
@app.route('/getstatus', methods=['GET', 'POST'])
def post():
	keys = request.form.get('keys')
	post_models = request.form.get('models')
	alldict={}
	allmodels={}
	status={}
	if "all" in keys or post_models:
		for model in sd.device.models_list:
			if model.model_type.label:
				label = '%s (%s)' % (model.model_type.label, str(model.id))
			else:
				label = '(%s)' % (str(model.id))
			alldict.update({label: {}})
			if label in post_models:
				allmodels.update({label: {}})
			for block in model.blocks:
				if block.index > 0:
				  index = '%02d:' % (block.index)
				else:
				  index = '   '
				for point in block.points_list:
					if point.value is not None:
						if point.point_type.label:
							label2 = '%s%s(%s)' % (index, point.point_type.label, point.point_type.id)
						else:
							label2 = '%s(%s)' % (index, point.point_type.id)
						units = point.point_type.units
						if units is None:
							units = ''
						if point.point_type.type == suns.SUNS_TYPE_BITFIELD16:
							value = '0x%04x' % (point.value)
						elif point.point_type.type == suns.SUNS_TYPE_BITFIELD32:
							value = '0x%08x' % (point.value)
						else:
							value = str(point.value).rstrip('\0')
						alldict[label].update({label2:{"point_id": point.point_type.id, "value":value, "unit":str(units)}})
						if label in post_models:
							allmodels[label].update({label2:{"point_id": point.point_type.id, "value":value, "unit":str(units)}})
	if "live" in keys:
		status.update({'livedata': get_status()})
	if 'controlvwatt' in keys:
		status.update({'controlvwatt':func.V_W_getter(sd)})
	if 'controlvvar' in keys:
		status.update({'controlvvar':func.V_VAr_getter(sd)})
	if 'controlvfactor' in keys:
		status.update({'controlvfactor':func.V_quo_getter(sd)})
	if 'controlmaxp' in keys:
		maxPFile = open('logs/maxP.txt', 'r')
		for line in maxPFile:
			status.update({'controlmaxp':line})
	if 'basic_settings' in keys:
		status.update({'basic_settings':func.basic_settings_getter(sd)})
	if "all" in keys:
		status.update({'livedata': get_status()})
		status.update(alldict)
		status.update({'controlvwatt':func.V_W_getter(sd)})
		status.update({'controlvvar':func.V_VAr_getter(sd)})
		status.update({'controlvfactor':func.V_quo_getter(sd)})
		maxPFile = open('logs/maxP.txt', 'r')
		for line in maxPFile:
			status.update({'controlmaxp':line})
	if post_models:
		status.update(allmodels)
	return jsonify(status)

@app.route('/writestatus', methods = ['POST', 'GET'])
def writestatus():
	controls = request.json
	newcontrols = {}
	#verbindet alle Eingabedicts zu einem
	for control in controls:
		newcontrols.update(control)
	for key in newcontrols:
		if key == "controlvvar":
			valuesvvar = {'valuesV':[],'valuesVAr':[]}
			for value in newcontrols[key]:
				if value[0] > 0:
					valuesvvar['valuesV'].append(value[0])
				else:
					return "ERROR: Fehlerhafte Spannungseingabe"
				valuesvvar['valuesVAr'].append(value[1])
			#sortiert nach Spannung
			valuesvvar["valuesV"], valuesvvar["valuesVAr"] = (list(t) for t in zip(*sorted(zip(valuesvvar["valuesV"], valuesvvar["valuesVAr"]))))
			#schreibt Werte
			func.V_VAr_setter(sd, valuesvvar)
		if key == "controlvfactor":
			valuesvvar = {'valuesV':[],'valuesQuo':[]}
			for value in newcontrols[key]:
				if value[0] > 0:
					valuesvvar['valuesV'].append(value[0])
				else:
					return "ERROR: Fehlerhafte Spannungseingabe"
				if value[1] <= 1 and value[1] >= -1:
					valuesvvar['valuesQuo'].append(value[1])
				else:
					return "ERROR: Fehlerhafte Faktoringabe"
			#sortiert nach Spannung
			valuesvvar["valuesV"], valuesvvar["valuesQuo"] = (list(t) for t in zip(*sorted(zip(valuesvvar["valuesV"], valuesvvar["valuesQuo"]))))
			#schreibt Werte
			func.V_Quo_setter(sd, valuesvvar)
		if key == "controlvwatt":
			valuesvvar = {'valuesV':[],'valuesW':[]}
			for value in newcontrols[key]:
				if value[0] > 0:
					valuesvvar['valuesV'].append(value[0])
				else:
					return "ERROR: Fehlerhafte Spannungseingabe"
				if value[1] >= 0 and value[1] <= 100:
					valuesvvar['valuesW'].append(value[1])
				else:
					return "ERROR: Fehlerhafte Leistungseingabe"
			#sortiert nach Spannung
			valuesvvar["valuesV"], valuesvvar["valuesW"] = (list(t) for t in zip(*sorted(zip(valuesvvar["valuesV"], valuesvvar["valuesW"]))))
			#schreibt Werte
			func.V_W_setter(sd, valuesvvar)
		if key == "controlmaxp":
			wmax = float(sd.device.models_list[mdlnmbNAME].points['WRtg'].value_getter())
			sd.device.models_list[mdlnmbBS].points['WMax'].value_setter(newcontrols[key]*wmax*0.01)
			sd.device.models_list[mdlnmbBS].write_points()
			maxPFile = open('logs/maxP.txt', 'w')
			maxPFile.write(newcontrols[key])
			maxPFile.close()
		if key == "activate":
			for control in newcontrols["activate"]:
				set_control(control[0],control[1])
	return "successfully changed controlsettings"
	
	
def get_status():
	sd.read()
	i = 0
	invvalues = []
	
	invmodel = sd.device.models_list[mdlnmbINV]
	
	for point in invmodel.blocks[0].points_list:
		if i > 18:
			break
		if point.value != None:
			invvalues.append((point.point_type.id, point.value, point.point_type.units))
		i += 1
	return invvalues
	
def get_control():
	sd.read()
	actCntrl = []
	setMaxP = float(sd.device.models_list[mdlnmbBS].points['WMax'].value_getter())
	globalMaxP = float(sd.device.models_list[mdlnmbNAME].points['WRtg'].value_getter())
	if sd.device.models_list[mdlnmbQU].blocks[0].points["ActCrv"].value_getter() == 1:
		actCntrl.append("true")
	else:
		actCntrl.append("false")
	if sd.device.models_list[mdlnmbPU].blocks[0].points["ActCrv"].value_getter() == 1:
		actCntrl.append("true")
	else:
		actCntrl.append("false")
	if setMaxP/globalMaxP != 1:
		actCntrl.append("true")
	else:
		actCntrl.append("false")
	return actCntrl	
	
def set_control(name, value):
	sd.read()
	if name == "qu":
		#schreibt ActCrv in Q(U)
		if value == "true":
			sd.device.models_list[mdlnmbQU].blocks[0].points["ActCrv"].value_setter(1)
		else:
			sd.device.models_list[mdlnmbQU].blocks[0].points["ActCrv"].value_setter(0)
		sd.volt_var.write()
	elif name == "pu":
		#schreibt ActCrv in P(U)
		if value == "true":
			sd.device.models_list[mdlnmbPU].blocks[0].points["ActCrv"].value_setter(1)
		else:
			sd.device.models_list[mdlnmbPU].blocks[0].points["ActCrv"].value_setter(0)
		sd.volt_watt.write()
	elif name == "maxp":
		#setzt maxp auf Wechselrichter maximum
		if value == "true":
			maxPFile = open('logs/maxP.txt', 'r')
			for line in maxPFile:
				actMaxP = line
		else:
			actMaxP = float(sd.device.models_list[mdlnmbNAME].points['WRtg'].value_getter())
		sd.device.models_list[mdlnmbBS].points['WMax'].value_setter(actMaxP)
		sd.device.models_list[mdlnmbBS].write_points()
	else:
		return "wrong control name"
	return "switched"


    
	
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    

