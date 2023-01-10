from kafka_proto_api.consumer.proto_consumer import ProtoKafkaConsumer
from confluent_kafka.serialization import SerializationContext, MessageField
import whylogs as why
import pandas as pd
from glob import glob
from functools import reduce
from google.protobuf.json_format import MessageToDict
import dataframe_image as dfi
class WhylogsAnalyzer():
    def __int__(self):
        print("something")

    def analyze_dataset(self,kafka_consumer: ProtoKafkaConsumer ):
        consumer=kafka_consumer.get_consumer()
        total = 0
        df = pd.DataFrame()
        with why.logger(mode="rolling", interval=5, when="M", base_name="whylogs-kafka") as logger:
            logger.append_writer("local", base_dir="profiles")
            while True:
                try:
                    # SIGINT can't be handled when polling, limit timeout to 1 second.
                    msg = consumer.poll(1.0)
                    if msg is None:
                        continue
                    proto_deserializer = kafka_consumer.get_proto_deserializer()
                    etf = proto_deserializer(msg.value(), SerializationContext(kafka_consumer.get_consumer_topic(), MessageField.VALUE))
                    dict_obj = MessageToDict(etf)
                    #print(etf)

                    #for k, v in dict_obj.items():
                        #print(f'{k} - {len(v)}')
                    df = df.append(dict_obj,ignore_index=True)
                    logger.log(df)
                    total += 1

                    if total > 1500:
                        print(df)
                        break
                except KeyboardInterrupt:
                    break

        consumer.close()
        print(df)
        print("analyze")
        profiles_binaries = glob("profiles/whylogs*")
        profiles_list = []

        for profile in profiles_binaries:
            profiles_list.append(why.read(profile).view())

        merged_profile = reduce((lambda x, y: x.merge(y)), profiles_list)
        merged_profile_df = merged_profile.to_pandas()
        print(merged_profile_df)
        dfi.export(merged_profile_df, "merged_profile_df.png")