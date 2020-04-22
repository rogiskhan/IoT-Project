
var i = 1;
var listaMed = ["aspirina", "vivinC", "tachipirina"];
var listaOrari = ["00:00","00:30","01:00","01:30","02:00","02:30","03:00","03:30","04:00","04:30","05:00","05:30",
				  "06:00","06:30","07:00","07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30",
				  "12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30",
				  "18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"];
var flag_valid_form = 0;
var Schedule_int = {};
var orari = [];
var liste_med = [];
var med_ind = [];


function ValidazioneForm(){
	// costruisco un dizionario grazie ai dati ottenuti dal form
	for(var ind = 0; ind<document.FormName.elements.length-1; ind++){
		var x = document.FormName.elements[ind].name;
		var y = document.FormName.elements[ind].value;
		if (x != ""){											// BUG boh prende un elemento vuoto all'inizio
			Schedule_int[x] = y;	
		}
	}
	
	lists = CreaListe(Schedule_int);
	orari = lists[0];
	liste_med = lists[1];

	ordinato = bubbleSort(orari, liste_med);
	orari = ordinato[0];
	liste_med = ordinato[1];
}

// dividere in due funzioni, una crea le liste una controlla se ci sono doppioni--> CreaListe(posso ordinare con i doppioni?) e Validazione

function CreaListe(Schedule){
	orari = [];													// conterrà la lista degli orari inseriti
	liste_med = [];												// conterrà la lista delle liste di medicinali(una lista per ogni orario)
	for (var key in Schedule){
		if (key.includes("Orario")){ 							// devo controllare se la chiave contiene "Orario_"
			if (orari.includes(Schedule[key])){				// se è già in orari l'orario è un duplicato
				alert("Un orario è stato inserito due volte il form non è valido");
				flag_valid_form = 1;
				Schedule_int = {};
			}
			else{
				orari.push(Schedule[key]);					// aggiungo l'orario alla lista degli orari
			}
			var meds = [];										// conterrà la lista dei medicinali per l'orario che stiamo controllando
			var n_or = key.replace("Orario_", "");				// rimuovo Orario_ per ottenere il numero che mi interessa
			var new_str = "Medicinale_" + n_or;					// devo cercare tutti gli elementi del tipo medicinale_n_or_##
			if (flag_valid_form == 0){							// se già il form non è valido non faccio neanche la fatica di scorrere di nuovo tra tutti i valori
				for (var key in Schedule){
					if (key.includes(new_str)){					// cerco il medicinale che mi interessano
						if (meds.includes(Schedule[key])){	// controllo che non siano già nella lista
							alert("Un medicinale è stato inserito due volte il form non è valido");
							flag_valid_form = 1;
							Schedule_int = {};
						}
						else{
							meds.push(Schedule[key]);		// se non è nella lista lo aggiungo
						}
					}
				}
				liste_med.push(meds);							// aggiungo la lista di medicinali per questo orario nella lista di liste
			}			
		}
	}
	return [orari, liste_med];
}

function aggiungiOrario() {
	// bottone per eliminare un orario
	var button = document.createElement('button');
	button.setAttribute("onclick", "delOrario(this.id)");		// funzione da richiamare quando viene schiacciato
	button.append("Rimuovi orario");							// testo sul bottone
	button.setAttribute("type", "button");						// devo specificare di tipo button se no fa partire automaticamente il submit del form
	button.setAttribute("id", "del_Orario_" + i);				// serve un id per poterlo associare all'elemento da eliminare che avrà lo stesso numero

	// il bottone deve essere inserito in un elemnto td se no dopo la funzione modifica sbabbia quando vede button invece che td in un tr
	var td = document.createElement('td');
	td.append(button);

	var tr = document.createElement('tr');
	tr.setAttribute("id", "Orario" + i);						// id che verrà cercato al momento di dover cancellare un orario

	tr.append(td);
	// menù a tendina per scegliere l'orario
	var select = document.createElement("select");
	for (var ind = 0; ind<listaOrari.length; ind++){
		var op = document.createElement("option");
		op.setAttribute("value", listaOrari[ind]);				// valori possibili da scegliere
		op.append(listaOrari[ind]);
		select.append(op);
	}
	select.setAttribute("name", "Orario_" + i);					// ogni elemento del form deve avere un suo name per identificarlo
	select.setAttribute("id", "Orario_" + i);	

	var td = document.createElement('td');
	//td.setAttribute("id", "Orario_" + i);
	td.append(select);
	tr.append(td);

	// bottone per eliminare un medicinale
	var button = document.createElement('button');
	button.setAttribute("id", "del_Medicinale_" + i + "_1");
	button.setAttribute("type", "button");
	button.setAttribute("onclick", "delMedicinale(this.id)");
	button.append("Rimuovi medicinale");

	var td = document.createElement('td');
	td.setAttribute("class", "Medicinale" + i + "_1");			// non definisco un id ma una classe perchè quando cancello un medicinale
																// devo cancellare più di un elemento
	td.append(button);
	tr.append(td);

	// menù a tendina per selezionare il medicinale
	var select = document.createElement("select");
	for (var ind = 0; ind<listaMed.length; ind++){
		var op = document.createElement("option");
		op.setAttribute("value", listaMed[ind]);
		op.append(listaMed[ind]);
		select.append(op);
	}
	select.setAttribute("name", "Medicinale_" + i + "_1");
	select.setAttribute("id", "Medicinale_" + i + "_1");

	var td = document.createElement('td');
 	td.append(select);
	td.setAttribute("class", "Medicinale" + i + "_1");
	//td.setAttribute("id", "Medicinale_" + i + "_1");
	tr.append(td);
	
	// bottone per aggiungere un medicinale
	var button = document.createElement('button');
	button.setAttribute("id", "Button_" + i);
 	button.setAttribute("onclick", "aggiungiMedicinale(this.id)");
	button.append("Aggiungi medicinale");
	button.setAttribute("type", "button");

	var td = document.createElement('td');
	td.setAttribute("id", "Td_button_" + i);
	td.append(button);
	tr.append(td);
	document.getElementById("tab").appendChild(tr);
	i++;
	med_ind[i-2] = 1;
}

