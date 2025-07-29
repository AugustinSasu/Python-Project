# log_consumer.py to consume logs from RabbitMQ and write them to a file
import pika
import json
import os
import time


def callback(ch, method, properties, body):
    log_entry = json.loads(body.decode())["log"]
    with open("/var/log/my_app.log", "a") as f:
        f.write(log_entry + "\n")


def main():
    rmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

    credentials = pika.PlainCredentials('guest', 'guest')
    for attempt in range(10):
        try:
            print(f"[*] Connecting Log Consumer to RabbitMQ at {rmq_host}:5672 (attempt {attempt + 1})")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rmq_host, port=5672, credentials=credentials)
            )
            print("[✔] Connected Log Consumer to RabbitMQ.")
            break
        except Exception as e:
            print(f"[!] Log Consumer could not connect to RabbitMQ (try {attempt + 1}/10): {e}")
            time.sleep(2)
    else:
        print("[!] Giving up after 10 tries.")
        return

    channel = connection.channel()

    channel.queue_declare(queue="logs", durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue="logs", on_message_callback=callback, auto_ack=True)

    print("📡 Waiting for logs. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()