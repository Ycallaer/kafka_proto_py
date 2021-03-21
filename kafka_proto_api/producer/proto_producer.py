from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer


class ProtoKafkaProducer:
    def __init__(self,config_env):
        self.config = config_env
        self.topic_name = self.config["kafka_produce_topic"]

        conf = {'bootstrap.servers': self.config["bootstrap_servers"],
                'message.max.bytes': self.config["kafkaMaxMessageBytes"],
                'queue.buffering.max.ms': self.config["queue.buffering.max.ms"],
                'queue.buffering.max.messages': self.config["queue.buffering.max.messages"],
                'key.serializer': StringSerializer('utf_8'),
                'value.serializer': self.__protobuf_serializer()
                }

        self.producer = SerializingProducer(conf)

    def on_delivery(self, err, msg):
        if err:
            print("Message failed delivery, error: %s", err)
        else:
            print("Message delivered to %s on partition %s", msg.topic(), msg.partition())

    def __protobuf_serializer(self):
        schema_registry_conf = {'url': self.config['schemaregistry.url']}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        _proto_conf = {
            'auto.register.schemas': self.config['auto.register.schemas'],
        }

        return ProtobufSerializer(self.config['proto_msg_type'], schema_registry_client, conf=_proto_conf)

    def produce(self, kafka_msg, kafka_key):
        try:
            self.producer.produce(topic=self.topic_name,
                                  value=kafka_msg,
                                  key=kafka_key,
                                  on_delivery=self.on_delivery
            )

            self.producer.flush()

        except Exception as e:
            print("Error during producing to kafka topic. Stacktrace is %s",e)