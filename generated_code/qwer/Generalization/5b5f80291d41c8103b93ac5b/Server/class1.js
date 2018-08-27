var express = require('express');
var router = express();

var bodyParser = require('body-parser');
var primary_key = '_id';

var dbOps = require("./dbOps.js");
var authen = require("./authen.js");
// CRUD: Create
router.post('/create', function (req, res) {
    if (typeof(req.body.collection) !== 'undefined' &&
        typeof(req.body.data) !== 'undefined') {
        authen.verify(req, function(result, error) {
            if (error == 0)
            {
                var data = JSON.parse(req.body.data);
                var collection = req.body.collection;

                //DB create
                dbOps.create(collection, data, function(result) {
                    if (!result) 
                    {
                        res.send(null);
                    }
                    else 
                    {
                        res.send(result);
                    }
                });
                
            }else if (error == 1)
            {
                res.sendStatus(500);
            }else{
                res.send("Invalid Authentication");
            }
        });
    }
});

//CRUD: ReadOne
//TODO: make sure the data is returned in JSON format
router.post('/readOne', function (req, res) {
    if (typeof(req.body.collection) === 'undefined') {
        res.send({});
        return;
    }

    authen.verify(req, function(result, error) {
        if (error == 0)
        {
            var collection = req.body.collection;
            if(req.body.hasOwnProperty('data')){
                var data = JSON.parse(req.body.data);
            }
            if(req.body.hasOwnProperty('_id')){
                var _id = req.body._id;
            }

            //DB readOne
            dbOps.readOne(collection, _id, data, function(result) {
                if (!result) 
                {
                    res.send(null);
                }
                else 
                {
                    res.send(result);
                }
            });        
        }else if (error == 1)
        {
            res.sendStatus(500);
        }else{
            res.send("Invalid Authentication");
        }
    });

});

//CRUD: ReadAll
//TODO: make sure the data is returned in JSON format
router.post('/readAll', function (req, res) {
    if (typeof(req.body.collection) === 'undefined') {
        res.send([]);
        return;
    }
    authen.verify(req, function(result, error) {
        if (error == 0)
        {
            var collection = req.body.collection;
            if(req.body.hasOwnProperty('data')){
                var data = JSON.parse(req.body.data);
            }

            //DB readAll
            dbOps.readAll(collection, data, function(result) {
                if (!result) 
                {
                    res.send(null);
                }
                else 
                {
                    res.send(result);
                }
            });      

        }else if (error == 1)
        {
            res.sendStatus(500);
        }else{
            res.send("Invalid Authentication");
        }
    });

});

//CRUD: Delete
router.delete('/delete', function (req, res) {
    if (typeof(req.body.collection) === 'undefined') {
        res.send();
        return;
    }
    authen.verify(req, function(result, error) {
        if (error == 0)
        {
            var collection = req.body.collection;
            if(req.body.hasOwnProperty('data')){
                var data = JSON.parse(req.body.data);
            }
            if(req.body.hasOwnProperty('_id')){
                var _id = req.body._id;
            }

            //DB delete
            dbOps.delete(collection, _id, data, function(result) {
                if (!result) 
                {
                    res.send(null);
                }
                else 
                {
                    res.send(result);
                }
            });

        }else if (error == 1)
        {
            res.sendStatus(500);
        }else{
            res.send("Invalid Authentication");
        }
    });

});

//CRUD: Update
router.put('/update', function (req, res) {
    if (typeof(req.body.collection) === 'undefined' ||
        typeof(req.body.newData) === 'undefined') {
        res.send();
        return;
    }
    authen.verify(req, function(result, error) {
        if (error == 0)
        {
            var collection = req.body.collection;
            var newData = JSON.parse(req.body.newData);

            if(req.body.hasOwnProperty('oldData')){
                var oldData = JSON.parse(req.body.oldData);
            }

            if(req.body.hasOwnProperty('_id')){
                var _id = req.body._id;
            }

            //DB update
            dbOps.update(collection, _id, newData, oldData, function(result) {
                    res.send(result);
            });


        }else if (error == 1)
        {
            res.sendStatus(500);
        }else{
            res.send("Invalid Authentication");
        }
    });

});

module.exports = router;

