from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import SimpleHTTPServer
import SocketServer
import urlparse
import sys
import thread
import argparse

class OAuthHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if '?' in self.path:
            path, query_string = self.path.split('?', 1)
            query_parameters = urlparse.parse_qs(query_string)
            self.path = path
            if 'code' in query_parameters:
                global code
                code = query_parameters['code'][0]

        if self.path != "/auth_return":
            self.send_response(307)
            self.send_header('Location', auth_uri)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            if "code" in globals():
                self.wfile.write("<h1>Process Complete!</h1>")
            else:
                self.wfile.write("<h1>Something went wrong, please try again.</h1>")
            def stop():
                server.shutdown()
            thread.start_new_thread(stop,())

    def log_message(self, format, *args):
        pass

def get_arguments():
    parser = argparse.ArgumentParser(description="Get OAuth2 token to access the Google APIs on behalf of a user")
    parser.add_argument('scope', help="the google OAuth2 scope to request")
    parser.add_argument('-s', '--secret', default="client_secret.json", help="the client secret file to use for authentication")
    parser.add_argument('-c', '--credentials', default="credentials.json", help="the file to save the auth credentials to")
    parser.add_argument('-p', '--port', default=8000, help="the port to run the local server on")

    args = vars(parser.parse_args())

    return args['scope'], args['secret'], args['credentials'], args['port']


def main():
    scope, client_secret, credentials_file, port = get_arguments()

    flow = flow_from_clientsecrets(client_secret, scope=scope, redirect_uri='http://localhost:8000/auth_return')
    flow.params.update({'approval_prompt': 'force'})

    global auth_uri
    auth_uri = flow.step1_get_authorize_url()

    print "Please connect to http://localhost:" + str(port) + " to continue"

    global server
    server = SocketServer.TCPServer(("localhost", port), OAuthHandler)
    server.serve_forever()

    credentials = flow.step2_exchange(code)

    storage = Storage(credentials_file)
    storage.put(credentials)

    print "Credentials have been saved to", credentials_file

if __name__ == "__main__":
    main()
