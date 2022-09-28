import queue
import logging
import paho.mqtt.client as mqtt
from google.protobuf.any_pb2 import Any
import models.mqtt.mcptt_configuration_pb2 as change_profile_mqtt_model
import models.mqtt.floor_control_mqtt_datamodel_pb2 as floor_control_mqtt_model

__author__ = 'Dmitriy Minor'

logger = logging.getLogger()


class MQTTClient(object):
    import logging

    def __init__(self):
        """
        Отправка и прием сообщений Floor Control, изменений профиля пользователя или группы по MQTT
        :param self.client - клиент, подключенный к брокеру
        :param self.sender - экземпляр класса, занимающийся отправкой сообщений
        :param self.receiver - экземпляр класса, занимающийся приемом сообщений
        """

        self.client = None
        self.sender = None
        self.receiver = None
        self.response_queue = queue.Queue()
        self.logging.basicConfig(filename="logs/clients/MQTTClient.log", level=self.logging.INFO)

    def connect_to_broker(self, ip_addr: str = "127.0.0.1", port: int = 1883):
        """
        Подключение к брокеру (rabbitmq) по заданному ip:port
        :param ip_addr: ip адрес
        :param port: порт
        """

        self.sender = MQTTSender()
        self.receiver = MQTTReceiver()
        self.client = mqtt.Client(clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.recv_message
        self.client.connect(ip_addr, port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.sender.on_connect(rc)

    def recv_message(self, client, userdata, message):
        self.response_queue.put(message)

    def recv_create_user(self):
        """ Прием нотификации о создании пользователя """
        return self.receiver.recv_create_user(self.response_queue.get(timeout=3))

    def recv_update_user(self):
        """ Прием нотификации о обновлении пользователя """
        return self.receiver.recv_update_user(self.response_queue.get(timeout=3))

    def recv_delete_user(self):
        """ Прием нотификации о удалении пользователя """
        return self.receiver.recv_delete_user(self.response_queue.get(timeout=3))

    def recv_create_group(self):
        """ Прием нотификации о создании группы """
        return self.receiver.recv_create_group(self.response_queue.get(timeout=3))

    def recv_update_group(self):
        """ Прием нотификации о обновлении группы """
        return self.receiver.recv_update_group(self.response_queue.get(timeout=3))

    def recv_delete_group(self):
        """ Прием нотификации о создании группы """
        return self.receiver.recv_delete_group(self.response_queue.get(timeout=3))

    def recv_floor_request(self):
        """ Прием Floor Request """
        return self.receiver.recv_floor_request(self.response_queue.get(timeout=3))

    def recv_floor_release(self):
        """ Прием Floor Release """
        return self.receiver.recv_floor_release(self.response_queue.get(timeout=3))

    def recv_floor_granted(self):
        """ Прием Floor Granted """
        return self.receiver.recv_floor_granted(self.response_queue.get(timeout=3))

    def recv_floor_revoked(self):
        """ Прием Floor Revoked """
        return self.receiver.recv_floor_revoked(self.response_queue.get(timeout=3))

    def recv_floor_taken(self):
        """ Прием Floor Taken """
        return self.receiver.recv_floor_taken(self.response_queue.get(timeout=3))

    def recv_floor_idle(self):
        """ Прием Floor Idle """
        return self.receiver.recv_floor_idle(self.response_queue.get(timeout=3))

    def recv_floor_ack(self):
        """ Прием Floor Ack """
        return self.receiver.recv_floor_ack(self.response_queue.get(timeout=3))

    def recv_floor_deny(self):
        """ Прием Floor Deny """
        return self.receiver.recv_floor_deny(self.response_queue.get(timeout=3))

    def stop_connection(self):
        """ Закрывает соединение с MQTT брокером"""
        self.client.loop_stop()
        
    def subscribe_to_user_profile_mcptt(self, sip_uri):
        """
        Подписка на пользователя
        :param sip_uri: sip uri пользователя
        """
        topic = f"/mcptt/user/{sip_uri.replace('.', '%2E')}/cfg"
        self.sender.subscribe_to_topic(self.client, topic)

    def subscribe_to_group_profile_mcptt(self, sip_uri):
        """
        Подписка на группу
        :param sip_uri: sip uri группы
        """
        topic = f"/mcptt/group/{sip_uri.replace('.', '%2E')}/cfg"
        self.sender.subscribe_to_topic(self.client, topic)

    def subscribe_to_floor_control(self, sip_uri):
        """
        Подписка на группу
        :param sip_uri: sip uri группы
        """
        topic = f"/mcptt/user/{sip_uri.replace('.', '%2E')}/fctrl/tx"
        self.sender.subscribe_to_topic(self.client, topic)

    def status_call_group(self, sip_uri):
        """
        Подписка на статус групп
        :param sip_uri: sip uri пользователя
        """
        topic = f"/mcptt/group/sip:{sip_uri}/call/status"
        self.client.subscribe(topic)

    def subscribe_to_group(self, sip_uri):
        """
        Подписка на группу
        :param sip_uri: sip uri пользователя
        """
        topic = f"/mcptt/group/sip:{sip_uri}/call/fctrl/ntfy"
        self.client.subscribe(topic)

    def log_writer(self, topic, body, sip_uri, fl):
        logger.info("#################### SEND Floor Control MQTT ####################")
        logger.info(f"Send Publish Floor {fl} (MQTT)")
        logger.info(f"Topic {topic}")
        logger.info(f"Body {body}")
        logger.info(f"Reply to /uc/al/session/{sip_uri.replace('%2E', '.')}")
        logger.info(f"Request id 1")
        logger.info("#################################################################")

    def send_floor_request(self, sip_uri, source_id, priority):
        """
        Отправка Floor Request
        :param sip_uri: sip uri пользователя
        :param source_id: идентификатор плеча вызова
        """
        topic = f"/mcptt/user/sip:{sip_uri}/fctrl/tx"
        floor_request_model = floor_control_mqtt_model.FloorRequest(uri=sip_uri, priority=priority, source_id=source_id)
        body = Any()
        body.Pack(floor_request_model)
        message = floor_control_mqtt_model.McpttMessage(body=body).SerializeToString()
        self.sender.send_floor_request(self.client, topic, message)
        self.log_writer(topic, body, sip_uri, "Request")

    def send_floor_release(self, sip_uri, source_id):
        """
        Отправка Floor Release
        :param sip_uri: sip uri пользователя
        :param source_id: идентификатор плеча вызова
        """
        topic = f"/mcptt/user/sip:{sip_uri}/fctrl/tx"
        floor_release_model = floor_control_mqtt_model.FloorRelease(uri=sip_uri, source_id=source_id)
        body = Any()
        body.Pack(floor_release_model)
        message = floor_control_mqtt_model.McpttMessage(body=body).SerializeToString()
        self.sender.send_floor_release(self.client, topic, message)
        self.log_writer(topic, body, sip_uri, "Release")

    def send_floor_granted(self, sip_uri, source_id):
        """
        Отправка Floor Granted
        :param sip_uri: sip uri пользователя
        :param source_id: идентификатор плеча вызова
        """
        topic = f"/mcptt/user/sip:{sip_uri}/fctrl/tx"
        floor_granted_model = floor_control_mqtt_model.FloorGranted(duration=30, source_id=source_id, need_ack=True)
        body = Any()
        body.Pack(floor_granted_model)
        message = floor_control_mqtt_model.McpttMessage(body=body, reply_to=f"/uc/al/session/{sip_uri.replace('%2E', '.')}",
                                          request_id=1).SerializeToString()
        self.sender.send_floor_granted(self.client, topic, message)
        self.log_writer(topic, body, sip_uri, "Granted")

    def send_floor_revoked(self, sip_uri, source_id):
        """
        Отправка Floor Revoked
        :param sip_uri: sip uri пользователя
        :param source_id: идентификатор плеча вызова
        """
        topic = f"/mcptt/user/sip:{sip_uri}/fctrl/tx"
        floor_revoked_model = floor_control_mqtt_model.FloorRevoked(source_id=source_id, need_ack=True)
        body = Any()
        body.Pack(floor_revoked_model)
        message = floor_control_mqtt_model.McpttMessage(body=body, reply_to=f"/uc/al/session/{sip_uri.replace('%2E', '.')}",
                                          request_id=1).SerializeToString()
        self.sender.send_floor_revoked(self.client, topic, message)
        self.log_writer(topic, body, sip_uri, "Revoked")

    def send_floor_taken(self, sip_uri, source_id):
        """
        Отправка Floor Taken
        :param sip_uri: sip uri пользователя
        :param source_id: идентификатор плеча вызова
        """
        topic = f"/mcptt/user/sip:{sip_uri}/fctrl/tx"
        floor_taken_model = floor_control_mqtt_model.FloorTaken(uri=sip_uri, source_id=source_id, need_ack=True)
        body = Any()
        body.Pack(floor_taken_model)
        message = floor_control_mqtt_model.McpttMessage(body=body, reply_to=f"/uc/al/session/{sip_uri.replace('%2E', '.')}",
                                          request_id=1).SerializeToString()
        self.sender.send_floor_taken(self.client, topic, message)
        self.log_writer(topic, body, sip_uri, "Taken")

    def send_floor_idle(self, sip_uri, source_id):
        """
        Отправка Floor Idle
        :param sip_uri: sip uri пользователя
        :param source_id: идентификатор плеча вызова
        """
        topic = f"/mcptt/user/sip:{sip_uri}/fctrl/tx"
        floor_idle_model = floor_control_mqtt_model.FloorIdle(source_id=source_id, need_ack=True)
        body = Any()
        body.Pack(floor_idle_model)
        message = floor_control_mqtt_model.McpttMessage(body=body, reply_to=f"/uc/al/session/{sip_uri.replace('%2E', '.')}",
                                          request_id=1).SerializeToString()
        self.sender.send_floor_idle(self.client, topic, message)
        self.log_writer(topic, body, sip_uri, "Idle")

    def send_floor_ack(self, sip_uri):
        """
        Отправка Floor Ack
        :param sip_uri: sip uri пользователя
        """
        topic = f"/mcptt/user/sip:{sip_uri}/fctrl/tx"
        floor_ack_model = floor_control_mqtt_model.FloorAck(uri=sip_uri)
        body = Any()
        body.Pack(floor_ack_model)
        message = floor_control_mqtt_model.McpttMessage(body=body, reply_to=f"/uc/al/session/{sip_uri.replace('%2E', '.')}",
                                          request_id=1).SerializeToString()
        self.sender.send_floor_ack(self.client, topic, message)
        self.log_writer(topic, body, sip_uri, "Ack")

    def send_floor_deny(self, sip_uri):
        """
        Отправка Floor Deny
        :param sip_uri: sip uri пользователя
        """
        topic = f"/mcptt/user/sip:{sip_uri}/fctrl/tx"
        floor_deny_model = floor_control_mqtt_model.FloorDeny(cause="Failed", need_ack=True)
        body = Any()
        body.Pack(floor_deny_model)
        message = floor_control_mqtt_model.McpttMessage(body=body, reply_to=f"/uc/al/session/{sip_uri.replace('%2E', '.')}",
                                          request_id=1).SerializeToString()
        self.sender.send_floor_deny(self.client, topic, message)
        self.log_writer(topic, body, sip_uri, "Deny")


class MQTTSender(object):

    def on_connect(self, rc):
        print(f"Connect to broker {rc}")

    def subscribe_to_topic(self, client, topic):
        client.subscribe(topic)
        print(f"Send Subscribe to topic {topic}")

    def send_floor_request(self, client, topic, payload):
        client.publish(topic, payload)

    def send_floor_release(self, client, topic, payload):
        client.publish(topic, payload)
        print("Send Publish Floor Release (MQTT)")

    def send_floor_granted(self, client, topic, payload):
        client.publish(topic, payload)
        print("Send Publish Floor Granted (MQTT)")

    def send_floor_revoked(self, client, topic, payload):
        client.publish(topic, payload)
        print("Send Publish Floor Revoked (MQTT)")

    def send_floor_taken(self, client, topic, payload):
        client.publish(topic, payload)
        print("Send Publish Floor Taken (MQTT)")

    def send_floor_idle(self, client, topic, payload):
        client.publish(topic, payload)
        print("Send Publish Floor Idle (MQTT)")

    def send_floor_ack(self, client, topic, payload):
        client.publish(topic, payload)
        print("Send Publish Floor Ack (MQTT)")

    def send_floor_deny(self, client, topic, payload):
        client.publish(topic, payload)
        print("Send Publish Floor Deny (MQTT)")


class MQTTReceiver(object):

    def log_writer_fc(self, message, mcptt_msg, fl):
        logger.info("#################### RECV Floor Control MQTT ####################")
        logger.info(f"Package is Floor {fl} (MQTT)")
        logger.info(f"Topic {message.topic}")
        logger.info(f"Body {mcptt_msg.body}")
        logger.info("#################################################################")

    def log_writer_doc(self, message, mcptt_msg, fl):
        logger.info("#################### RECV Action Document MCPTT ####################")
        logger.info(f"Package is {fl} (MQTT)")
        logger.info(f"Topic {message.topic}")
        logger.info(f"Body {mcptt_msg}")
        logger.info("#################################################################")

    def recv_create_user(self, message):
        create_user_msg = change_profile_mqtt_model.ProfileChanged()
        create_user_msg.ParseFromString(message.payload)
        self.log_writer_doc(message, create_user_msg, "Create user")
        return create_user_msg

    def recv_update_user(self, message):
        update_user_msg = change_profile_mqtt_model.ProfileChanged()
        update_user_msg.ParseFromString(message.payload)
        self.log_writer_doc(message, update_user_msg, "Update user")
        return update_user_msg

    def recv_delete_user(self, message):
        delete_user_msg = change_profile_mqtt_model.ProfileChanged()
        delete_user_msg.ParseFromString(message.payload)
        self.log_writer_doc(message, delete_user_msg, "Delete user")
        return delete_user_msg

    def recv_create_group(self, message):
        create_group_msg = change_profile_mqtt_model.ProfileChanged()
        create_group_msg.ParseFromString(message.payload)
        self.log_writer_doc(message, create_group_msg, "Create group")
        return create_group_msg

    def recv_update_group(self, message):
        update_group_msg = change_profile_mqtt_model.ProfileChanged()
        update_group_msg.ParseFromString(message.payload)
        self.log_writer_doc(message, update_group_msg, "Update group")
        return update_group_msg

    def recv_delete_group(self, message):
        delete_group_msg = change_profile_mqtt_model.ProfileChanged()
        delete_group_msg.ParseFromString(message.payload)
        self.log_writer_doc(message, delete_group_msg, "Delete group")
        return delete_group_msg

    def recv_floor_request(self, message):
        mcptt_msg = floor_control_mqtt_model.McpttMessage()
        mcptt_msg.ParseFromString(message.payload)
        floor_request = floor_control_mqtt_model.FloorRequest()
        floor_request.ParseFromString(mcptt_msg.body.value)
        if mcptt_msg.body.type_url == "type.googleapis.com/protei.uc.mcptt.api.FloorRequest":
            self.log_writer_fc(message, mcptt_msg, "Request")
            return floor_request
        else:
            raise AssertionError(f"Package is not Floor Request (MQTT). Recv packet {mcptt_msg.body.type_url}")

    def recv_floor_release(self, message):
        mcptt_msg = floor_control_mqtt_model.McpttMessage()
        mcptt_msg.ParseFromString(message.payload)
        floor_release = floor_control_mqtt_model.FloorRelease()
        floor_release.ParseFromString(mcptt_msg.body.value)
        if mcptt_msg.body.type_url == "type.googleapis.com/protei.uc.mcptt.api.FloorRelease":
            self.log_writer_fc(message, mcptt_msg, "Release")
            return floor_release
        else:
            raise AssertionError(f"Package is not Floor Release (MQTT). Recv packet {mcptt_msg.body.type_url}")

    def recv_floor_granted(self, message):
        mcptt_msg = floor_control_mqtt_model.McpttMessage()
        mcptt_msg.ParseFromString(message.payload)
        floor_granted = floor_control_mqtt_model.FloorGranted()
        floor_granted.ParseFromString(mcptt_msg.body.value)
        if mcptt_msg.body.type_url == "type.googleapis.com/protei.uc.mcptt.api.FloorGranted":
            self.log_writer_fc(message, mcptt_msg, "Granted")
        else:
            raise AssertionError(f"Package is not Floor Granted (MQTT). Recv packet {mcptt_msg.body.type_url}")

    def recv_floor_revoked(self, message):
        mcptt_msg = floor_control_mqtt_model.McpttMessage()
        mcptt_msg.ParseFromString(message.payload)
        floor_revoked = floor_control_mqtt_model.FloorRevoked()
        floor_revoked.ParseFromString(mcptt_msg.body.value)
        if mcptt_msg.body.type_url == "type.googleapis.com/protei.uc.mcptt.api.FloorRevoked":
            self.log_writer_fc(message, mcptt_msg, "Revoked")
        else:
            raise AssertionError(f"Package is not Floor Revoked (MQTT). Recv packet {mcptt_msg.body.type_url}")

    def recv_floor_taken(self, message):
        mcptt_msg = floor_control_mqtt_model.McpttMessage()
        mcptt_msg.ParseFromString(message.payload)
        floor_taken = floor_control_mqtt_model.FloorTaken()
        floor_taken.ParseFromString(mcptt_msg.body.value)
        if mcptt_msg.body.type_url == "type.googleapis.com/protei.uc.mcptt.api.FloorTaken":
            self.log_writer_fc(message, mcptt_msg, "Taken"),
        else:
            raise AssertionError(f"Package is not Floor Taken (MQTT). Recv packet {mcptt_msg.body.type_url}")

    def recv_floor_idle(self, message):
        mcptt_msg = floor_control_mqtt_model.McpttMessage()
        mcptt_msg.ParseFromString(message.payload)
        floor_idle = floor_control_mqtt_model.FloorIdle()
        floor_idle.ParseFromString(mcptt_msg.body.value)
        if mcptt_msg.body.type_url == "type.googleapis.com/protei.uc.mcptt.api.FloorIdle":
            self.log_writer_fc(message, mcptt_msg, "Idle")
        else:
            raise AssertionError(f"Package is not Floor Idle (MQTT). Recv packet {mcptt_msg.body.type_url}")

    def recv_floor_ack(self, message):
        mcptt_msg = floor_control_mqtt_model.McpttMessage()
        mcptt_msg.ParseFromString(message.payload)
        floor_ack = floor_control_mqtt_model.FloorAck()
        floor_ack.ParseFromString(mcptt_msg.body.value)
        if mcptt_msg.body.type_url == "type.googleapis.com/protei.uc.mcptt.api.FloorAck":
            self.log_writer_fc(message, mcptt_msg, "Ack")
        else:
            raise AssertionError(f"Package is not Floor Ack (MQTT). Recv packet {mcptt_msg.body.type_url}")

    def recv_floor_deny(self, message):
        mcptt_msg = floor_control_mqtt_model.McpttMessage()
        mcptt_msg.ParseFromString(message.payload)
        floor_deny = floor_control_mqtt_model.FloorDeny()
        floor_deny.ParseFromString(mcptt_msg.body.value)
        if mcptt_msg.body.type_url == "type.googleapis.com/protei.uc.mcptt.api.FloorDeny":
            self.log_writer_fc(message, mcptt_msg, "Deny")
        else:
            raise AssertionError(f"Package is not Floor Deny (MQTT). Recv packet {mcptt_msg.body.type_url}")


# if __name__ == '__main__':
#     import sys
#     from robotremoteserver import RobotRemoteServer
#
#     RobotRemoteServer(FCMQTTMachine(), host=sys.argv[1], port=sys.argv[2])
