        function totalReload(amount) {
		
		var i;
		var inputvaluesV = []
		var inputvaluesVAr = []
		for (i = 1; i < amount+1; i++) {
			var searchtextV = 'input[name="V' + i + '"]';
			var searchtextVAr = 'input[name="VAr' + i + '"]';
			inputvaluesV.push($(searchtextV).val());
			inputvaluesVAr.push($(searchtextVAr).val());
		} 
		var valueObject = { 
                        valuesV : inputvaluesV,
                        valuesVAr : inputvaluesVAr,
                }
		
      $.post('control', JSON.stringify(valueObject), function(data) {
        var newPlotData = [];
        var arrayLength = data.newvalues.valuesV.length;
        for (var i = 0; i < arrayLength; i++) {
			newPlotData.push([data.newvalues.valuesV[i], data.newvalues.valuesVAr[i]]);
		}
		$.plot("#QUGraph", [{
				data: newPlotData,
				lines: { show: true },
				points: { show: true }
			},]);
        
      });
      $("#reload").load(location.href + " #reload>*", "");
      $("#reload2").load(location.href + " #reload2>*", "");
      
      return false;
		
		}
                
        function deleteEntry(target) {
		
		var i;
		var inputvaluesV = []
		var inputvaluesVAr = []
		for (i = 1; i < amount+1; i++) {
			var searchtextV = 'input[name="V' + i + '"]';
			var searchtextVAr = 'input[name="VAr' + i + '"]';
			inputvaluesV.push($(searchtextV).val());
			inputvaluesVAr.push($(searchtextVAr).val());
		} 
		var valueObject = { 
                        valuesV : inputvaluesV,
                        valuesVAr : inputvaluesVAr,
                        target : target,
                }
		
      $.post('deleteEntry', JSON.stringify(valueObject), function(data) {
        var newPlotData = [];
        var arrayLength = data.newvalues.valuesV.length;
        for (var i = 0; i < arrayLength; i++) {
			newPlotData.push([data.newvalues.valuesV[i], data.newvalues.valuesVAr[i]]);
		}
		$.plot("#QUGraph", [{
				data: newPlotData,
				lines: { show: true },
				points: { show: true }
			},]);
        
      });
      $("#reload").load(location.href + " #reload>*", "");
      $("#reload2").load(location.href + " #reload2>*", "");
      
      return false;
		
		}
                
        
		

