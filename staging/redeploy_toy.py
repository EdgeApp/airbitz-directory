import web
import json
import subprocess
import os
import pwd

from wsgilog import WsgiLog

class Log(WsgiLog):
    def __init__(self, app):
        WsgiLog.__init__(
            self, app,
            logformat = '%(message)s',
            tofile = True,
            toprint = True,
            file = '/tmp/redeploy_toy.log')

urls = ( '/.*', 'Redeploy')
app = web.application(urls, globals())

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

class Redeploy:
    def POST(self):
        production = "bitz" == get_username() 
        data = web.input()
        body = json.loads(data.payload)
        print json.dumps(body, indent=2)
        print "User %s" % get_username()
        print "Production %s" % production
        print "Is %s okay?" % body['repository']['name']
        if body['repository']['name'] != "airbitz-directory":
            print "No"
            return self.sorry_stud()
        print "Is %s okay?" % body['ref']
        if (production and body['ref'] != "refs/heads/deploy") \
            or (not production and body['ref'] != "refs/heads/staging") :
            print "No"
            return self.sorry_stud()
            
        (self.static_files, self.database) = (False, False)
        for commit in body['commits']:
            self.file_check(commit['added'])
            self.file_check(commit['modified'])
            self.file_check(commit['removed'])
        success = self.redeploy(production)
        web.header('Content-Type', 'application/json')
        print 'Success? %s' % success
        if success:
            return json.dumps({ "message": "Ooooh Github...that was amazing! Want a smoke?" })
        else:
            return json.dumps({ "message": "Meh...I've had better." })

    def sorry_stud(self):
        print 'Sorry stud. No dice.'
        return json.dumps({ "message": "Sorry stud." })

    def redeploy(self, production):
        print 'Running redeploy'
        u = get_username()
        p = subprocess.Popen("sudo su - {0}".format(u), shell=True, stdin=subprocess.PIPE)
        try:
            home = '/home/%s/' % get_username()
            print 'Home is %s' % home
            (cin, cout) = (p.stdin, p.stdout)
            cin.write("cd %s\n" % home)
            cin.write("source %s/.bashrc 1>>/tmp/redeploy_toy.log 2>&1\n" % home)
            cin.write("source quick_bitz.sh 1>>/tmp/redeploy_toy.log 2>&1\n")
            cin.write("source /etc/profile.d/environment_vars.sh 1>>/tmp/redeploy_toy.log 2>&1\n")
            if production:
                print 'Pulling Deploy'
                cin.write("git pull origin deploy 1>>/tmp/redeploy_toy.log 2>&1\n")
            else:
                print 'Pulling Deploy'
                cin.write("git pull origin staging 1>>/tmp/redeploy_toy.log 2>&1\n")
            if self.static_files:
                print 'Running collectstatic'
                cin.write("python manage.py collectstatic --noinput 1>>/tmp/redeploy_toy.log 2>&1\n")
            if self.database:
                print 'Running migrate'
                cin.write("python manage.py migrate 1>>/tmp/redeploy_toy.log 2>&1\n")
            print 'Running restart_gunicorn'
            cin.write("./restart_gunicorn.sh 1>/tmp/restart.out 1>>/tmp/redeploy_toy.log 2>&1\n")
            print 'Finished'
            p.stdin.close()
            if p.wait() != 0:
                return False
            return True
        except Exception as e:
            print e
        return False

    def file_check(self, files):
        for f in files:
            if f.find("static") > -1:
                self.static_files = True
            if f.find("migrations") > -1:
                self.database = True

if __name__ == "__main__":
    app.run(Log)

