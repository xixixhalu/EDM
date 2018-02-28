import com.google.gson.JsonObject;


public class $model {

    public static String className = "$model";
    public static String[] attributes = {$attributes};

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

    public static void createMany(JsonObject data) {
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
