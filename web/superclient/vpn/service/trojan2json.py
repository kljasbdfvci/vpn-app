import json

# trojan://segment01@segment02:segment03?sni=segment04#segment_name

template = """
{
  "stats": {},
  "log": {
    "loglevel": "warning"
  },
  "policy": {
    "levels": {
      "8": {
        "handshake": 4,
        "connIdle": 300,
        "uplinkOnly": 1,
        "downlinkOnly": 1
      }
    },
    "system": {
      "statsOutboundUplink": true,
      "statsOutboundDownlink": true
    }
  },
  "inbounds": [
    {
      "tag": "socks",
      "port": 10808,
      "protocol": "socks",
      "settings": {
        "auth": "noauth",
        "udp": true,
        "userLevel": 8
      },
      "sniffing": {
        "enabled": true,
        "destOverride": [
          "http",
          "tls"
        ]
      }
    },
    {
      "tag": "http",
      "port": 10809,
      "protocol": "http",
      "settings": {
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
            "port": segment03,
            "level": 8
          }
        ]
      },
      "streamSettings": {
        "network": "tcp",
        "security": "tls",
        "tlsSettings": {
          "allowInsecure": true,
          "serverName": "segment04",
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
      "settings": {}
    },
    {
      "tag": "block",
      "protocol": "blackhole",
      "settings": {
        "response": {
          "type": "http"
        }
      }
    }
  ],
  "dns": {
    "servers": [
      "8.8.8.8"
    ]
  },
  "routing": {
    "domainStrategy": "Asls",
    "rules": []
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
  _tlsSettings["serverName"] = model.sni

  return _json
