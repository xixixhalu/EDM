var express = require('express');
var router = express.Router();



var bodyParser = require('body-parser');
var primary_key = '_id';


var dbOps = require("./dbOps.js");
var authen = require("./authen.js");
// CRUD: Create
router.post('/create', function (req, res) {
    if (typeof(req.body.collection) !== 'undefined' &&
        typeof(req.body.data) !== 'undefined') {
        authen.process(req, 1, function(result, error) {
            if (error == 0)
            {
                res.send(result);
            }
            else if (error == 1)
            {
                res.sendStatus(500);
            }
            else
            {
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
    authen.process(req, 2, function(result, error) {
            if (error == 0)
            {
                res.send(result);
            }
            else if (error == 1)
            {
                res.sendStatus(500);
            }
            else
            {
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
    authen.process(req, 3, function(result, error) {
        if (error == 0)
        {
            res.send(result);
        }
        else if (error == 1)
        {
            res.sendStatus(500);
        }
        else
        {
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
    authen.process(req, 4, function(result, error) {
        if (error == 0)
        {
            res.send(result);
        }
        else if (error == 1)
        {
            res.sendStatus(500);
        }
        else
        {
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
    authen.process(req, 5, function(result, error) {
        if (error == 0)
        {
            res.send(result);
        }
        else if (error == 1)
        {
            res.sendStatus(500);
        }
        else
        {
            res.send("Invalid Authentication");
        }
    });
});

module.exports = router;

