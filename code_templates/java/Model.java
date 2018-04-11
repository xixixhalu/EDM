import com.google.gson.JsonObject;


public class $model {

    public static String className = "$model";
    public static String[] attributes = {
        $attributes
    };

    $FUNC createOne
    public static void createOne(JsonObject data) {
        class createOneCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createOneCB CBModel = new createOneCB();
        Adapter.createOne(className, data, CBModel);
    }
    $ENDFUNC

    $FUNC createMany
    public static void createMany(JsonArray data) {
        class createManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createManyCB CBModel = new createManyCB();
        Adapter.createMany(className, data, CBModel);
    }
    $ENDFUNC

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

    $FUNC readMany
    public static void readMany(JsonObject data) {
        class readManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        readManyCB CBModel = new readManyCB();
        Adapter.readMany(className, data, CBModel);
    }
    $ENDFUNC

    $FUNC update
    public static void update(JsonObject searchData, JsonObject updateData) {
        class updateCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        JsonObject data = new JsonObject();
        data.add("oldData",search);
        data.add("newData",update);
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

$methods

}
