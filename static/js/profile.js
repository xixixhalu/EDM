//use angularJS to help implement the profile page
var app = angular.module('profile', []);
app.controller('profileCtrl', ['$scope', '$http', function($scope, $http) {

    running_instances = new Set();

    instances = JSON.parse(running_instance_data);

    for (var i = 0; i < instances.length; i++) {
        let instance = instances[i];
        running_instances.add(instance.file.$oid);
    }

    $scope.histories = [];
    histories = JSON.parse(history_data);
    for (var i = 0; i < histories.length; i++) {
        var history = histories[i];
        var h = {
            domainModelName : history.domainModelName,
            length : history.files.length,
            files : []
        };

        for (var j = 0; j < history.files.length; j++ ) {
            var file = history.files[j];
            let date = new Date(file.date.$date).toLocaleDateString();
            let time = new Date(file.date.$date).toLocaleTimeString();
            let updated_date = file.updated ? new Date(file.updated.$date).toLocaleDateString() : date;
            let updated_time = file.updated ? new Date(file.updated.$date).toLocaleTimeString() : time;
            var f = {
                id : file.file.$oid,
                date : time + " " + date,
                updated : updated_time + " " + updated_date,
                active : running_instances.has(file.file.$oid) ? true : false
            };
            h.files.push(f);
        }
        $scope.histories.push(h);
    }
}]);
