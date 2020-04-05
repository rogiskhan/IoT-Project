var i = 2;

function addfieldFunction() {
	// creo un elemento di tipo tr, due di tipo td e due di tipo input
  	var r = document.createElement('tr');
	var td1 = document.createElement('td');
	var td2 = document.createElement('td');
 	var y = document.createElement('input');
 	var z = document.createElement('input');
 	// setto gli attributi degli elementi input(<input name = "Orario1" placeholder="hh:mm")
	y.setAttribute("name", "Orario" + i + "");
	y.setAttribute("placeholder", "hh:mm");
	z.setAttribute("name", "Medicinali" + i + "");
	z.setAttribute("placeholder", "Medicinale/i");
	// inserisco gli elementi input nei rispettivi elementi td
  	td1.append(y);
  	td2.append(z);
  	// inserisco i due elementi td nell'elemento tr
	r.appendChild(td1);
	r.appendChild(td2);
	// prendo l'elemento che contiene l'elemento tr e lo aggiungo al suo interno
	document.getElementById("tab").appendChild(r);
	i++
}