import Foundation
import SwiftyJSON
import Alamofire

protocol AnyTypeOfArray {}
extension Array: AnyTypeOfArray {}
extension NSArray: AnyTypeOfArray {}

class Adapter {
    //var url = "http://localhost:3000"
    var url = "http://127.0.0.1:2001/"
    let headers: HTTPHeaders = [
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    ]

    func isArray(data: Any) -> Bool {
        return data is AnyTypeOfArray
    }

func callServer(_ operation: String, _ body: Dictionary<String, Any>, _ successCB:@escaping (_ result: Any)-> Void,_ errorCB: @escaping (_ result: Any) -> Void) {
        Alamofire.request(url + operation, method: .post, parameters: body, headers: headers)
            .responseJSON { dataResponse in
                switch dataResponse.result {
                case .success:
                    successCB(dataResponse.result)
                    successCB(dataResponse.response as Any)
                    successCB(dataResponse.value as Any)
                case .failure:
                    errorCB(dataResponse.error as Any)
                }
        }
    }

    func createOne(tableName collection: String, data:JSON, successCB: @escaping (_ result: Any)-> Void, errorCB: @escaping (_ result: Any) -> Void ) {
        if data != JSON.null && !collection.isEmpty && !isArray(data: data) {
            let body = ["collection": collection, "data": String(describing:data)]
            callServer("/create", body, successCB, errorCB)
        } else {
            errorCB("Error:" + "Invalid Parameter")
        }
    }

    // TODO test
    func createMany(tableName collection: String, data:JSON, successCB: @escaping (_ result: Any)-> Void, errorCB: @escaping (_ result: Any) -> Void ) {
        if data != JSON.null && !collection.isEmpty && isArray(data: data) {
            let body = ["collection": collection, "data": String(describing:data)]
            callServer("/create", body, successCB, errorCB)
        } else {
            errorCB("Error:" + "Invalid Parameter")
        }
    }

    func readOne(tableName collection: String, data:JSON, successCB: @escaping (_ result: Any)-> Void, errorCB: @escaping (_ result: Any) -> Void ) {
        if data != JSON.null && !collection.isEmpty {
            if data["._id"] != JSON.null {
                let body = ["collection": collection, "_id": String(describing:data["._id"])]
                callServer("/readOne", body, successCB, errorCB)
            } else {
                let body = ["collection": collection, "data": String(describing:data)]
                callServer("/readOne", body, successCB, errorCB)
            }
        } else {
            errorCB("Error:" + "Invalid Parameter")
        }
    }

    func readMany(tableName collection: String, data:JSON, successCB: @escaping (_ result: Any)-> Void, errorCB: @escaping (_ result: Any) -> Void ) {
        if data != JSON.null && !collection.isEmpty {
            let body = ["collection": collection, "data": String(describing:data)]
            callServer("/readOne", body, successCB, errorCB)
        } else {
            errorCB("Error:" + "Invalid Parameter")
        }
    }

    func update(tableName collection: String, data:JSON, successCB: @escaping (_ result: Any)-> Void, errorCB: @escaping (_ result: Any) -> Void ) {
        if data != JSON.null && !collection.isEmpty && data["newData"] != JSON.null && !isArray(data: data["newData"])  {
            if data["._id"] != JSON.null {
                let body = ["collection": collection, "_id": String(describing:data["._id"]), "newData": String(describing:data["newData"])]
                callServer("update", body, successCB, errorCB)
            } else if data["oldData"] != JSON.null && isArray(data: data["oldData"]){
                let body = ["collection": collection, "oldData": String(describing: data["oldData"]), "newData": String(describing: data["newData"])]
                callServer("/update", body, successCB, errorCB)
            }
        } else {
            errorCB("Error:" + "invalid parameters")
        }
    }

    func delete(tableName collection: String, data:JSON, successCB: @escaping (_ result: Any)-> Void, errorCB: @escaping (_ result: Any) -> Void ) {
        if data != JSON.null && !collection.isEmpty {
            if data["._id"] != JSON.null {
                let body = ["collection": collection, "_id": String(describing:data["._id"])]
                callServer("/delete", body, successCB, errorCB)
            } else {
                let body = ["collection": collection, "data": String(describing:data)]
                callServer("/delete", body, successCB, errorCB)
            }
        } else {
             errorCB("Error:" + "invalid parameters")
        }
    }
}
