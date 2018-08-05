class class2 {

// attributes: {"class2attribute1"}
var tableName = "class2"

func createOne(data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.createOne(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}

func createMany(data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.createMany(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}

func readOne(data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.readOne(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}

func readMany(data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.readMany(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}

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

func delete(data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adapter.delete(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
}



}