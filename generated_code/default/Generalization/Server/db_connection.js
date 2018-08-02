var mongodb = require('mongodb');

/*
 Initialize a connection to the MongoDB
 change the IP and keyspace so that it is according to your setting.
 */
var db_server = 'localhost:27017';
var db_name = "Generalization"
var db_user = "Generalization_user";
var db_password = "Generalization_pwd";

//USE BELOW URL ONCE BDR ACCOUNT IS SETUP IN MONGODB
//var url = 'mongodb://' + keyspace + ':' + keyspace + '@' + db_server + '/' + keyspace + '?authMechanism=DEFAULT&authSource=' + keyspace + '&maxPoolSize=50';
var url = "mongodb://"+db_user+":"+db_password+"@"+ db_server + "/" + db_name;

var Wrapper = function() {
    this.init();
};

Wrapper.prototype.init = function() {
    var wrapper = this;
    mongodb.MongoClient.connect(url, function (err, database) {
        if (err) {
            console.log(err);
        } else {
            console.log('Connected successfully to database');
            wrapper.db = database;
        }
    });
};

module.exports = new Wrapper();
