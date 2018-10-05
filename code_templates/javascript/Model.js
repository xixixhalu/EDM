
var $model = {};

$model.name = "$name";              // Model name

$model.attributes = [            // Model attribute list
    $attributes
];

// Model functions

$FUNC create
{ just test
lalala
}
// "data" : the Object or the Array of Objects to be created 
//          specifies the value of each attirbute in $name
$model.create = function(data, success, error) {
    // Wrap data

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.create($model.name, data, successCB, errorCB);
};
$ENDFUNC


$FUNC get
// "id" : the ObjectId of $name, must be 24 character hex string 
$model.get = function(id, success, error) {
    // Wrap data
    var data = id;

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.get($model.name, data, successCB, errorCB);
};
$ENDFUNC

$FUNC readMany
// "data" : the Object that specifies the attribute-values to be queried
$model.read = function(data, success, error) {
    // Wrap data

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.read($model.name, data, successCB, errorCB);
};
$ENDFUNC

$FUNC update
// "id" : the ObjectId of $name, MUST be 24 character hex string
// "data" : the Object to be modified, specifies the attribute-values to be updated
$model.update = function(id, update, success, error) {
    // Wrap data
    var data = {
        "_id" : id,
        "newData" : update
    };

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.update($model.name, data, successCB, errorCB);
};
$ENDFUNC

$FUNC delete
// "data" : the Object that specifies the attribute-values to be queried and then deleted
$model.delete = function(data, success, error) {
    // Wrap data 

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.delete($model.name, data, successCB, errorCB);
};
$ENDFUNC

$FUNC set
// "id" : the ObjectId of $name, MUST be 24 character hex string
// "data" : the Object to be replaced, specifies the value of each attirbute in $name
$model.set = function(id, newData, success, error) {
    // Wrap data
    var data = {"_id" : id, "newData" : newData};

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.update($model.name, data, successCB, errorCB);
};
$ENDFUNC

// Add the other functions here

$methods
