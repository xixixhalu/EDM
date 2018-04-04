
var $model = {};

$model.name = "$name";              // Model name

$model.attributes = [            // Model attribute list
    $attributes
];

// Model functions

$FUNC createOne
{ just test
lalala
}
$model.createOne = function(data, success, error) {
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

    DBAdapter.createOne($model.name, data, successCB, errorCB);
};
$ENDFUNC

$FUNC createMany
$model.createMany = function(data, success, error) {
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

    DBAdapter.createMany($model.name, data, successCB, errorCB);
};
$ENDFUNC

$FUNC readOne
$model.readOne = function(data, success, error) {
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

    DBAdapter.readOne($model.name, data, successCB, errorCB);
};
$ENDFUNC

$FUNC readMany
$model.readMany = function(data, success, error) {
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

    DBAdapter.readMany($model.name, data, successCB, errorCB);
};
$ENDFUNC

$FUNC update
$model.update = function(search, update, success, error) {
    // Wrap data
    var data = {
        oldData : search,
        newData : update
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

$model.get = function(id, success, error) {
    // Wrap data
    var data = {"_id" : id};

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.readOne($model.name, data, successCB, errorCB);
};

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

// Add the other functions here

$methods
