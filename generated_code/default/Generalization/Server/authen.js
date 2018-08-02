var http = require('http');
var querystring = require('querystring');
var bodyParser = require('body-parser');
var primary_key = '_id';

var dbOps = require("./dbOps.js");

var authen = {};


authen.process = function(req, requesttype, onResult) {
	var data = JSON.parse(req.body.data);
    var collection = req.body.collection;
    var postData = querystring.stringify({
            username: req.body.username,
            key: req.body.key
        });
    var headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': postData.length
        };
    var options = {
        host: 'localhost',
        port: 4000,
        path: '/verifykey',
        method: 'POST',
        headers: headers
    };
    http.request(options, function(verif_result) {
            var verification = '';
            verif_result.on('data', function(chunk){
                verification += chunk;
            });
            verif_result.on('end', function() {
                var obj = JSON.parse(verification);
            if (obj.valid === true)
         	{
            	if (requesttype == 1)
            	{
            		var data = JSON.parse(req.body.data);
        			var collection = req.body.collection;
	                dbOps.create(collection, data, function(result) {
		                if (!result) 
		                {
		                    onResult(null, 1);
		                }
		                else 
		                {
		                    onResult(result, 0);
		                }
		            });
            	}
            	else if (requesttype == 2)
            	{
            		var collection = req.body.collection;
    				var _id = req.body._id;
    				var data = JSON.parse(req.body.data);
    				dbOps.readOne(collection, _id, data, function(result) {
	        			if (!result) 
	        			{
	        				onResult(null, 1);
	        			}
	        			else 
	        			{
	            			onResult(result, 0);
	        			}
    				});
            	}
            	else if (requesttype == 3)
            	{
            		var collection = req.body.collection;
    				var data;
    				if (typeof(req.body.data) === 'undefined')
        				data = {};
    				else
        				data = JSON.parse(req.body.data);
        			dbOps.readAll(collection, data, function(result) {
        				if (!result) 
        				{
            				onResult(null, 1);
        				}
        				else 
        				{
            				onResult(result, 0);
        				}
    				});
            	}
            	else if (requesttype == 4)
            	{
            		var collection = req.body.collection;
    				var _id = req.body._id;
    				var data = JSON.parse(req.body.data);
    				dbOps.delete(collection, _id, data, function(result) {
	        			if (!result) 
	        			{
	            			onResult(null, 1);
	        			}
	        			else 
	        			{
	            			onResult(result, 0);
	        			}
    				});
            	}
            	else if (requesttype == 5)
            	{
            		var collection = req.body.collection;
    				var _id = req.body._id;
    				var newData = JSON.parse(req.body.newData);
    				var oldData = JSON.parse(req.body.oldData);
    				dbOps.update(collection, _id, newData, oldData, function(result) {
        				onResult(result, 0);
    				});
            	}
            }
            else
            {
                onResult(null, 2);
            }
        });
      }).write(postData);
};


module.exports = authen;