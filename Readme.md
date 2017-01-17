# Rabbit File Transfer Protocol
RFTP uses rabbitmq to transfer files. Can be used to push files through a [rabbitmq based data diode](https://github.com/marcelmaatkamp/rabbitmq-applications/tree/master/application/datadiode)

Let's say your rabbitmq data diode has an inside address of 192.168.1.15, and an outside address of 5.5.5.23, and you want to transfer my-app.deb into your closed environment.

*First* you start the receiver on the 'inside' with a filename you want to write to

	inside-host$ ./rftp rftp://user:pass@192.168.1.15/ my-app.deb
	Waiting for data on queue 6QFZVF. You can now start the sender!

*Then* you start the sender on the 'outside', providing the queue id shown by the receiver

	outside-host$ rftp  my-app.deb rftp://user:pass@5.5.5.23/6QFZVF
	[============================================================] 100.0%
	Done!
	outside-host$

