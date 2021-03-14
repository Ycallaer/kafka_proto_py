config = {
    'local': {
        'bootstrap_servers': 'localhost:9092',
        'kafkaMaxRequestSize': 50331648,
        'kafkaMaxMessageBytes': 50331648,
        'kafka_produce_topic': 'etf_dummy_data',
        'fetch.wait.max.ms': 60000,
        'session.timeout.ms': 180000,
        'heartbeat.interval.ms': 60000,
        'queue.buffering.max.ms': 0,
        'queue.buffering.max.messages': 15000,
        'auto.register.schemas': True,
        'schemaregistry.url': 'http://localhost:8081'
    }
}

def getConfigForEnv(environment):
    return config[environment]