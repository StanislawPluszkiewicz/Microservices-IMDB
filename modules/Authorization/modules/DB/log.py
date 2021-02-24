import coloredlogs, logging
from pymongo import monitoring

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=logger)

class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        logger.info(" Command {0.command_name} with request id "
                 "{0.request_id} started on server "
                 "{0.connection_id}".format(event))

    def succeeded(self, event):
        logger.debug("Command {0.command_name} with request id "
                 "{0.request_id} on server {0.connection_id} "
                 "succeeded in {0.duration_micros} "
                 "microseconds".format(event))

    def failed(self, event):
        logger.warn("Command {0.command_name} with request id "
                 "{0.request_id} on server {0.connection_id} "
                 "failed in {0.duration_micros} "
                 "microseconds".format(event))

monitoring.register(CommandLogger())