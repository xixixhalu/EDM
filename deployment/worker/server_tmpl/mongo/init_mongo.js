db.auth('admin-user','admin-pwd')
db = db.getSiblingDB('Composition')

//role set to readWrite, cannot use dbAdmin now, will raise "not authorized" when operate db as the new user
db.createUser({
        user:"Composition_user",
        pwd:"Composition_pwd",
        roles:[{
                role:"readWrite",
                db:"Composition"
        }]
})

db.auth('Composition_user','Composition_pwd')
