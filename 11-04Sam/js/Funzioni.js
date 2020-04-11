var i = 1;
var listaMed = ["aspirina", "vivinC", "tachipirina"];
var listaOrari = ["00:00","00:30","01:00","01:30","02:00","02:30","03:00","03:30","04:00","04:30","05:00","05:30",
				  "06:00","06:30","07:00","07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30",
				  "12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:15","16:20","16:30","16:35", "16:40","16:45","16:50","16:55","17:00","17:30",
				  "18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"];
var nMed = listaMed.length;
var nOrari = listaOrari.length;

function InizializzaTabella(){
	var el = document.getElementById("Orario_1");
	var but = document.createElement('button');
	var butMed = document.createElement('button');
	var td1 = document.createElement('td');
	var td2 = document.createElement('td');
	var td3 = document.createElement('td');
	var td_b = document.createElement('td');
	var aggiungiMed = document.createElement('button');
 	var selectMed = document.createElement("select");
 	var selectOrario = document.createElement("select");
 	for (var ind = 0; ind<nMed; ind++){
		var op;
		var medicinale = listaMed[ind];
		op = document.createElement("option");
		op.setAttribute("value", medicinale);
		op.append(medicinale);
		selectMed.append(op);
	}
	for (var ind = 0; ind<nOrari; ind++){
		var op;
		var orario = listaOrari[ind];
		op = document.createElement("option");
		op.setAttribute("value", orario);
		op.append(orario);
		selectOrario.append(op);
	}
	// setto l'id degli elementi
 	aggiungiMed.setAttribute("id", "Button_" + i);
 	but.setAttribute("id", "del_Orario_" + i);
 	butMed.setAttribute("id", "del_Farmaco_" + i + "_1");
 	td_b.setAttribute("class", "Medicinale_" + i + "_1");
 	// setto gli nome e placeholder degli elementi input
	selectOrario.setAttribute("name", "Orario_" + i);
	selectMed.setAttribute("name", "Medicinale_" + i + "_1");
	td2.setAttribute("class", "Medicinale_" + i + "_1");
	td3.setAttribute("id", "Td_button_" + i);
	// setto la funzione da richiamare schiacciato il bottone
	aggiungiMed.setAttribute("onclick", "aggiungiMedicinale(this.id)");
	aggiungiMed.append("Aggiungi medicinale");
	aggiungiMed.setAttribute("type", "button");
	but.setAttribute("onclick", "delOrario(this.id)");
	but.append("- Orario");
	but.setAttribute("type", "button");
	butMed.setAttribute("onclick", "delFarmaco(this.id)");
	butMed.append("- Farmaco");
	butMed.setAttribute("type", "button");
	// inserisco gli elementi input nei rispettivi elementi td
  	td1.append(selectOrario);
  	td_b.append(butMed);
  	td2.append(selectMed);
  	td3.append(aggiungiMed);
  	el.append(but);
	el.append(td1);
	el.append(td_b);
	el.append(td2);
	el.append(td3);
	i++;
}


function aggiungiOrario() {
	// creo un elemento di tipo tr, due di tipo td e due di tipo select e un bottone(per aggiungere più faramci per un orario)
  	var tr = document.createElement('tr');
  	var but = document.createElement('button');
  	var butMed = document.createElement('button');
	var td1 = document.createElement('td');
	var td2 = document.createElement('td');
	var td3 = document.createElement('td');
	var td_b = document.createElement('td');
 	var aggiungiMed = document.createElement('button');
 	var selectMed = document.createElement("select");
 	var selectOrario = document.createElement("select");
 	// inserisco all'interno dei select le varie opzioni possibili
	for (var ind = 0; ind<nMed; ind++){
		var op;
		var medicinale = listaMed[ind];
		op = document.createElement("option");
		op.setAttribute("value", medicinale);
		op.append(medicinale);
		selectMed.append(op);
	}
	for (var ind = 0; ind<nOrari; ind++){
		var op;
		var orario = listaOrari[ind];
		op = document.createElement("option");
		op.setAttribute("value", orario);
		op.append(orario);
		selectOrario.append(op);
	}

 	// setto l'id degli elementi
 	tr.setAttribute("id", "Orario_" + i);
 	aggiungiMed.setAttribute("id", "Button_" + i);
 	but.setAttribute("id", "del_Orario_" + i);
 	butMed.setAttribute("id", "del_Farmaco_" + i + "_1");
 	butMed.setAttribute("type", "button");
 	td_b.setAttribute("class", "Medicinale_" + i + "_1");
 	// setto gli nome e placeholder degli elementi input
	selectOrario.setAttribute("name", "Orario_" + i);
	selectMed.setAttribute("name", "Medicinale_" + i + "_1");
	td2.setAttribute("class", "Medicinale_" + i + "_1");
	td3.setAttribute("id", "Td_button_" + i);
	// setto la funzione da richiamare schiacciato il bottone
	aggiungiMed.setAttribute("onclick", "aggiungiMedicinale(this.id)");
	aggiungiMed.append("Aggiungi medicinale");
	aggiungiMed.setAttribute("type", "button");
	but.setAttribute("onclick", "delOrario(this.id)");
	but.append("- Orario");
	but.setAttribute("type", "button");
	butMed.setAttribute("onclick", "delFarmaco(this.id)");
	butMed.append("- Farmaco");
	// inserisco gli elementi input nei rispettivi elementi td
	td_b.append(butMed);
  	td1.append(selectOrario);
  	td2.append(selectMed);
  	td3.append(aggiungiMed);
  	// inserisco i due elementi td nell'elemento tr
 	tr.append(but);
	tr.append(td1);
	tr.append(td_b);
	tr.append(td2);
	tr.append(td3);
	// prendo l'elemento che contiene l'elemento tr e lo aggiungo al suo interno
	document.getElementById("tab").appendChild(tr);
	i++;
}

