from kafka_proto_api.producer.proto_producer import ProtoKafkaProducer
from kafka_proto_api.config.configuration import getConfigForEnv
from kafka_proto_api.consumer.proto_consumer import ProtoKafkaConsumer
from kafka_proto_api.whylogs_analyzer.whylogs_analyzer import WhylogsAnalyzer
from kafka_proto_api.pandas_custom_profiling.pd_profiling import CustomPandasProfiler

import arrow
from kafka_proto_api.protos import etf_pb2
from kafka_proto_api.protos import etf_complex_pb2
from kafka_proto_api.protos import etf_http_ref_pb2
import csv
from decimal import Decimal
import optparse


def option_parser():
    parser = optparse.OptionParser()
    parser.add_option(
        "-t",
        "--type",
        dest="run_type",
        help="Options are producer_run,whylogs_run, pandasprofile_run",
        default="pandasprofile_run",
    )

    return parser.parse_args()


def load_data_file(filename):
    rows = []
    fields = []
    with open(filename, "r") as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)
    print("Total no. of rows: %d" % (csvreader.line_num))
    return rows


def main():
    opts, _ = option_parser()

    if opts.run_type == "producer_run":
        print("Initializing the kafka producer")
        producer = ProtoKafkaProducer(config_env=getConfigForEnv("local"))
        producer_complex = ProtoKafkaProducer(
            config_env=getConfigForEnv("local_complex")
        )
        producer_http_ref = ProtoKafkaProducer(
            config_env=getConfigForEnv("local_http_ref")
        )

        data_set = load_data_file(filename="resources/etf.csv")

        for data_element in data_set:
            etf = etf_pb2.etf(
                date=data_element[0],
                open=Decimal(data_element[1]),
                high=Decimal(data_element[2]),
                low=Decimal(data_element[3]),
                close=Decimal(data_element[4]),
                volume=int(data_element[5]),
                openint=int(data_element[6]),
            )

            etf_complex_data = etf_complex_pb2.etf_date(date=data_element[0])

            etf_complex = etf_complex_pb2.etf_complex(
                date=etf_complex_data,
                open=Decimal(data_element[1]),
                high=Decimal(data_element[2]),
                low=Decimal(data_element[3]),
                close=Decimal(data_element[4]),
                volume=int(data_element[5]),
                openint=int(data_element[6]),
            )

            etf_http = etf_http_ref_pb2.etf_http_ref(
                date=data_element[0],
                open=Decimal(data_element[1]),
                high=Decimal(data_element[2]),
                low=Decimal(data_element[3]),
                close=Decimal(data_element[4]),
                volume=int(data_element[5]),
                openint=int(data_element[6]),
            )

            utc = str(arrow.now().timestamp)
            producer.produce(kafka_msg=etf, kafka_key=utc)
            producer_complex.produce(kafka_msg=etf_complex, kafka_key=utc)
            producer_http_ref.produce(kafka_msg=etf_http, kafka_key=utc)
    elif opts.run_type == "whylogs_run":
        print("Initializing the kafka Analyzer")

        consumer = ProtoKafkaConsumer(config_env=getConfigForEnv("local"))
        consumer_complex = ProtoKafkaConsumer(
            config_env=getConfigForEnv("local_complex")
        )
        consumer_http_ref = ProtoKafkaConsumer(
            config_env=getConfigForEnv("local_http_ref")
        )
        analyzer = WhylogsAnalyzer()
        analyzer.analyze_dataset(consumer)
    elif opts.run_type == "pandasprofile_run":
        print("Initialising the Kafka Pandas profiler.")
        consumer = ProtoKafkaConsumer(config_env=getConfigForEnv("local"))
        consumer_complex = ProtoKafkaConsumer(
            config_env=getConfigForEnv("local_complex")
        )
        consumer_http_ref = ProtoKafkaConsumer(
            config_env=getConfigForEnv("local_http_ref")
        )
        analyzer = CustomPandasProfiler()
        analyzer.analyze_dataset(consumer)
    else:
        print("Unimplemented run type chosen.")


if __name__ == "__main__":
    main()
