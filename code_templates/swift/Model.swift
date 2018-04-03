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
        adpter.createOne(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
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
        adpter.delete(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
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
        adpter.readOne(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
    }
$ENDFUNC

$FUNC update
func update(tableName: String, update: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adpter.update(tableName: collection, data: update, successCB: successCB, errorCB: errorCB)
    }
$ENDFUNC

}