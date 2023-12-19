from ncclient import manager
import xml.dom.minidom
import requests

def pretty_print(xml_string):
    print(xml.dom.minidom.parseString(xml_string).toprettyxml())

def send_webex_message(token, room_id, message):
    api_url = "https://api.ciscospark.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "roomId": room_id,
        "text": message
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)

# NETCONF Connection
m = manager.connect(
    host="192.168.25.130",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

print("# Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability)

# Get and print the current configuration
netconf_reply = m.get_config(source="running")
pretty_print(netconf_reply.xml)

# Specify a filter for a specific YANG model
netconf_filter = """
<filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter>
"""
netconf_reply = m.get_config(source="running", filter=netconf_filter)
pretty_print(netconf_reply.xml)

# Modify the hostname using NETCONF edit-config operation
netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <hostname>TIP5206</hostname>
  </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_hostname)
pretty_print(netconf_reply.xml)

# Add a new loopback interface
netconf_loopback1 = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>1</name>
    <description>My NETCONF loopback</description>
    <ip>
     <address>
      <primary>
       <address>10.3.1.2</address>
       <mask>255.255.255.0</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_loopback1)
pretty_print(netconf_reply.xml)


# Change the IP address of GigabitEthernet1
netconf_gig1_ip = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <ip>
          <address>
            <primary>
              <address>192.168.25.131</address> <!-- Change the IP address here -->
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </GigabitEthernet>
    </interface>
  </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_gig1_ip)
pretty_print(netconf_reply.xml)

# Webex Teams Message
access_token = "NWRkMmJkZDEtYTIxYy00ODAxLWE3N2YtY2VkMTk4NmQ5ZTgyYjEwZmVjYjktZDAy_P0A1_346e751c-7bdb-491d-9858-1355bbf861ac"
webex_room_id = "7be0e3a0-9dc8-11ee-8f9a-dd8e638e82f8"
message_text = "Changes Has Been Made!"

send_webex_message(access_token, webex_room_id, message_text)
