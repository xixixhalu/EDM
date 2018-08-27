//FOR MongoDB

/*
 Configure the variables below
 */
var server_ip = "127.0.0.1";
var dbname = "Generalization";
var server_port = "2000";
//declare what is the primary key for the table specified above.
var primary_key = '_id';

var collection_names = ['class2', 'class3', 'class1'];


/*
 Required node module
 */
var mongodb = require('mongodb');
var express = require('express');
var bodyParser = require('body-parser');
var client = mongodb.MongoClient;
var ObjectId = mongodb.ObjectId;

//using express for RESTful communcation
var app = express();
//bodyparser is used to get the data from the body of POST/GET method
// for urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// for json 
app.use(bodyParser.json());

//if you do not include the path in the node itself (pure rest from front end to backend) you need this below
app.use(function (req, res, next) {

    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', '*');

    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});

// end point: http://host:port/dbname/collection_name/crud_operation
for (var i = 0; i < collection_names.length; i++)
{
    var class_name = collection_names[i];
    var class_model = require('./' + class_name + '.js');
    app.use('/' + dbname + '/' + class_name, class_model);
}

//Server is running in port 9001; REST API should call ex. localhost:9001/readoneData etc...
var server = app.listen(server_port, server_ip, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log("App listening at http://%s:%s", host, port)
});
