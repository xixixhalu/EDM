//use angularJS to help implement the reference page ---- // Xuan Zhu
var app = angular.module('myApp', []);
app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {
    //$scope.classes is used to store all the classes generated when the data is loaded:
    $scope.classes = [];
    //$scope.details is used to store all the source code data
    $scope.details = [];
    //$scope.languages is used to store all the languages
    $scope.languages = [];

    //control the display of each class
    $scope.changeParentTab = function(tab) {
        $scope.view_tab = tab;
    };
    //control the display of each tab based on the class and language information
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
            //dymically load the classes info to classes array
            $scope.classes.push(key);
        });
    //});

    //this is used to split the source code of the data and store in an array
    //used the array in html page to generate the content of each span element
    $scope.generateView = function (data) {
        result = [];
        result = data.split(/\r?\n/);
        return result;
    }

    //This function is used to copy the code to clipboard:
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
        //Remind that you have successfully copied the code to clipboard
        alert("Your code has been copied to clipboard");
    };
}]);


