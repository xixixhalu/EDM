class $model {

// attributes: {$attributes}

$FUNC createOne
func createOne(tableName: String, data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.createOne(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}
$ENDFUNC

$FUNC createMany
func createMany(tableName: String, data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.createMany(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}
$ENDFUNC

$FUNC readOne
func readOne(tableName: String, data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.readOne(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}
$ENDFUNC

$FUNC readMany
func readMany(tableName: String, data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.readMany(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}
$ENDFUNC

$FUNC update
func update(tableName: String, search: JSON, update: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        let data = ["oldData": search, "newData": update]
        adapter.update(tableName: collection, data: update, successCB: successCB, errorCB: errorCB)
}
$ENDFUNC

$FUNC delete
func delete(tableName: String, data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.delete(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}
$ENDFUNC

$methods

}