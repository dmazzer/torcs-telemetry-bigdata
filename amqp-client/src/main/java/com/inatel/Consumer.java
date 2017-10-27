package com.inatel;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.ShutdownSignalException;

public class Consumer {

	private final static String QUEUE_NAME = "Car3";

	public void consume() throws IOException, TimeoutException, ShutdownSignalException, ConsumerCancelledException, InterruptedException {
		ConnectionFactory factory = new ConnectionFactory();
		
		factory.setUsername("guest");
		factory.setPassword("guest");
		factory.setHost("127.0.0.1");
		
		Connection connection = factory.newConnection();
		
		Channel channel = connection.createChannel();

		channel.queueDeclarePassive(QUEUE_NAME);
		
		QueueingConsumer consumer = new QueueingConsumer(channel);
		
		channel.basicConsume(QUEUE_NAME, false, consumer);
		
		while (true) {
			QueueingConsumer.Delivery delivery = consumer.nextDelivery();
			
			String message = new String(delivery.getBody());
			
			System.out.println("Cosumer Data:" + message);
			
			channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
		}
	}

}
