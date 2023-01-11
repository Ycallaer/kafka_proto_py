from kafka_proto_api.consumer.proto_consumer import ProtoKafkaConsumer
from google.protobuf.json_format import MessageToDict
import pandas as pd
from confluent_kafka.serialization import SerializationContext, MessageField
from pandas_profiling import ProfileReport
import logging


class CustomPandasProfiler:
    def __init__(self, minimal_profiling):
        self.logger = logging.getLogger(__name__)
        self.is_min_profiling_enabled = minimal_profiling

    def analyze_dataset(self, kafka_consumer: ProtoKafkaConsumer) -> None:
        consumer = kafka_consumer.get_consumer()
        total = 0
        df = pd.DataFrame()
        while True:
            try:
                # msg = consumer.poll(1.0)
                messages = consumer.consume(num_messages=100, timeout=2)
                if messages is None:
                    continue
                proto_deserializer = kafka_consumer.get_proto_deserializer()
                etf_list = []
                for msg in messages:
                    etf = proto_deserializer(
                        msg.value(),
                        SerializationContext(
                            kafka_consumer.get_consumer_topic(), MessageField.VALUE
                        ),
                    )
                    dict_obj = MessageToDict(etf)
                    etf_list.append(dict_obj)

                df = df.append(etf_list, ignore_index=True)
                total += 100

                if total > 1500:
                    # ugly hack for demo purpose
                    print(df)
                    break
            except KeyboardInterrupt:
                break

        consumer.close()
        if self.is_min_profiling_enabled:
            profile = ProfileReport(df, title="Pandas Profiling Report",config_file="kafka_proto_api/config/config_profiling_minimal.yml")
        else:
            profile = ProfileReport(df, title="Pandas Profiling Report",
                                    config_file="kafka_proto_api/config/config_profiling_minimal.yml")
        profile.to_file("dataset_analysis.html")
        json_data = profile.to_json()
        with open("dataset_analysis.json", "w") as outfile:
           outfile.write(json_data)
