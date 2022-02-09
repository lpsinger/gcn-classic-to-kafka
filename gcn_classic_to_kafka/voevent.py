"""Process GCN Notices in VOEvent format."""

import logging

import gcn
from confluent_kafka import Producer

from .common import kafka_topic_for_notice_type

log = logging.getLogger(__name__)


def serve_forever(config):
    log.info('Connecting to Kafka')
    producer = Producer(config)

    def handler(payload, root):
        notice_type = gcn.get_notice_type(root)
        kafka_topic = kafka_topic_for_notice_type(notice_type, 'voevent')
        log.info('Sending notice type %d to %s', notice_type, kafka_topic)
        producer.produce(kafka_topic, payload)

    log.info('Connecting to GCN')
    gcn.listen(handler=handler)