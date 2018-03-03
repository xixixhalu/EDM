import com.google.gson.JsonObject;


public class $model {

    public static String className = "$model";
    public static String[] attributes = {
        $attributes
    };

    $FUNC readOne
    public static void readOne(JsonObject data) {
        class readOneCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        readOneCB CBModel = new readOneCB();
        Adapter.readOne(className, data, CBModel);
    }
    $ENDFUNC

    $FUNC readAll
    public static void readAll(JsonObject data) {
        class readAllCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        readAllCB CBModel = new readAllCB();
        Adapter.readAll(className, data, CBModel);
    }
    $ENDFUNC


    $FUNC create
    public static void create(JsonObject data) {
        class createCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createCB CBModel = new createCB();
        Adapter.create(className, data, CBModel);
    }
    $ENDFUNC


    $FUNC update
    public static void update(JsonObject data) {
        class updateCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        updateCB CBModel = new updateCB();
        Adapter.update(className, data, CBModel);
    }
    $ENDFUNC


    $FUNC delete
    public static void delete(JsonObject data) {
        class deleteCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        deleteCB CBModel = new deleteCB();
        Adapter.delete(className, data, CBModel);
    }
    $ENDFUNC

}
