class Class3 {

// attributes: {}

func createOne(tableName: String, data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adpter.createOne(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
        }

func delete(tableName: String, data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adpter.delete(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
        }

func readOne(tableName: String, data: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adpter.readOne(tableName: tableName, data: data, successCB: successCB, errorCB: errorCB)
    }

func update(tableName: String, update: JSON) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        adpter.update(tableName: collection, data: update, successCB: successCB, errorCB: errorCB)
    }

}