function aggiungiMedicinale(button_id){
	// so a che orario corrisponde il bottone
	// se il button_id è Button_1, l'id del tr sarà Orario_1
	// così troverò il valore di i
	// per trovare il valore di j invece devo vedere quanti elementi di tipo td ci sono nel tr
	// questo valore comprenderà anche il bottone e l'orario che non ci interessano (-2)
	// il valore poi dovrà essere incrementato per ottenere il valore del prossimo elemento da aggiungere (+1)
	// faccio -1 e ottengo quello che mi serve
	var id = button_id;
	var i2 = id.replace("Button_","");
	var tabella = document.getElementById("Orario_" + i2);
 	var j = tabella.getElementsByTagName("td").length;
 	j = j/2;

	// devo aggiungere tre elementi td (uno per rimuovere il medicinale, uno per il nuovo medicinale, uno per reinserire il bottone)
	var td_b1 = document.createElement('td');
	var td = document.createElement('td');
	var td_b = document.createElement('td');
	// all'interno del td dovrà esserci un elemento select
	var inMed = document.createElement('select');
	// inserisco le opzioni nel select
	for (var ind = 0; ind<nMed; ind++){
		var op;
		var medicinale = listaMed[ind];
		op = document.createElement("option");
		op.setAttribute("value", medicinale);
		op.append(medicinale);
		inMed.append(op);
	}

	// dovrà essere settato l'id ed il placeholder di questo elemento
	inMed.setAttribute("name", "Medicinale_" + i2 + "_" + j);
	td.setAttribute("class", "Medicinale_" + i2 + "_" + j);
	td_b.setAttribute("id", "Td_button_" + i2);
	td_b1.setAttribute("class", "Medicinale_" + i2 + "_" + j);
	// dovrò inserire l'elemento di input nell'elemento td
	td.append(inMed);
	// prima di aggiungere il nuovo elemento tolgo il bottone(devo togliere l'intero td non solo il button)
	var bottone = document.getElementById("Td_button_" + i2);
    bottone.parentNode.removeChild(bottone);

    var rimuoviMed = document.createElement('button');
//  alert("1");
	rimuoviMed.setAttribute("id", "del_Farmaco_" + i2 + "_" + j);
	rimuoviMed.append("- Farmaco");
//	alert("2");
	rimuoviMed.setAttribute("type", "button");
	rimuoviMed.setAttribute("onclick", "delFarmaco(this.id)");
//	alert("3");
	td_b1.append(rimuoviMed);
//	alert(i2);
//	alert(j);
	document.getElementById("Orario_" + i2).append(td_b1);
	// e inserire il td ottenuto nel tr originario
	document.getElementById("Orario_" + i2).append(td);
	// e poi reinserisco il bottone nel posto giusto
	var aggiungiMed = document.createElement('button');
	aggiungiMed.setAttribute("id", button_id);
	aggiungiMed.append("Aggiungi medicinale");
	aggiungiMed.setAttribute("type", "button");
	aggiungiMed.setAttribute("onclick", "aggiungiMedicinale(this.id)");
	
	// inserisco il bottone nel td
	td_b.append(aggiungiMed);

	document.getElementById("Orario_" + i2).append(td_b);
}

function delOrario(button_id){
	// devo controllare che ci siano almeno due orari se no non posso cancellarlo
	var t = document.getElementById("tab");
	var n_orari = t.getElementsByTagName("tr").length;
	if (n_orari == 1){
		alert("C'è solo un orario non puoi cancellarlo");
	}
	else{
		var id = button_id;
		var i2 = id.replace("del_Orario_","");
		var toDelete = document.getElementById("Orario_" + i2);
		toDelete.parentNode.removeChild(toDelete);
	}
}

function delFarmaco(button_id){
	// devo controllare che in quell'orario ci siano almeno due farmaci altrimenti non posso cancellarlo

	var id = button_id;
	var i2 = id.replace("del_Farmaco_","");
	var lista = i2.split("_");
	var n = lista[0];
	var t = document.getElementById("Orario_" + n);
	var n_farmaci = t.getElementsByTagName("td").length;
	n_farmaci = (n_farmaci - 2)/2;
	if (n_farmaci == 1){
		alert("C'è solo un farmaco non lo puoi eliminare");
	}
	else{
		var toDelete = document.getElementsByClassName("Medicinale_" + i2);
		for (ind = 0; ind<=toDelete.length; ind++){
			// devo eliminare uno per volta gli elementi della classe "Medicinale_" +i2
			toDelete[0]= toDelete[0].parentNode.removeChild(toDelete[0]);
		}
	}
}
