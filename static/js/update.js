//use angularJS to help implement the profile page
var app = angular.module('update', []);
app.controller('updateCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.domainModelName = domainModelName;
    $scope.fileId = fileId;
    
}]);


