const icon = L.icon({
  iconSize: [25, 41],
  iconAnchor: [10, 41],
  popupAnchor: [2, -40],
  iconUrl: "https://unpkg.com/leaflet@1.6/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.6/dist/images/marker-shadow.png"
});

Promise.all([
  fetch("http://127.0.0.1:8000/api/v1/map_pepinieres/"),
  
]).then(async ([response1, response2]) => {
  const responseData1 = await response1.json();
 // const responseData2 = await response2.json();

  const data1 = responseData1;
  console.log(data1);
  //const data2 = responseData2;

  const pepinieres = L.featureGroup().addTo(map);
  //url = "http://127.0.0.1:8000/api/v1/map_pepinieres/";

data1.forEach(({id,cooperative, region, ville, site, latitude, longitude, technicien, contacts_technicien,fournisseur,contacts_fournisseur, superviseur, contacts_superviseur, production_plant,sachet_recus}) => {
    pepinieres.addLayer(
      L.marker([latitude, longitude], { icon }).bindPopup(
        `
          <table class="table table-striped table-bordered">
            <thead style="align-items: center">
                <tr>           
                  <th scope="col" class="center">ID</th>
                  <th scope="col" class="center">INFORMATIONS</th>                  
                </tr>
            </thead>
            <tbody style="align-items: center">
                
                <tr>
                    <th scope="col"><b>LOCALISATION :</b></th>
                    <td class="text-uppercase"><strong>${ville} - ${site}</strong></td>                    
                </tr>
                <tr>
                    <th scope="col"><b>SUPERVISEUR :</b></th>
                    <td class="text-uppercase"><strong>${superviseur} - ${contacts_superviseur}</strong></td>                    
                </tr>
                <tr>
                    <th scope="col"><b>TECHNICIEN:</b></th>
                    <td class="text-uppercase"><strong>${technicien} - ${contacts_technicien}</strong></td>                     
                </tr>
                <tr>
                    <th scope="col"><b>PLANTS A PRODUIRES :</b></th>
                    <td class="text-uppercase">${production_plant}</td>                    
                </tr>
                <tr>
                    <th scope="col"><b>SACHETS RECUS :</b></th>
                    <td class="text-uppercase">${sachet_recus}</td>                    
                </tr>
                <tr>
                <th scope="col"><b>ESPECES</b></th>
                <td class="text-uppercase text-center">
                    <a class="btn btn-success" href="#" onclick="show_semence('http://127.0.0.1:8000/semence_by_pepiniere/${id}')" target="_blank"  role="button"><i class="glyphicon glyphicon-tree-deciduous"></i></a>
                </td>
            </tr>
            </tbody>
          </table>    
        `
      )
    );
  });

 // map.fitBounds(pepinieres.getBounds());
});

//Initialisation de la Map
var map = L.map('map').setView([7.539989, -5.547080], 7);
map.zoomControl.setPosition('topright');

var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
 maxZoom: 22,
 attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors - @Copyright - Agro-Map CI'
}).addTo(map);

//map Climat
var climat = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
 maxZoom: 22,
 attribution: '@Copyright - Agro-Map CI - Map'
});


// Ajouter Popup de Marquage
var singleMarker = L.marker([5.349390, -4.017050])
 .bindPopup("Bienvenus en .<br> Côte d'Ivoire.")
 .openPopup();

// Ajouter Calcul de Distance
L.control.scale().addTo(map);

//Afficher les Coordonnées sur la carte
map.on('mousemove', function (e) {
 //console.log(e);
 $('.coordinates').html(`lat: ${e.latlng.lat}, lng: ${e.latlng.lng}`)
});


//Charger les Villes sur la Carte
//L.geoJSON(data).addTo(map);
var marker = L.markerClusterGroup();
marker.addTo(map);

// Laeflet Layer control
var baseMaps = {
 'ROUTE': osm,
 'COUVERT FORESTIER': climat,
}

var overLayMaps = {
 // 'VILLES' : marker,
 // 'ABIDJAN': singleMarker
}
L.control.layers(baseMaps, overLayMaps, {collapse :false, position: 'topleft'}).addTo(map);




function show_semence(url) {
  event.preventDefault();

  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  $.ajax({
      url:url,
      method: "GET",
      dataType : "json",
      success:function(response){
        //console.log(response.templateStr);
         $('#ModalSemence').html(response.templateStr)
         $('#ModalSemence').modal('show')
         
      }
  });


}

function fermer() {
    $('#modalSemence').toggle( "hide" );
    $('.fade').removeClass('in')
}

