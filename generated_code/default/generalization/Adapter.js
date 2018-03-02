// Change the url as required

var server_ip = "0.0.0.0";
var port = "2001";
var url = "http://"+server_ip+":"+port+"/";

function is_defined(x) {
    return typeof x !== 'undefined';
}

function is_object(x) {
    return Object.prototype.toString.call(x) === "[object Object]";
}

function is_array(x) {
    return Object.prototype.toString.call(x) === "[object Array]";
}

var DBAdapter = {};

// CRUD: createOne.
// "collection" must be specified by the first parameter.
// "data" must be specified as an object passed in by the second parameter.
// Example,
// collection : "table1",
// data : {"entity1" : 1}
DBAdapter.createOne = function(collection, data1) {
    alert(data1);

        var body = {
            collection : collection,
            data : JSON.stringify(data1)
        };

        ajaxCall("create", body);

};

// CRUD: createMany.
// "collection" must be specified in by the first parameter.
// "data" must be specified as an Array by the second parameter.
// Example,
// collection : "table1",
// data : [{"entity1" : 1}, {"entity2" : 2}]
DBAdapter.createMany = function(collection, data) {

        var body = {
            collection : collection,
            data : JSON.stringify(data)
        };
        ajaxCall("create", body);

};

// CRUD: ReadOne.
// "collection" must be specified in by the first parameter.
// "data" must be specified as an object by the second parameter.
// Example,
// collection : "table1",
// data : {"_id", "57d26068f2a81b5d740f695c"} or
// data : {"x" : 1234}
DBAdapter.readOne = function(collection, data) {

        var body;
        if (is_defined(data._id)) {
            body = {
                collection : collection,
                _id : data._id
            };
        } else {
            body = {
                collection : collection,
                data : JSON.stringify(data)
            };
        }
        ajaxCall("readOne", body);
};

// CRUD: readAll.
// "collection" must be specified in by the first parameter.
// "data" must be specified as an object by the second parameter.
// Example,
// collection : "table1",
// data : {"x" : 1234}
DBAdapter.readAll = function(collection, body) {

        var body = {
            collection : collection,
            data : JSON.stringify(data)
        };
        ajaxCall("readAll", body);

};

// CRUD: update.
// "collection" must be specified in by the first parameter.
// "data" must be specified as an object by the second parameter.
// Example,
// collection : "table1",
// data : {_id : "57d25c9cf2a81b5d740f6956", newData : {x:5678, y:2222}} or
// data : {oldData: {y:2222}, newData : {z:5678, y:2222}}
DBAdapter.update = function(collection, data) {

        var body;
        if (is_defined(data._id) && is_defined(data.newData) && !is_array(data.newData)) {
            body = {
                collection : collection,
                _id : data._id,
                newData: JSON.stringify(data.newData)
            };
        } else if (is_defined(data.oldData) && is_defined(data.newData) &&
            !is_array(data.oldData) && !is_array(data.newData)) {
            body = {
                collection : collection,
                oldData : JSON.stringify(data.oldData),
                newData: JSON.stringify(data.newData)
            };
        } else {
            return;
        }
        ajaxCall("update", body);
};

// CRUD: delete.
// "collection" must be specified in by the first parameter.
// "data" must be specified as an object by the second parameter.
// Example,
// collection : "table1",
// data : {"x" : [{"x":1111}, {"y":3333}]} or
// data : {"y" : 2222} or
// data : {"_id" : "57d26068f2a81b5d740f695c"}
DBAdapter.delete = function(collection, data) {

        var body;
        if (is_defined(data._id)) {
            body = {
                collection : collection,
                _id : data._id
            };
        } else {
            body = {
                collection : collection,
                data : JSON.stringify(data)
            };
        }
        ajaxCall("delete", body);
};

function ajaxCall(operation, body) {
    alert(JSON.stringify(body));

    $.ajax({
        "url": url + operation,
        "method": "POST",
        "content-Type": "application/json; charset=utf-8",
        "data": body,
        "success": function(result){
        alert("Call succeeded");
        alert(JSON.stringify(result));

        },
        "error":  function(xhr, ajaxOptions, thrownError) {

        }
    });
}






