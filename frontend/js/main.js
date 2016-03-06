angular.module('borealysisApp', [])
.controller('borealysisController', function($scope, $http) {
    var api_url = "http://unearthed.nicolaus.pw/";
    var borealysis = this;

    borealysis.boreholes = {};
    borealysis.data = {};

    function data_request (url) {
        var result = $http({
          method: 'GET',
          url: url
        }).then(function successCallback(response) {
            return (response);
          }, function errorCallback(response) {
            console.log("GET error.");
          });
        return (result);
    }

    borealysis.get_boreholes = function() {
        var url = api_url.concat("holes/");
        var response = data_request(url);
        console.log(response);
        // $http({
        //   method: 'GET',
        //   url: url
        // }).then(function successCallback(response) {
        //     borealysis.boreholes = response.data;
        //     console.log(borealysis.boreholes)
        //   }, function errorCallback(response) {
        //     console.log("GET error.");
        //   });
    };

    borealysis.get_borehole_properties = function(borehole_id){
        var url = api_url.concat("holes/").concat(borehole_id).concat("/");
        data = data_request(url);
        console.log(data);


    };

    borealysis.borehole_search = function(){
        var search = borealysis.search;
        borealysis.get_borehole_properties(search);

    };

    borealysis.get_boreholes();


    borealysis.test = [{"text":"ayy lmao"}];



});


