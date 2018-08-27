import com.google.gson.JsonObject;


public class class2 {

    public static String className = "class2";
    public static String[] attributes = {
        "class2Attribute2", "class2Attribute1"
    };

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
    


}
