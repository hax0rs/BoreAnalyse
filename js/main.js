angular.module('borealysisApp', [])
.controller('borealysisController', function($scope, $http) {
    var api_url = "http://unearthed.nicolaus.pw/";
    var borealysis = this;


    borealysis.data = {};


    borealysis.get_boreholes = function() {
        var url = api_url.concat("holes/");
        $http({
          method: 'GET',
          url: url
        }).then(function successCallback(response) {
            console.log(response.data);
          }, function errorCallback(response) {
            console.log("GET error.");
          });
    };

    borealysis.get_borehole_properties = function(borehole_id){
        var url = api_url.concat("holes/").concat(borehole_id);
        $http({
          method: 'GET',
          url: url
        }).then(function successCallback(response) {
            console.log(response.data);
          }, function errorCallback(response) {
            console.log("GET error.");
          });
    };

    borealysis.borehole_search = function(){
        var search = borealysis.search;


    };

    // get_boreholes();



    borealysis.test = [{"text":"ayy lmao"}];



});


