package $NAMESPACE;

import com.google.gson.JsonObject;

import java.io.IOException;

import org.apache.http.client.ClientProtocolException;

import com.google.gson.JsonElement;

public class $model {
    public static String className = "$model";
    public static String[] attributes = {
        $attributes
    };
    
    $FUNC creat
    public static void create(JsonElement data) {
        class createManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createManyCB CBModel = new createManyCB();
        Adapter.create(className, data, CBModel);
    }
    $ENDFUNC
    
    $FUNC get
    public static void get(String dataId) {
        class createManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createManyCB CBModel = new createManyCB();
        Adapter.get(className, dataId, CBModel);
    }
    $ENDFUNC

    $FUNC read
    public static void read(JsonElement value) {
        class createManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createManyCB CBModel = new createManyCB();
        Adapter.read(className, value, CBModel);
    }
    $ENDFUNC

    $FUNC set
    public static void set(String dataId, JsonElement data) {
        class createManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createManyCB CBModel = new createManyCB();
        Adapter.set(className, data, dataId, CBModel);
    }
    $ENDFUNC

    $FUNC update
    public static void update(String dataId, JsonElement data) {
        class createManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createManyCB CBModel = new createManyCB();
        Adapter.update(className, data, dataId, CBModel);
    }
    $ENDFUNC

    $FUNC delete
    public static void delete(JsonObject data) throws ClientProtocolException, IOException {
        class createManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createManyCB CBModel = new createManyCB();
        Adapter.delete(className, data, CBModel);
    }
    $ENDFUNC
    
    $FUNC delete
    //OverLoad
    public static void delete(String dataId) {
        class createManyCB {
            public void successCB(String result) {
                System.out.println("successCB: " + result);
            }
            public void errorCB(String message) {
                System.out.println("errorCB: " + message);
            }
        }
        createManyCB CBModel = new createManyCB();
        Adapter.delete(className, dataId, CBModel);
    }
    $ENDFUNC
 
$methods   
}
