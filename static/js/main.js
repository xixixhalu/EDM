var app = angular.module('myApp', []);
app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.classes = [];
    $scope.details = [];
    $scope.languages = [];
    $scope.changeParentTab = function(tab) {
        $scope.view_tab = tab;
    };
    $scope.changeChildTab = function (classInfo, lanInfo) {
        $scope.view = classInfo+"_"+lanInfo;
    };
    $scope.isView = function (classInfo, lanInfo) {
        return classInfo+"_"+lanInfo;
    };
    //$http({
    //    method: 'GET',
    //    url: 'getData.php'
    //}).then(function(data) {
    //    $scope.contents= data.data;
		//$scope.contents = model_display_data;
        myArray = model_display_data;//angular.fromJson($scope.contents);
        $scope.details = myArray;
        console.log($scope.details);
        Object.keys(myArray).forEach(function(k){
            $scope.languages = Object.keys(myArray[k]);
            /*$scope.languages.forEach(function(lan){
                if (lan === "attribute_list")
                    return;
            });
            $scope.languages.splice($scope.languages.indexOf("attribute_list"), 1);*/
        });

        angular.forEach(myArray, function(value, key){
            $scope.functions = [];
            $scope.classes.push(key);
        });
    //});
    $scope.generateView = function (data) {
        result = [];
        result = data.split(/\r?\n/);
        return result;
    }

    $scope.CopyToClipboard = function(classInfo, lanInfo, index) {
        // Create a new textarea element and give it id='t'
        var containerid = classInfo+"_"+lanInfo+"_"+index;
        var textarea = document.createElement('textarea');
        textarea.id = 't';
        // Optional step to make less noise on the page, if any!
        textarea.style.height = 0;
        // Now append it to your page somewhere, I chose <body>
        document.body.appendChild(textarea);
        // Give our textarea a value of whatever inside the div of id=containerid
        textarea.value = document.getElementById(containerid).innerText;
        // Now copy whatever inside the textarea to clipboard
        var selector = document.querySelector('#t');
        selector.select();
        document.execCommand('copy');
        // Remove the textarea
        document.body.removeChild(textarea);
        alert("Your code has been copied to clipboard");
    };
}]);


