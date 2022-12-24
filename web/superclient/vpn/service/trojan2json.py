import json

# trojan://segment01@segment02:10000?sni=segment03#segment_name

template = """
{
  "stats": {},
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "tag": "socks",
      "port": 1080,
      "listen": "::",
      "protocol": "socks",
      "settings": {
        "auth": "noauth",
        "udp": true,
        "userLevel": 8
      }
    }
  ],
  "outbounds": [
    {
      "tag": "proxy",
      "protocol": "trojan",
      "settings": {
        "servers": [
          {
            "address": "segment02",
            "method": "auto",
            "ota": false,
            "password": "segment01",
            "port": 10000,
            "level": 8
          }
        ]
      },
      "streamSettings": {
        "network": "tcp",
        "security": "tls",
        "tlsSettings": {
          "allowInsecure": true,
          "serverName": "segment03",
          "fingerprint": "randomized"
        }
      },
      "mux": {
        "enabled": false
      }
    },
    {
      "tag": "direct",
      "protocol": "freedom",
      "settings": {
        "domainStrategy": "UseIP"
      }
    }
  ],
  "dns": {
    "servers": [
      "8.8.8.8"
    ]
  },
  "routing": {
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      {
        "type": "field",
        "ip": [
          "geoip:private",
          "geoip:cn"
        ],
        "outboundTag": "direct"
      },
      {
        "type": "field",
        "domain": [
          "geosite:cn"
        ],
        "outboundTag": "direct"
      }
    ]
  }
}
"""

def generate(model):

  # load json
  _json = json.loads(template)

  # get childs
  _outbounds = _json["outbounds"][0]
  _servers = _outbounds["settings"]["servers"][0]
  _tlsSettings = _outbounds["streamSettings"]["tlsSettings"]
  
  # set values
  _servers["password"] = model.uid
  _servers["address"] = model.host
  _servers["port"] = model.port
  _tlsSettings["serverName"] = model.ws_sni

  return json.dumps(_json)
