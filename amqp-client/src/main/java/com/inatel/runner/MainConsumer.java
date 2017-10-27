package com.inatel.runner;

import com.inatel.Consumer;

public class MainConsumer {

	public static void main(String[] args) {
		try {
			new Consumer().consume();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}