from rdiosock.services import RdioService


class RdioPrivateService(RdioService):
    __key__ = 'private'

    def publish_command(self, event, command_type, **kwargs):
        data = {
            'command': {
                'type': command_type
            }
        }

        for key, value in kwargs.items():
            data['command'][key] = value

        self.publish_event(event, data)