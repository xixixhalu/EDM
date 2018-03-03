
var Class3 = {};

Class3.name = "Class3";              // Model name

Class3.attributes = [            // Model attribute list
    
];

// Model functions


Class3.create = function(data, success, error) {
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

    DBAdapter.createOne(Class3.name, data, successCB, errorCB);
};

Class3.read = function(data, success, error) {
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

    DBAdapter.readOne(Class3.name, data, successCB, errorCB);
};

Class3.update = function(search, update, success, error) {
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

    DBAdapter.update(Class3.name, data, successCB, errorCB);
};

Class3.delete = function(data, success, error) {
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

    DBAdapter.delete(Class3.name, data, successCB, errorCB);
};

Class3.get = function(id, success, error) {
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

    DBAdapter.readOne(Class3.name, data, successCB, errorCB);
};

Class3.set = function(id, newData, success, error) {
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

    DBAdapter.update(Class3.name, data, successCB, errorCB);
};

// Add the other functions here

// 
