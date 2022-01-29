package com.example.logdemo;

import java.io.*;
import java.util.HashMap;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import javax.servlet.http.*;
import javax.servlet.annotation.*;

@WebServlet(name = "sayingsServlet", value = "/sayings-servlet")
public class SayingsServlet extends HttpServlet {

    final static Logger logger = LogManager.getLogger(SayingsServlet.class);
    private HashMap<Integer,String> phrases;

    public void init() {
        phrases = new HashMap<>();
        phrases.put(0,"The grass is always greener on the other side");
        phrases.put(1, "Take it with a grain of salt");
        phrases.put(2, "A chip on your shoulder");
        phrases.put(3, "A dime a dozen");
        phrases.put(4, "A piece of cake");
        phrases.put(5, "If you're not first you are last");
        phrases.put(6, "An arm and a leg");
        phrases.put(7, "Back to square one");
        phrases.put(8, "Beating around the bush");
        phrases.put(9, "Between a rock and hard place");
        phrases.put(10, "Burst your bubble");
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        String message;

        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        for (int i=0; i<10000; i++)
        {
            String id = String.format("%d-%d",System.currentTimeMillis(),i);
            message = getPhrase();

            if (i % 100 == 0) {
                logger.error(String.format("Log ID: %s - %s", id, message));
                out.println(String.format("<p>ID: %s - Message: %s</p>", id, message));
            }
            else if (i % 10 == 0) {
                logger.warn(String.format("Log ID: %s - %s", id, message));
                out.println(String.format("<p>ID: %s - Message: %s</p>", id, message));
            }
            else{
                logger.info(String.format("Log ID: %s - %s", id, message));
                out.println(String.format("<p>ID: %s - Message: %s</p>", id, message));
            }
        }
        out.println("</body></html>");
    }

    public void destroy() {
    }

    private String getPhrase(){
        int max = phrases.size();
        int min = 0;
        int random_int = (int)Math.floor(Math.random()*(max-min)+min);
        return phrases.get(random_int);
    }
}