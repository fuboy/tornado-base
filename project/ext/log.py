from project.modules.log.models import Log


def add_log(alchobj, msg_type, msg, user=None):
    log = Log()

    log.object = alchobj
    log.message_type = msg_type
    log.message = msg

    Log.add(log, user)