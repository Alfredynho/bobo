
class Attachment(object):

    def to_dict(self):
        return {
            'type': self.attachment_type,
            'payload': self.payload
        }


class FileAttachment(Attachment):

    attachment_type = 'file'

    def __init__(self, url):
        self._url = url

    @property
    def payload(self):
        return {
            'url': self._url
        }


class ImageAttachment(FileAttachment):
    attachment_type = 'image'


class VideoAttachment(FileAttachment):
    attachment_type = 'video'


class AudioAttachment(FileAttachment):
    attachment_type = 'audio'


class TemplateAttachment(Attachment):

    attachment_type = 'template'

    def __init__(self, template):
        self.template = template

    @property
    def payload(self):
        return self.template.to_dict()