function aggiungiMedicinale(button_id){
	// avendo passato come parametro l'id del bottone posso risalire all'orario a cui corrisponde (i, che mi servirà per dare gli id al nuovo medicinale)
	// dovrò tenere conto di quanti medicinali ho in ogni orario
	// tengo l'indice massimo raggiunto (+1) per ogni orario in un array med_ind
	var i2 = button_id.replace("Button_","");
	var j = med_ind[i2-1] + 1;	// in med_ind ho l'indice massimo che ho in questo momento
	//devo aggiungere un elemento che come id avrà med_ind[i2-1]+1 e alla fine aumentare il valore di med_ind[i2-1]

	// per mantenere la struttura con bottone per rimuovere il medicinale, menu a tendina e bottone per rimuovere il medicinale
	// prima rimuovo il bottone aggiungi e poi aggiungo singolarmente i 3 elementi
 	var button = document.getElementById("Td_button_" + i2);
    button.parentNode.removeChild(button);

	// bottone per rimuovere un medicinale
    var button = document.createElement('button');
	button.setAttribute("id", "del_Medicinale_" + i2 + "_" + j);
	button.append("Rimuovi Medicinale");
	button.setAttribute("type", "button");
	button.setAttribute("onclick", "delMedicinale(this.id)");

	var td = document.createElement('td');
	td.setAttribute("class", "Medicinale" + i2 + "_" + j);
	td.append(button);

	var tr = document.getElementById("Orario" + i2);
	tr.append(td);

	// menu a tendina per scegliere il medicinale
	var select = document.createElement('select');
	for (var ind = 0; ind<listaMed.length; ind++){
		var op = document.createElement("option");
		op.setAttribute("value", listaMed[ind]);
		op.append(listaMed[ind]);
		select.append(op);
	}
	select.setAttribute("name", "Medicinale_" + i2 + "_" + j);
	select.setAttribute("id", "Medicinale_" + i2 + "_" + j);

	var td = document.createElement('td');
	td.setAttribute("class", "Medicinale" + i2 + "_" + j);
	//td.setAttribute("id", "Medicinale_" + i2 + "_" + j);
	td.append(select);
	tr.append(td);

	// bottone per aggiungere medicinale
	var button = document.createElement('button');
	button.setAttribute("id", button_id);
	button.append("Aggiungi medicinale");
	button.setAttribute("type", "button");
	button.setAttribute("onclick", "aggiungiMedicinale(this.id)");

	var td = document.createElement('td');
	td.setAttribute("id", "Td_button_" + i2);
	td.append(button);
	tr.append(td);
	med_ind[i2-1] = med_ind[i2-1] + 1;
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
		var toDelete = document.getElementById("Orario" + i2);
		toDelete.parentNode.removeChild(toDelete);
	}
}

