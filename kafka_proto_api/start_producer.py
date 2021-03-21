from kafka_proto_api.producer.proto_producer import ProtoKafkaProducer
from kafka_proto_api.config.configuration import getConfigForEnv
import arrow
from kafka_proto_api.protos import etf_pb2
from kafka_proto_api.protos import etf_complex_pb2
import csv
from decimal import Decimal


def load_data_file(filename):
    rows = []
    fields = []
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)
    print("Total no. of rows: %d" % (csvreader.line_num))
    return rows


def main():
    print("Initializing the kafka producer")
    producer = ProtoKafkaProducer(config_env=getConfigForEnv("local"))
    producer_complex = ProtoKafkaProducer(config_env=getConfigForEnv("local_complex"))

    data_set=load_data_file(filename="resources/etf.csv")

    for data_element in data_set:
        etf = etf_pb2.etf(date=data_element[0],
                          open=Decimal(data_element[1]),
                          high=Decimal(data_element[2]),
                          low=Decimal(data_element[3]),
                          close=Decimal(data_element[4]),
                          volume=int(data_element[5]),
                          openint=int(data_element[6]))

        etf_complex_data = etf_complex_pb2.etf_date(date=data_element[0])

        etf_complex = etf_complex_pb2.etf_complex(date=etf_complex_data,
                          open=Decimal(data_element[1]),
                          high=Decimal(data_element[2]),
                          low=Decimal(data_element[3]),
                          close=Decimal(data_element[4]),
                          volume=int(data_element[5]),
                          openint=int(data_element[6]))

        utc = str(arrow.now().timestamp)
        producer.produce(kafka_msg=etf, kafka_key=utc)
        producer_complex.produce(kafka_msg=etf_complex, kafka_key=utc)


if __name__=="__main__":
    main()