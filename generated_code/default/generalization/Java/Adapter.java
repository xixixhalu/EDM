import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.concurrent.FutureCallback;
import org.apache.http.impl.nio.client.CloseableHttpAsyncClient;
import org.apache.http.impl.nio.client.HttpAsyncClients;
import org.apache.http.message.BasicNameValuePair;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;


public class Adapter {
    private static String serverIP = "0.0.0.0";
    private static String port = "2000";
    //static String serverUrl = "https://httpbin.org/post";
    private static String serverUrl = "http://" + serverIP + ":" + port + "/";
    //private static CloseableHttpClient httpClient = HttpClients.createDefault();
    private static CloseableHttpAsyncClient httpAsyncClient = HttpAsyncClients.createDefault();

    static {
        httpAsyncClient.start();
    }

private static List<NameValuePair> basicDataArgs(JsonObject data) {
        if(data == null)
            throw new NullPointerException("data cannot be Null");
        String dataStr = data.toString();
        List<NameValuePair> dataArgs = new ArrayList<NameValuePair>();
        if(data.has("_id")) {
            dataArgs.add(new BasicNameValuePair("_id", data.get("_id").getAsString()));
        }
        else {
            dataArgs.add(new BasicNameValuePair("data", dataStr));
        }
        return dataArgs;
    }

    private static List<NameValuePair> basicDataArgs(JsonArray data) {
        if(data == null)
            throw new NullPointerException();
        String dataStr = data.toString();
        List<NameValuePair> dataArgs = new ArrayList<NameValuePair>();
        dataArgs.add(new BasicNameValuePair("data", dataStr));
        return dataArgs;
    }

    public static void readOne(String collection, JsonObject data, Object CBModel) {
        List<NameValuePair> dataArgs = basicDataArgs(data);
        callServer(collection, "readOne", dataArgs, CBModel);
    }

    public static void readAll(String collection, JsonObject data, Object CBModel) {
        List<NameValuePair> dataArgs = basicDataArgs(data);
        callServer(collection, "readAll", dataArgs, CBModel);
    }

    public static void create(String collection, JsonObject data, Object CBModel){
        List<NameValuePair> dataArgs = basicDataArgs(data);
        callServer(collection, "create", dataArgs, CBModel);
    }

    public static void create(String collection, JsonArray data, Object CBModel){
        List<NameValuePair> dataArgs = basicDataArgs(data);
        callServer(collection, "create", dataArgs, CBModel);
    }

    public static void update(String collection, JsonObject data, Object CBModel){
        if (!data.has("newData")) {
            throw new IllegalArgumentException("lack key 'newData' in data");
        }
        List<NameValuePair> params = new ArrayList<NameValuePair>();
        if(data.has("_id")) {
            params.add(new BasicNameValuePair("_id", data.get("_id").getAsString()));
        }
        else if(data.has("oldData")){
            params.add(new BasicNameValuePair("oldData", data.get("oldData").toString()));
        }
        else {
            throw new IllegalArgumentException("lack key '_id' or 'oldData' in data");
        }
        params.add(new BasicNameValuePair("newData", data.get("newData").toString()));
        callServer(collection, "update", params, CBModel);
    }

    public static void delete(String collection, JsonObject data, Object CBModel){
        List<NameValuePair> dataArgs = basicDataArgs(data);
        callServer(collection, "delete", dataArgs, CBModel);
    }

    public static void callServer(String collection, String operation, List<NameValuePair> params, Object CBModel){
        String url = serverUrl + operation;
        params.add(new BasicNameValuePair("collection", collection));
        PostCall(url, params, CBModel);
    }

    //java.io.UnsupportedEncodingException
    public static void PostCall(String url, List<NameValuePair> params, Object CBModel){
        Method successM, errorM;
        try {
            successM = CBModel.getClass().getMethod("successCB", String.class);
            errorM = CBModel.getClass().getMethod("errorCB", String.class);
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
            return;
        }

        HttpPost post = new HttpPost(url);
        post.setHeader("Content-Type", "application/x-www-form-urlencoded; charset=utf-8");

        if (params != null) {
//            StringEntity params = null;
//            try {
//                params = new StringEntity(data.toString());
//            } catch (UnsupportedEncodingException e) {
//                e.printStackTrace();
//            }
//            post.setEntity(params);
            try {
                post.setEntity(new UrlEncodedFormEntity(params,"utf-8"));
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
        httpAsyncClient.execute(post, new FutureCallback<HttpResponse>() {
            @Override
            public void completed(HttpResponse result) {
                try {
                    String s = new BufferedReader(new InputStreamReader(result.getEntity().getContent()))
                            .lines().collect(Collectors.joining(System.lineSeparator()));
                    successM.invoke(CBModel, s);
                } catch (IllegalAccessException | InvocationTargetException | IOException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void failed(Exception ex) {
                try {
                    errorM.invoke(CBModel, ex.getMessage());
                } catch (IllegalAccessException | InvocationTargetException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void cancelled() {
                try {
                    errorM.invoke(CBModel, "cancelled");
                } catch (IllegalAccessException | InvocationTargetException e) {
                    e.printStackTrace();
                }
            }
        });

    }


}
