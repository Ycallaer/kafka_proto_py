from confluent_kafka.serialization import StringDeserializer
from confluent_kafka import DeserializingConsumer, Consumer, OFFSET_END, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
import time
import logging

class ProtoKafkaConsumer:
    def __init__(self, config_env):
        self.config = config_env
        logger = logging.getLogger(__name__)
        self.topic_name = self.config["kafka_produce_topic"]

        self.consumer_conf = {
            "bootstrap.servers": self.config["bootstrap_servers"],
            "group.id": "test-group-{}".format(str(time.time() * 1000)),
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "fetch.wait.max.ms": 0,
        }

    def _on_assign(self, consumer, partitions):
        """
        Print the consumer information

        Args:
            consumer
            Partitions
        """
        print("assign {} on partitions {}".format(consumer, partitions))

    def get_consumer(self):
        """
        Retrieves a consumer object that is subscribed to a topic

        return con
        """
        consumer = Consumer(self.consumer_conf)
        try:
            consumer.subscribe([self.topic_name], on_assign=self._on_assign)
        except KafkaException as e:
            print(e)
        return consumer

    def get_proto_deserializer(self):
        return ProtobufDeserializer(self.config['proto_msg_type'])

    def get_consumer_topic(self):
        return self.topic_name
