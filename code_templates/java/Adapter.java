import com.google.gson.Gson;
import com.google.gson.JsonObject;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.concurrent.FutureCallback;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
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
    private static String serverIP = "$server_ip"; 
    private static String port = "$port"; 
    //static String serverUrl = "https://httpbin.org/post";
    private static String serverUrl = "http://" + serverIP + ":" + port + "/";
    //private static CloseableHttpClient httpClient = HttpClients.createDefault();
    private static CloseableHttpAsyncClient httpAsyncClient = HttpAsyncClients.createDefault();

    static {
        httpAsyncClient.start();
    }

    public static void readOne(String collection, JsonObject data, Object CBModel) {
        callServer(collection, "readOne", data, CBModel);
    }

    public static void readAll(String collection, JsonObject data, Object CBModel) {
        callServer(collection, "readAll", data, CBModel);
    }

    public static void createOne(String collection, JsonObject data, Object CBModel){
        callServer(collection, "create", data, CBModel);
    }

    public static void createMany(String collection, JsonObject data, Object CBModel){
        callServer(collection, "create", data, CBModel);
    }

    public static void update(String collection, JsonObject data, Object CBModel){
        if (!data.has("newData")) {
            return; //TODO more conditions
        }
        List<NameValuePair> params = new ArrayList<NameValuePair>();
        params.add(new BasicNameValuePair("collection", collection));
        if(data.has("_id")) {
            params.add(new BasicNameValuePair("_id", data.get("_id").getAsString()));
        }
        else if(data.has("oldData")){
            params.add(new BasicNameValuePair("oldData", data.get("oldData").toString()));
        }
        params.add(new BasicNameValuePair("newData", data.get("newData").toString()));

        callServer("update", params, CBModel);
    }

    public static void delete(String collection, JsonObject data, Object CBModel){
        callServer(collection, "delete", data, CBModel);
    }

    public static void callServer(String operation, List<NameValuePair> params, Object CBModel){
        String url = serverUrl + operation;
        PostCall(url, params, CBModel);
    }

    public static void callServer(String collection, String operation, JsonObject data, Object CBModel){
        String url = serverUrl + operation;
        String dataStr = data.toString();
        List<NameValuePair> params = new ArrayList<NameValuePair>();
        params.add(new BasicNameValuePair("collection", collection));
        if(data.has("_id")) {
            params.add(new BasicNameValuePair("_id", data.get("_id").getAsString()));
        }
        else {
            params.add(new BasicNameValuePair("data", dataStr));
        }
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
