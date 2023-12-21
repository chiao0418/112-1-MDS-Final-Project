// ---- Global ----

var map = undefined
var center = undefined
let zoom = 15; // 0 - 18

var predict_layer = undefined
let green = '#159e30'
let yellow = '#fcd018'
let orange = '#ed6415'
let red = '#ac121b'
let opacity = 0.7
let weight = 6

// ---- GPS ----

function successGPS(position) {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    center = [lat, lng];
    render_map(center);
};

function errorGPS() {
    window.alert('無法判斷您的所在位置，預設地點將為台灣大學');
    center = [25.0173405, 121.5397518];
    render_map(center);
};


// ---- Map Component ----

function place_marker(icon, position, info){
    const marker_position = position;
    const custom_icon = icon
    const marker = L.marker(marker_position, {
        title: '點擊查看事故資訊',
        opacity: 1.0,
        icon: custom_icon,
    }).addTo(map);

    marker.bindPopup(info);
};

function draw_circle(position, info){
    const circle = L.circle(position, {
        color: "#000000",
        weight: 1.5,
        fillColor: "#ffffff",
        fillOpacity: 0.5,
        radius: 10.0
    }).addTo(map);

    circle.bindPopup(info);
};


// ---- Map Render

function render_map(center){

    // Init map
    let map_center = center;
    map = L.map('map').setView(map_center, zoom)
    L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
    }).addTo(map);
    
    // // Listen click event
    // const popup = L.popup();
    // function onMapClick(e) {
    //     let lat = e.latlng.lat;
    //     let lng = e.latlng.lng;
    //     popup
    //         .setLatLng(e.latlng)
    //         .setContent(`緯度：${lat}<br/>經度：${lng}`)
    //         .openOn(map);
    // };
    // map.on('click', onMapClick);
    
    place_marker(blueIcon, center);

    // Draw Event
    $.ajax({
        url: '/get_accident_data',
        data: {},
        type: 'GET',
        success: function(data){
            let accident_data = eval(data.accident_data);
            console.log(accident_data.length);
            for (i=0;i<accident_data.length;i++){
                console.log(accident_data[i]['death_injured'])
                switch (accident_data[i]['death_injured']){
                    case 0: place_marker(greyIcon, accident_data[i]['location'], accident_data[i]['info']);
                        break;
                    case 1: place_marker(yellowIcon, accident_data[i]['location'], accident_data[i]['info']);
                        break;
                    case 2: place_marker(orangeIcon, accident_data[i]['location'], accident_data[i]['info']);
                        break;
                    default:
                        place_marker(redIcon, accident_data[i]['location'], accident_data[i]['info']);
                        break;
                }
            }
        },
        error: function(error_message){
            alert('Ajax Request Error', error_message)
        }
    })
};

function prediction_drawer(weekend, time, climate){
    // Draw Road
    $.ajax({
        url: '/get_geo_data',
        data: {'weekend': weekend, 'time': time, 'climate': climate},
        type: 'POST',
        success: function(data){
            let geo_data = data.geo_data
            predict_layer = L.geoJson(geo_data, {style: function(feature) {
                switch (feature.severity) {
                    case 0: return {color: green, "weight": weight, "opacity": opacity};
                    case 1: return {color: yellow, "weight": weight, "opacity": opacity};
                    case 2: return {color: orange, "weight": weight, "opacity": opacity};
                    case 3: return {color: red, "weight": weight, "opacity": opacity};
                }
            }})
            
            map.addLayer(predict_layer);
        },
        error: function(error_message){
            alert('Ajax Request Error', error_message)
        }
    })
}