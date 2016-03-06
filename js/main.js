angular.module('borealysisApp', [])
.controller('borealysisController', function($scope, $http) {
    var api_url = "http://unearthed.nicolaus.pw/";
    var borealysis = this;

    borealysis.current = {};
    borealysis.boreholes = {};
    borealysis.data = {};


// Animation

function lmao () {
    var h = 100;
var foo = setInterval(function () {
   if (h>2000) {
    clearInterval(foo);
   }
   h = h + 5;
   document.getElementById('vis').style.height = h + 'px';
}, 100);

}

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
        var url = api_url.concat("holes/").concat(borehole_id).concat("/");
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

    borealysis.borehole_search = function(){
        var search = borealysis.search;
        borealysis.get_borehole_properties(search);
        lmao();
    };


    borealysis.test = [{"text":"ayy lmao"}];



});

