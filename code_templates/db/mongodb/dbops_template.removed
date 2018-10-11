
var wrapper = require("./db_connection.js");
var mongodb = require('mongodb');

var dbOps = {};

var primary_key = '_id';
dbOps.create = function(collection, data, onResult) {
	if (Array.isArray(data)) {
		wrapper.db.collectoin(collection).insertMany(data, {w: 1}, function (err, result) {
        	if (err) {
                onResult(null);
            }
            else {
            	onResult(result);
        	}
    	});
	} else {
		wrapper.db.collection(collection).insertOne(data, {w: 1}, function (err, result) {
			if (err) {
				onResult(null);
			}
			else {
				onResult(result);
			}
		});
	}
};

dbOps.readOne = function(collection, _id, data, onResult) {
	if (typeof(_id) !== 'undefined') {
    	var query = {};
        query[primary_key] = new ObjectId(_id);
        wrapper.db.collection(collection).find(query).next(function (err, result) {
            if (err) {
                onResult(null);
            }
            else {
                onResult(result);
            }
        });
    } else if (typeof(data) !== 'undefined') {
        var data = JSON.parse(data);
        wrapper.db.collection(collection).find(data).next(function (err, result) {
            if (err) {
                onResult(null);
            }
            else {
                onResult(result);
            }
      	});
    }
};

dbOps.readAll = function(collection, data, onResult) {
	wrapper.db.collection(collection).find(data).toArray(function (err, result) {
        if (err) {
            onResult(null);
        }
        else {
            onResult(result);
        }
    });
}

dbOps.delete = function(collection, _id, data, onResult) {
	if (typeof(_id) !== 'undefined') {
        // Remove one document by _id
        var query = {};
        query[primary_key] = new ObjectId(_id);
        wrapper.db.collection(collection).removeOne(query, {w: 1}, function (err, result) {
            if (err) {
                onResult(null);
            }
            else {
                onResult(result);
            }
        });
    } else if (typeof(data) !== 'undefined') {
        // Remove several documents with same key-value pair
        var data = JSON.parse(data);

        wrapper.db.collection(collection).removeMany(data, {w: 1}, function (err, result) {
            if (err) {
                onResult(null);
            }
            else {
                onResult(result);
            }
        });
	}
};

dbOps.update = function(collection, _id, newData, oldData, onResult) {
	if (typeof(_id) !== 'undefined') {
        // update one document by _id
        var query = {};
        query[primary_key] = new ObjectId(_id);
        wrapper.db.collection(collection).updateOne(query, {$set: newData}, {w: 1}).then(function (result) {
            onResult(result);
        });
    } else if (typeof(oldData) !== 'undefined') {
        // Remove several documents with same key-value pair
        // var data = JSON.parse(req.body.oldData);
        wrapper.db.collection(collection).updateMany(oldData, {$set: newData}, {
            upsert: true,
            w: 1
        }).then(function (result) {
            onResult(result);
        });
    }
};

module.exports = dbOps;
