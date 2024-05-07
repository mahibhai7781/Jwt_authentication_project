from rest_framework import renderers
import json 

class UserRenderer(renderers.JSONOpenAPIRenderer):
    charset = 'utf-8'
    def render(self,data,accepted_madia_types=None,renderer_context=None):

        reponse = ''
        if 'ErrorDetails' in str(data):
            reponse = json.dumps({"errors":data})
        else:
            reponse = json.dumps(data)
        return reponse
