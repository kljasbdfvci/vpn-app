import json
from pathlib import Path

def generate(model):
  
  # read template
  f = open(Path(__file__).resolve().parent / "tempalate_trojan.json", "r")
  template = f.read()

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
