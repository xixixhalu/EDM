var http = require('http');
var querystring = require('querystring');
var bodyParser = require('body-parser');
var primary_key = '_id';

var dbOps = require("./dbOps.js");

var authen = {};

authen.verify = function(req, onResult) {
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
                onResult(true, 0);
            }
            else
            {
                onResult(null, 1);
            }
        });
      }).write(postData);
};
module.exports = authen;
