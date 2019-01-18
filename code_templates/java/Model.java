package $NAMESPACE;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

// $MODEL_NAME
// $DM_NAME
public class $model {

    public static String className = "$model";
    public static String[] attributes = {
        $attributes
    };

//    public $model($attributeListWithTypes) {
//        // TODO really need a foreach capability in the template
//    }

    $FUNC createOne
    public static void createOne(JsonObject data, Adapter.ApiCallback callback) {
        Adapter.createOne(className, data, callback);
    }
    $ENDFUNC

    $FUNC createMany
    public static void createMany(JsonArray data, Adapter.ApiCallback callback) {
        Adapter.createMany(className, data, callback);
    }
    $ENDFUNC

    $FUNC readOne
    public static void readOne(JsonObject data, Adapter.ApiCallback callback) {
        Adapter.readOne(className, data, callback);
    }
    $ENDFUNC

    $FUNC readMany
    public static void readMany(JsonObject data, Adapter.ApiCallback callback) {
        Adapter.readMany(className, data, callback);
    }
    $ENDFUNC

    $FUNC update
    public static void update(JsonObject searchData, JsonObject updateData, Adapter.ApiCallback callback) {
        JsonObject data = new JsonObject();
        data.add("oldData",searchData);
        data.add("newData",updateData);
        Adapter.update(className, data, callback);
    }
    $ENDFUNC

    $FUNC delete
    public static void delete(JsonObject data, Adapter.ApiCallback callback) {
        Adapter.delete(className, data, callback);
    }
    $ENDFUNC

$methods

}
