//use angularJS to help implement the profile page
var app = angular.module('profile', []);
app.controller('profileCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.histories = [];

    histories = JSON.parse(history_data);

    histories.forEach(function(history){
        var h = {
            domainModelName : history.domainModelName,
            length : history.files.length,
            files : []
        };

        history.files.forEach(function(file){

            let date = new Date(file.date.$date).toLocaleDateString();
            let time = new Date(file.date.$date).toLocaleTimeString();

            var f = {
                id : file.file.$oid,
                date : time + " " + date
            };
            h.files.push(f);
        });

        $scope.histories.push(h);
    });
    
}]);


