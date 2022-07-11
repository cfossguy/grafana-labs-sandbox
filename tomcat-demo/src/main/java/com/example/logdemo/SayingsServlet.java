package com.example.logdemo;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.annotation.WebServlet;
import java.util.Random;

@WebServlet(name = "sayingsServlet", value = "/sayings-servlet")
public class SayingsServlet extends HttpServlet {

    final static Logger logger = LogManager.getLogger(SayingsServlet.class);
    private HashMap<Integer,String> phrases;
    private long lastErrorTime = 0;

    public void init() {
        phrases = new HashMap<>();
        phrases.put(0,"Grass is greener on the other side");
        phrases.put(1, "Take it with a grain of salt");
        phrases.put(2, "A chip on your shoulder");
        phrases.put(3, "A dime a dozen");
        phrases.put(4, "A piece of cake");
        phrases.put(5, "If you're not first you are last");
        phrases.put(6, "An arm and a leg");
        phrases.put(7, "Back to square one");
        phrases.put(8, "Beating around the bush");
        phrases.put(9, "Between a rock and hard place");
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        String message;
        String id;

        PrintWriter out = response.getWriter();
        try
        {
            for (int i = 0; i < 100; i++){
                id = String.format("%d-%d",System.currentTimeMillis(),i);
                message = getPhrase(false);
                logger.warn(String.format("Log ID: %s - %s", id, message));
                out.println(String.format("ID: %s - Message: %s", id, message));

                for (int j = 0; j < 10; j++){
                    id = String.format("%d-%d",System.currentTimeMillis(),i);
                    message = getPhrase(false);
                    logger.info(String.format("Log ID: %s - %s", id, message));
                    out.println(String.format("ID: %s - Message: %s", id, message));
                }
            }
            message = getPhrase(true);
            id = String.format("%d-%d",System.currentTimeMillis(),0);
            if (timeForError()) {
                logger.error(String.format("Log ID: %s - %s", id, message));
                out.println(String.format("ID: %s - Message: %s", id, message));
            }

            Random rand = new Random();
            int n = rand.nextInt(5000);
            Thread.sleep(100 + n);
        }

        catch(InterruptedException exc){
             logger.error(exc.getMessage());
        }
    }

    public void destroy() {
    }

    private String getPhrase(boolean isError){

        int random_int = (int)Math.floor(Math.random()*(phrases.size()));
        int put_index = phrases.size();
        if (isError)
        {
            if (put_index % 2 == 0)
                phrases.put(put_index , "If you're not first you are last");
            else if (put_index % 3 == 0)
                phrases.put(put_index , "Take it with a grain of salt");
            else if (put_index % 5 == 0)
                phrases.put(put_index , "A piece of cake");
        }

        return phrases.get(random_int);
    }

    private boolean timeForError(){

        if (lastErrorTime == 0){
            lastErrorTime = System.currentTimeMillis();
            return true;
        }

        if (lastErrorTime < System.currentTimeMillis() - 240000){
            lastErrorTime = System.currentTimeMillis();
            return true;
        }

        return false;
    }
}