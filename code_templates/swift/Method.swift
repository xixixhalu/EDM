$FUNC $method
func $method($parameters) {
        func successCB(_ result: Any)-> Void {
            print(result)
        }
        func errorCB(_ result:Any) -> Void {
            print(result)
        }
        }
$ENDFUNC