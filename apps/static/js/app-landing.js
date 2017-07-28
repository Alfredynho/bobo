"use strict";

var TANQUE_TYPE = 1;
var CURRENT_TYPE = 2;
var NEXT_TYPE = 3;

var app_landing = {    
    header: 
    {
        height: function(){        
            if($("#header > .header-content").outerHeight(true) < $(window).outerHeight(true)){
                $("#header").height($(window).outerHeight(true));
            }else{
                $("#header").height("auto");
            }
        },
        scroll: function(){                        
            $(window).scroll(function(){
                if($(window).width() > 992){
                    if($(window).scrollTop() > 100) {
                        $("#header .header").addClass("fixed animated fadeInDown");
                    } else {
                        $("#header .header").removeClass("fixed fadeInDown");
                    }
                }else{
                    $("#header .header").removeClass("fixed fadeInDown");
                }
            });            
        },
        navigation: function(){
            var self = this;                        
            $(".navigation-toggle").on("click",function(){
                $("#header .header .navigation").toggleClass("show");
                self.height();
            });
            
            $(".navigation a").on("click",function(){
                var href = $(this).attr("href");
                $("html, body").animate({
                    scrollTop: $(href).offset().top
                }, 500);
            });
                                    
        }
    }
    
};

$(document).ready(function(){
  app_landing.header.height();
  app_landing.header.scroll();
  app_landing.header.navigation();

  var map;
  var markers = [];
  var infoViewsArray = [];

  var lp = {lat: -16.496158993702153, lng: -68.13751441738282};
  function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12,
      center: lp
    });

    // Adds a marker at the center of the map.
    //loadMarkers(CURRENT_LOCATIONS);
    loadMarkers(ORDERS_NEWS_LOCATIONS, TANQUE_TYPE);
  }

  function loadMarkers(markers, type) {
    _.each(markers, function (item) {
      addMarker({lat: item.latitud, lng: item.longitud}, item, type);
    });

    google.maps.event.addListener(map, "click", function(event) {
      for (var i = 0; i < infoViewsArray.length; i++ ) {  //I assume you have your infoboxes in some array
        infoViewsArray[i].close();
      }
    });
    map.setZoom(12);
    map.setCenter(lp);
  }

  // Adds a marker to the map and push to the array.
  function addMarker(location, item, type) {

    var contentString = "";
    var marker = null;

    switch (type) {
      case TANQUE_TYPE:
      contentString = '<div class="infoview">'+
      '<div class="title">'+ item.estado + '</div>'+
      '<div class="body">'+
      '<p>' + item.cliente+ '</p>'+
      '</div>'+
      '</div>';
      var image = {
        url: "static/img/marker_tanque.png",
        scaledSize: new google.maps.Size(48, 48)
      };
      marker = new google.maps.Marker({
        position: location,
        map: map,
        optimized:false,
        animation: google.maps.Animation.DROP,
        icon: image
      });
      break;
      default:
      contentString = '<div class="infoview">'+
      '<div class="title">'+ item.estado + '</div>'+
      '<div class="body">'+
      '<p>' + item.cliente+ '</p>'+
      '</div>'+
      '</div>';
      var image = {
        url: "static/img/marker_cisterna.png",
        scaledSize: new google.maps.Size(48, 48)
      };
      marker = new google.maps.Marker({
        position: location,
        map: map,
        optimized:false,
        animation: google.maps.Animation.DROP,
        icon: image
      });

    }

    var closeInfos = function(){
      for (var i = 0; i < infoViewsArray.length; i++ ) {  //I assume you have your infoboxes in some array
        infoViewsArray[i].close();
      }
    }


    var infowindow = new google.maps.InfoWindow({
      content: contentString
    });


    markers.push(marker);
    infoViewsArray.push(infowindow);

    marker.addListener('click', function() {
      closeInfos();
      infowindow.open(map, marker);
    });

  }

  // Sets the map on all markers in the array.
  function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
  }

  // Removes the markers from the map, but keeps them in the array.
  function clearMarkers() {
    setMapOnAll(null);
  }

  // Shows any markers currently in the array.
  function showMarkers() {
    setMapOnAll(map);
  }

  // Deletes all markers in the array by removing references to them.
  function deleteMarkers() {
    clearMarkers();
    markers = [];
  }

  // the smooth zoom function
  function smoothZoom (map, max, cnt) {
    if (cnt >= max) {
      return;
    }
    else {
      var z = google.maps.event.addListener(map, 'zoom_changed', function(event){
        google.maps.event.removeListener(z);
        smoothZoom(map, max, cnt + 1);
      });
      setTimeout(function(){map.setZoom(cnt)}, 10); // 80ms is what I found to work well on my system -- it might not work well on all systems
    }
  }

  initMap();

  $(".btn-location").click(function (e) {
    var lat = parseFloat($(this).attr("data-lat").replace(",", "."));
    var lng = parseFloat($(this).attr("data-lng").replace(",", "."));
    var loc = {lat: lat, lng:lng};

    console.log(loc);
    map.setCenter(loc);
    map.setZoom(16);
    // smoothZoom(map, 16, map.getZoom());

  });

  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    var name = $(e.target).attr("data-name");
    if(name=="current") {
      deleteMarkers();
      loadMarkers(CURRENT_LOCATIONS, CURRENT_TYPE);
    } else if(name=="next") {
      deleteMarkers();
      loadMarkers(NEXT_LOCATIONS, NEXT_TYPE);
    } else {
      deleteMarkers();
      loadMarkers(ORDERS_NEWS_LOCATIONS, TANQUE_TYPE);
    }
  })

});

$(window).resize(function(){
  app_landing.header.height();
});

var delayBeforeFire = (function(){
  var timer = 0;

  return function (callback, ms) {
    clearTimeout(timer);
    timer = setTimeout(callback, ms);
  };
})();
