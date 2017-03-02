import base64

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = 'http://192.168.150.191 :3128'
#
#         # Use the following lines if your proxy requires authentication
#         # proxy_user_pass = "USERNAME:PASSWORD"
#         # setup basic authentication for the proxy
#         # encoded_user_pass = base64.encodestring(proxy_user_pass)
#         # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass