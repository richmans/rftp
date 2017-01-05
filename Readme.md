# Rabbit File Transfer Protocol
RFTP uses rabbitmq to transfer files. Can be used to push files through a [rabbitmq based data diode](https://github.com/marcelmaatkamp/rabbitmq-applications/tree/master/application/datadiode)

Let's say your rabbitmq data diode has an inside address of 192.168.1.15, and an outside address of 5.5.5.23, and you want to transfer my-app.deb into your closed environment.

*First* you start the receiver on the 'inside' with a filename you want to write to

    inside-host$ rftp receive rftp://192.168.1.15 my-app.deb
		Receiver ready, listening to queue f34Azms3
		...

*Then* you start the sender on the 'outside', providing the queue id shown by the receiver

    outside-host$ rftp send my-app.deb rftp://5.5.5.23/f34Azms3
		outside-host$