function delMedicinale(button_id){
	// devo controllare che in quell'orario ci siano almeno due medicinali altrimenti non posso cancellarlo

	var id = button_id;
	var i2 = id.replace("del_Medicinale_","");
	var lista = i2.split("_");
	var n = lista[0];
	var t = document.getElementById("Orario" + n);
	var n_medicinali = t.getElementsByTagName("td").length;
	n_medicinali = (n_medicinali - 3)/2;
	if (n_medicinali == 1){
		alert("C'è solo un medicinale non lo puoi eliminare");
	}
	else{
		var toDelete = document.getElementsByClassName("Medicinale" + i2);
		for (ind = 0; ind<=toDelete.length; ind++){
			// devo eliminare uno per volta gli elementi della classe "Medicinale_" +i2
			toDelete[0]= toDelete[0].parentNode.removeChild(toDelete[0]);
		}
	}
}

function Visualizza(){
	try{											// se non ho ricevuto niente Schedule non è definita per cui serve il blocco try
		Schedule = JSON.parse(Schedule);
		lists = CreaListe(Schedule);
		orari = lists[0];
		liste_med = lists[1];
		ordinato = bubbleSort(orari, liste_med);
		orari = ordinato[0];
		liste_med = ordinato[1];
	}
	catch{
	}
	if (orari == ""){		// non ho appena compilato il form e non mi è stato restituito niente dallo script python
		alert("Prima compila il form");
	}
	else{
		var tds = [];
		for(var i = 0; i<orari.length; i++){
			tds[i] = liste_med[i].length;		// sarà una lista con il numero di td da creare per ogni tr
		}
	}
	var body_int = document.getElementById("tab");
	var body_bu = body_int.innerHTML;
	body_bu = body_bu.trim();
	body_int.innerHTML = "";
	for (var i = 0; i<orari.length; i++){
		var td = document.createElement("td");
		var tr = document.createElement("tr");		// nel primo tr ci va l'orario
		td.append(orari[i]);
		tr.append(td);
		body_int.append(tr);
		for (var j = 0; j < tds[i]; j++){
			var td = document.createElement("td");	// negli altri td ci va il medicinale
			td.append(liste_med[i][j]);
			tr.append(td);
		}
		body_int.append(tr);
	}
}

function Submit(){
	ValidazioneForm();
	if (flag_valid_form == 0){
		var form = document.getElementById("ProvaForm");
		if (form.action[0] == "f"){
			alert("Non è stato inserito l'ip a cui mandare il form, puoi comunque visualizzare e modificare il form ma quando chiudi la finestra ciaone");
		}
		else{
				document.getElementById("ProvaForm").submit()
		}	
	}
	else{
		alert("Il form non è valido deve essere ricompilato");
		flag_valid_form = 0;
	}
}

function bubbleSort(ListaDaOrdinare, SecondaLista){
    var swapp;
    var n = ListaDaOrdinare.length-1;
    var x = ListaDaOrdinare;
    var y = SecondaLista;
    do {
        swapp = false;
        for (var ind = 0; ind < n; ind++)
        {
            if (x[ind] > x[ind+1])
            {
               var temp = x[ind];
               var temp2 = y[ind];
               x[ind] = x[ind+1];
               x[ind+1] = temp;
               y[ind] = y[ind+1];
               y[ind+1] = temp2;
               swapp = true;
            }
        }
        n--;
    } while (swapp);
    var fin = [x, y];
 	return fin; 
}

function Modifica(){
	// a partire dalle due liste di orari e medicinali creao l'html della pagina da modificare
	i = 1;
	var el = document.getElementById("tab");
	el.innerHTML = "";
	for (var ind = 0; ind<orari.length; ind++){
		aggiungiOrario();
		var el = document.getElementById("Orario_" + (ind+1));
		var value = orari[ind];
		var t = el.getElementsByTagName("option");		// ho tutti gli elementi di tipo option
		for (var ind2 = 0; ind2<t.length; ind2++){
			var opt = t[ind2];						// elemento option all'interno del select
			if (opt.value == value){
				opt.setAttribute("selected", "selected");	// faccio in modo che questo elemento sia selezionato
			}
		}
		// aggiunto l'orario devo scorrere nella lista di medicinali
		for (var ind3 = 0; ind3<liste_med[ind].length; ind3++){
			// devo calcolare l'id del bottone
			var button_id = "Button_" + (ind+1);				// se ind è 0 avrò Td_button_1
			if (ind3>0){
				aggiungiMedicinale(button_id);
			}
			var el = document.getElementById("Medicinale_" + (ind+1) + "_" + (ind3+1));
			var value = liste_med[ind][ind3];
			var t = el.getElementsByTagName("option");		// ho tutti gli elementi di tipo option
			for (var ind4 = 0; ind4<t.length; ind4++){
				var opt = t[ind4];						// elemento option all'interno del select
				if (opt.value == value){
					opt.setAttribute("selected", "selected");	// faccio in modo che questo elemento sia selezionato
				}
			}
		}
	}
}