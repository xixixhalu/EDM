package $NAMESPACE;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.concurrent.FutureCallback;
import org.apache.http.impl.nio.client.CloseableHttpAsyncClient;
import org.apache.http.impl.nio.client.HttpAsyncClients;
import org.apache.http.message.BasicNameValuePair;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;


public class Adapter {
    private static String serverIP = "$server_ip";
    private static String port = "$port";
    private static String dmName = "$dm_name";

    private static String serverUrl = "http://" + serverIP + ":" + port + "/" + dmName + "/";
    private static CloseableHttpAsyncClient httpAsyncClient = HttpAsyncClients.createDefault();


    public interface ApiCallback {
        void success(String js);

        void error(String err);
    }


    static {
        httpAsyncClient.start();
    }

    $FUNC Adapter

    private static List<NameValuePair> basicDataArgs(JsonObject data) {
        String dataStr = data.toString();
        List<NameValuePair> dataArgs = new ArrayList<NameValuePair>();
        if (data.has("_id")) {
            dataArgs.add(new BasicNameValuePair("_id", data.get("_id").getAsString()));
        } else {
            dataArgs.add(new BasicNameValuePair("data", dataStr));
        }
        return dataArgs;
    }

    private static List<NameValuePair> basicDataArgs(JsonArray data) {
        String dataStr = data.toString();
        List<NameValuePair> dataArgs = new ArrayList<NameValuePair>();
        dataArgs.add(new BasicNameValuePair("data", dataStr));
        return dataArgs;
    }

    public static void readOne(String collection, JsonObject data, ApiCallback callback) {
        List<NameValuePair> dataArgs = basicDataArgs(data);
        GetCall(serverUrl + collection + "/readOne", callback);
    }

    public static void readMany(String collection, JsonObject data, ApiCallback callback) {
        List<NameValuePair> dataArgs = basicDataArgs(data);
        GetCall(serverUrl + collection, callback);
    }

    public static void createOne(String collection, JsonObject data, ApiCallback callback) {
        List<NameValuePair> dataArgs = basicDataArgs(data);
        callServer(collection, "create", dataArgs, callback);
    }

    public static void createMany(String collection, JsonArray data, ApiCallback callback) {
        List<NameValuePair> dataArgs = basicDataArgs(data);
        callServer(collection, "create", dataArgs, callback);
    }

    public static void update(String collection, JsonObject data, ApiCallback callback) {
        if (!data.has("newData")) {
            throw new IllegalArgumentException("data must contain a key called 'newData'");
        }
        List<NameValuePair> params = new ArrayList<NameValuePair>();
        if (data.has("_id")) {
            params.add(new BasicNameValuePair("_id", data.get("_id").getAsString()));
        } else if (data.has("oldData")) {
            params.add(new BasicNameValuePair("oldData", data.get("oldData").toString()));
        } else {
            throw new IllegalArgumentException("lack key '_id' or 'oldData' in data");
        }
        params.add(new BasicNameValuePair("newData", data.get("newData").toString()));
        callServer(collection, "update", params, callback);
    }

    public static void delete(String collection, JsonObject data, ApiCallback callback) {
        List<NameValuePair> dataArgs = basicDataArgs(data);
        callServer(collection, "delete", dataArgs, callback);
    }

    public static void callServer(String collection, String operation, List<NameValuePair> params, ApiCallback callback) {
        String url = serverUrl + operation;
        params.add(new BasicNameValuePair("collection", collection));
        PostCall(url, params, callback);
    }

    public static void GetCall(String url, ApiCallback callback) {
        HttpGet get = new HttpGet(url);
        get.setHeader("Accept", "application/json");
        httpAsyncClient.execute(get, responseHandler(callback));
    }

    public static void PostCall(String url, List<NameValuePair> params, ApiCallback callback) {
        HttpPost post = new HttpPost(url);
        post.setHeader("Content-Type", "application/x-www-form-urlencoded; charset=utf-8");

        if (params != null) {
            try {
                post.setEntity(new UrlEncodedFormEntity(params, "utf-8"));
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
        httpAsyncClient.execute(post, responseHandler(callback));
    }

    private static FutureCallback<HttpResponse> responseHandler(ApiCallback callback) {
        return new FutureCallback<HttpResponse>() {
            @Override
            public void completed(HttpResponse result) {
                try {
                    String s = new BufferedReader(new InputStreamReader(result.getEntity().getContent()))
                            .lines().collect(Collectors.joining(System.lineSeparator()));
                    callback.success(s);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void failed(Exception ex) {
                try {
                    callback.error(ex.getMessage());
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void cancelled() {
                try {
                    callback.error("cancelled");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        };
    }

    $ENDFUNC

}
