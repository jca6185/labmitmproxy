# Usage: mitmdump -s "js_injector.py src"
# (this script works best with --anticache)
# mas usos: http://pankajmalhotra.com/Injecting-Javascript-In-HTML-Content-Using-MITM-Proxy

from bs4 import BeautifulSoup
from libmproxy.protocol.http import decoded

# On start of proxy server ask for src as an argument

def start(context, argv):
   if len(argv) != 2:
       raise ValueError('Usage: -s "js_injector.py src"')
   context.src_url = argv[1]

def response(context, flow):
   with decoded(flow.response): # Remove content encoding (gzip, ...)
       html = BeautifulSoup(flow.response.content)
       """
       # To Allow CORS
       if "Content-Security-Policy" in flow.response.headers:
           del flow.response.headers["Content-Security-Policy"]
       """
       if html.body and ('text/html' in flow.response.headers["content-type"][0]):
           script = html.new_tag(
               "script",
               src=context.src_url)
           html.body.insert(len(html.body.contents, script)
           flow.response.content = str(html)
           context.log("******* Filter Injected *******")
