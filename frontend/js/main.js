angular.module('borealysisApp', [])
.controller('borealysisController', function($scope, $http) {
    var api_url = "http://unearthed.nicolaus.pw/";
    var borealysis = this;

    borealysis.current = {};
    borealysis.boreholes = {};
    borealysis.data = {};
    borealysis.summary = {};



    borealysis.get_boreholes = function() {
        var url = api_url.concat("holes/");
        var response = data_request(url);
        console.log(response);
        $http({
          method: 'GET',
          url: url
        }).then(function successCallback(response) {
            borealysis.boreholes = response.data;
            console.log(borealysis.boreholes);
          }, function errorCallback(response) {
            console.log("GET error.");
          });
    };

    borealysis.get_borehole_properties = function(borehole_id){
        var url = api_url.concat("con/").concat(borehole_id).concat("/");
        $http({
          method: 'GET',
          url: url
        }).then(function successCallback(response) {
            borealysis.current = response.data;
            console.log(borealysis.current);
          }, function errorCallback(response) {
            console.log("GET error.");
          });


    };

    borealysis.get_borehole_summary = function(borehole_id){
        var url = api_url.concat("summary/").concat(borehole_id).concat("/");
        $http({
          method: 'GET',
          url: url
        }).then(function successCallback(response) {
            borealysis.summary = response.data;
            console.log(borealysis.summary);
          }, function errorCallback(response) {
            console.log("GET error.");
          });
    };

    borealysis.borehole_search = function(){
        var search = borealysis.search;
        borealysis.get_borehole_properties(search);
        borealysis.get_borehole_summary(search);
        // console.log(borealysis.current);
        // console.log(borealysis.current);

        var url = api_url.concat("summary/").concat(search).concat("/");
        $http({
          method: 'GET',
          url: url
        }).then(function successCallback(response) {
            var returnedData = response.data;
            var a = returnedData.location.latitude;
            var b = returnedData.location.longitude;
            window.map.setZoom(10);
            window.map.setCenter({lat: a, lng: b});

              var otherMarker = new google.maps.Marker({
                position: {lat: a, lng: b},
                map: window.map,
                title: search
              });

            // console.log(borealysis.summary);
          }, function errorCallback(response) {
            console.log("GET error.");
          });

    };





});

