from kafka_proto_api.producer.proto_producer import ProtoKafkaProducer
from kafka_proto_api.config.configuration import getConfigForEnv
import arrow
from kafka_proto_api.protos import etf_pb2
import csv
from decimal import Decimal

# csv file name
filename = "resources/etf.csv"

# initializing the titles and rows list
fields = []
rows = []



def main():
    print("Initializing the kafka producer")
    producer = ProtoKafkaProducer(config_env=getConfigForEnv("local"))
    filepath = "../resources/etf.csv"

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
            etf = etf_pb2.etf(date=row[0], open=Decimal(row[1]), high=Decimal(row[2]), low=Decimal(row[3]), close=Decimal(row[4]), volume=int(row[5]), openint=int(row[6]))
            utc = str(arrow.now().timestamp)
            producer.produce(kafka_msg=etf, kafka_key=utc)
            #time.sleep(1)

        print("Total no. of rows: %d" % (csvreader.line_num))


if __name__=="__main__":
    main()