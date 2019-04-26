package $NAMESPACE;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonElement;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpEntityEnclosingRequestBase;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPatch;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.concurrent.FutureCallback;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.nio.client.CloseableHttpAsyncClient;
import org.apache.http.impl.nio.client.HttpAsyncClients;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URI;
import java.util.Iterator;
import java.util.stream.Collectors;


public class Adapter {
    private static String serverIP = "$server_ip";
    private static String port = "$port";
    private static String dm_name = "$dm_name";
    private static String serverUrl = "http://" + serverIP + ":" + port + "/" + dm_name + "/"; 
    private static CloseableHttpAsyncClient httpAsyncClient = HttpAsyncClients.createDefault();

    static {
        httpAsyncClient.start();
    }

    $FUNC Adapter 

    // CRUD: create
    // "collection" must be specified by the first parameter.
    // "data" must be specified as an JsonObject or an JsonArray passed in by the second parameter.
    public static void create(String collection, JsonElement data, Object CBModel){
        String body = data.toString();
        String url = serverUrl + collection;
        HttpPost request = new HttpPost(url);
        CallServer(request, body, CBModel);
    }
    
    // CRUD: ReadOne.
    // "collection" must be specified in by the first parameter.
    // "param" must be specified as an object by the second parameter.
    public static void get(String collection, String param, Object CBModel){
        String url = serverUrl + collection + "/" + param;
        HttpGet request = new HttpGet(url);
        CallServer(request, "", CBModel);
    }
    
    // CRUD: readMany.
    // "collection" must be specified in by the first parameter.
    // "data" must be specified as a JsonElement by the second parameter.
    public static void read(String collection, JsonElement data, Object CBModel){
        String url = serverUrl + collection;
        String body = data.toString();
        if (!body.isEmpty()) {
            if (data.isJsonObject()) {
                url += "/?";
                for (String s : ((JsonObject) data).keySet()) {
                    String value = ((JsonObject) data).get(s).toString();
                    if (Character.toString(value.charAt(0)).equals("\"")) {
                        value = value.substring(1, value.length() - 1);
                    }
                    url += s + "=" + value + "&";
                }
                url = url.substring(0, url.length() - 1);
            } else if (data.isJsonArray()) {
                Iterator<JsonElement> iter = ((JsonArray) data).iterator();
                url += "/?";
                while (iter.hasNext()) {
                    JsonElement element = iter.next();
                    for (String s : ((JsonObject) element).keySet()) {
                        url += s + "=" + ((JsonObject) element).get(s) + "&";
                    }
                }
                url = url.substring(0, url.length() - 1);
            }
        }
        HttpGet request = new HttpGet(url);
        CallServer(request, "", CBModel);
    }
    
    // CRUD: replace.
    // "collection" must be specified in by the first parameter.
    // "data" must be specified as an JsonObject by the second parameter.
    // "dataId" must be specified as an String by the third parameter.
    public static void set(String collection, JsonElement data, String dataId, Object CBModel){
        String body = data.toString();
        String url = serverUrl + collection + "/" + dataId;
        HttpPut request = new HttpPut(url);
        CallServer(request, body, CBModel);
    }
    
    // CRUD: modify.
    // "collection" must be specified in by the first parameter.
    // "data" must be specified as an JsonObject by the second parameter.
    // "dataId" must be specified as an String by the third parameter.
    public static void update(String collection, JsonElement data, String dataId, Object CBModel){
        String body = data.toString();
        String url = serverUrl + collection + "/" + dataId;
        HttpPatch request = new HttpPatch(url);
        CallServer(request, body, CBModel);
    }
    
    // CRUD: delete.
    // "collection" must be specified in by the first parameter.
    // "data" must be specified as an JsonObject by the second parameter.
    public static void delete(String collection, JsonObject data, Object CBModel) throws  ClientProtocolException, IOException{
        String body = data.toString();
        String url = serverUrl + collection;
        HttpDeleteWithBody request = new HttpDeleteWithBody(url);
        CallServer(request, body, CBModel);
    }
    
    // OverLoad delete().
    // "collection" must be specified in by the first parameter.
    // "dataId" must be specified as an String by the second parameter.
    public static void delete(String collection, String dataId, Object CBModel) {
        String url = serverUrl + collection + "/" + dataId;
        HttpDelete request = new HttpDelete(url);
        CallServer(request, "", CBModel);
    }
    
    public static void CallServer(HttpRequestBase request, String body, Object CBModel){
        Method successM, errorM;
        try {
            successM = CBModel.getClass().getMethod("successCB", String.class);
            errorM = CBModel.getClass().getMethod("errorCB", String.class);
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
            return;
        }
        
        request.setHeader("Content-Type", "application/json; charset=utf-8");

        if (!body.isEmpty()) {
            try {
                if (request instanceof HttpEntityEnclosingRequestBase) {
                    ((HttpEntityEnclosingRequestBase)request).setEntity(new StringEntity(body));
                }
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
        
        httpAsyncClient.execute(request, new FutureCallback<HttpResponse>() {
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
    
    public static class HttpDeleteWithBody extends HttpEntityEnclosingRequestBase {
        public static final String METHOD_NAME = "DELETE";
     
        public String getMethod() {
            return METHOD_NAME;
        }
     
        public HttpDeleteWithBody(final String uri) {
            super();
            setURI(URI.create(uri));
        }
     
        public HttpDeleteWithBody(final URI uri) {
            super();
            setURI(uri);
        }
     
        public HttpDeleteWithBody() {
            super();
        }
    }

    $ENDFUNC

}
