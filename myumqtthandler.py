handlers = {}


def lockcom(client, msg):
    client.pub("lock", {"msg": f"Received: {msg}"})


handlers["lockcom"] = lockcom