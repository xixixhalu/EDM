import com.google.gson.JsonObject;


public class Class1 {

    public static String className = "Class1";
    public static String[] attributes = {
        "class1Attribute1"
    };

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
