import paho.mqtt.publish as publish
import time


class Comunic_ThingSpeak:

    def __init__(self, channelID, apiKey):
        ###   Start of user configuration   ##
        #  ThingSpeak Channel Settings

        # The ThingSpeak Channel ID
        self.channelID = channelID

        # The Write API Key for the channel
        self.apiKey = apiKey

        #  MQTT Connection Methods

        # Set useUnsecuredTCP to True to use the default MQTT port of 1883
        # This type of unsecured MQTT connection uses the least amount of system resources.
        useUnsecuredTCP = False

        # Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
        # Try this if port 1883 is blocked on your network.
        useUnsecuredWebsockets = False

        # Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
        # This type of connection will use slightly more system resources, but the connection
        # will be secured by SSL.
        useSSLWebsockets = True

        ###   End of user configuration   ###

        # The Hostname of the ThinSpeak MQTT service
        self.mqttHost = "mqtt.thingspeak.com"

        # Set up the connection parameters based on the connection type
        if useUnsecuredTCP:
            self.tTransport = "tcp"
            self.tPort = 1883
            self.tTLS = None

        if useUnsecuredWebsockets:
            self.tTransport = "websockets"
            self.tPort = 80
            self.tTLS = None

        if useSSLWebsockets:
            import ssl

            self.tTransport = "websockets"
            self.tTLS = {'ca_certs': "/etc/ssl/certs/ca-certificates.crt", 'tls_version': ssl.PROTOCOL_TLSv1}
            self.tPort = 443

    def send_ts(self, ora, medicine, ritardo, preso=1):
        # Create the topic string
        self.topic = "channels/" + self.channelID + "/publish/" + self.apiKey

        # invio a entrambi i canali il ritardo, uno dei due grafici mi farà
        # direttamente la media
        if preso==0:
            status="Non sono state prese le medicine"
        else:

            status = "Medicine ore: " + str(ora) + " = " + str(medicine) + "   " + " Ritardo: " + str(ritardo) + " minuti"

        tPayload = "field1=" + str(ora) + "&status=" + status  + "&field2=" + str(ritardo)
        # attempt to publish this data to the topic
        try:
            publish.single(self.topic, payload=tPayload, hostname=self.mqttHost, port=self.tPort, tls=self.tTLS,
                           transport=self.tTransport)
            time.sleep(20)

        except:
            print("There was an error while publishing the data.")
            time.sleep(0.5)
