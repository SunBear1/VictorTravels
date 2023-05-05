package com.cringe.travels.trips.rabbitmq;

import java.nio.charset.StandardCharsets;

import org.json.JSONObject;
import org.springframework.stereotype.Component;

@Component
public class Receiver {
    public void receiveMessage(byte[] message) {
        String s = new String(message, StandardCharsets.UTF_8);
        JSONObject jsonObject = new JSONObject(s);
        System.out.println(jsonObject.getString("title"));
      }
}
