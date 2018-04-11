class $model {

// attributes: {$attributes}
var tableName = "$model"

$FUNC createOne
func createOne(data: JSON) {
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
func createMany(data: JSON) {
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
func readOne(data: JSON) {
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
func readMany(data: JSON) {
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
func update(search: JSON, update: JSON) {
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
func delete(data: JSON) {
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