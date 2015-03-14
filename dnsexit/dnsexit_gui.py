#!/usr/bin/python3

import tkinter as tk
import urllib.request, re, os.path, sys
from tkinter import messagebox
import mysql.connector

################################################################################

class Application(tk.Frame):

    def __init__(self, master=None):
        self.config = {
            'user': 'root',
            'password': 'n0@cc3$$',
            'host': '192.168.0.66',
            'database': 'dnsexit',
            'raise_on_warnings': True,
        }

        self.db = mysql.connector.connect(**self.config)

        tk.Frame.__init__(self, master)
        self.grid()
        self.get_config()
        self.createWidgets()

    ############################################################################

    def createWidgets(self):
        self.top=self.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="Settings", command=self.settings)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Quit",command=self.quit)
        self.menubar.add_cascade(label="File",menu=self.filemenu)

        self.helpmenu = tk.Menu(self.menubar,tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help",menu=self.helpmenu)

        self.top.config(menu=self.menubar)

        # Current IP info
        #current_ip = self.get_ip()
        self.currentiplbl = tk.Label(self, text="Current IP:", justify=tk.RIGHT)
        self.currentiplbl.grid(row=0, column=0)
        self.u_currentip = tk.StringVar()
        self.showcurrentiplbl = tk.Label(self, textvariable=self.u_currentip)
        self.showcurrentiplbl.grid(row=0, column=1)

        if self.getip == '0':
            showcurrentip_button = tk.Button(self, text=u'Get IP', command=self.get_ip)
            showcurrentip_button.grid(row=0, column=2)
        else: self.get_ip()

        # Logged IP info
        self.loggediplbl = tk.Label(self, text="Logged IP:", justify=tk.RIGHT)
        self.loggediplbl.grid(row=1, column=0)
        self.u_loggedip = tk.StringVar()
        self.loggediplbl2 = tk.Label(self, textvariable=self.u_loggedip)
        self.loggediplbl2.grid(row=1, column=1)
        self.get_dat()

        self.updateiplbl = tk.Label(self, text="Update IP:", justify=tk.RIGHT)
        self.updateiplbl .grid(row=2, column=0)
        self.u_ip = tk.StringVar()
        self.updateIP = tk.Entry(self, textvariable=self.u_ip)
        self.updateIP.grid(row=2, column=1)
        copycurrentip_button = tk.Button(self, text=u'Copy IP', command=self.copy_ip)
        copycurrentip_button.grid(row=2, column=2)

        self.loginlbl = tk.Label(self, text="Login:", justify=tk.RIGHT)
        self.loginlbl.grid(row=3, column=0)
        self.u_login = tk.StringVar()
        self.login = tk.Entry(self, textvariable=self.u_login)
        self.login.grid(row=3, column=1)

        self.passwordlbl = tk.Label(self, text="Password:", justify=tk.RIGHT)
        self.passwordlbl.grid(row=4, column=0)
        self.u_password = tk.StringVar()
        self.password = tk.Entry(self, show='*', textvariable=self.u_password)
        self.password.grid(row=4, column=1)

        self.hostlbl = tk.Label(self, text="Host:", justify=tk.RIGHT)
        self.hostlbl.grid(row=5, column=0)
        self.u_host = tk.StringVar()
        self.host = tk.Entry(self, textvariable=self.u_host)
        self.host.grid(row=5, column=1)

        username_button = tk.Button(self, text=u'Update', command=self.update)
        username_button.grid(row=10, column=1)

    ############################################################################

    def get_ip(self):
      url="http://checkip.dyndns.org"
      response=urllib.request.urlopen(url)
      html=response.readall().decode('utf-8')
      if re.search('Current IP Address:',html):
        ip_pat=re.search("(\d+.\d+.\d+.\d+)",html)
        ip=ip_pat.group(0)

      #if ip: return ip
      self.u_currentip.set(ip)

    ############################################################################

    def get_config(self):
        if os.path.isfile('dnsexit.cfg'):
            with open('dnsexit.cfg') as f:
                content = [line.rstrip() for line in f]

                self.dat = content[0]
                self.getip = content[1]

    ############################################################################

    def log_ip(self,ip):
      log = open(self.dat, 'w')

      log.write(ip)

      log.close()

    ############################################################################

    def copy_ip(self):
      ip = self.u_currentip.get()
      self.u_ip.set(ip)

    ############################################################################

    def log_err(self, err):
      logerr = open('/var/log/dnsexit.err', 'w')

      logerr.write(err)

      logerr.close()

    ############################################################################

    def update(self):
      ip = self.u_ip.get()
      if self.update_ip(ip): self.log_ip(ip)
      logged_ip = self.get_dat

    ############################################################################

    def update_ip(self,ip):
      login = self.u_login.get()
      password = self.u_password.get()
      host = self.u_host.get()
      #url="http://update.dnsexit.com/RemoteUpdate.sv?login=macastillo&password=n0@cc3$$&host=macastillo.publicvm.com&myip=" + str(ip)
      url="http://update.dnsexit.com/RemoteUpdate.sv?login=" + str(login) + "&password=" + str(password) + "&host=" + str(host) + "&myip=" + str(ip)
      response=urllib.request.urlopen(url)
      html=response.readall().decode('utf-8')
      if re.search('Success',html):
        ret=True
      elif (re.search('1=',html) or re.search('4=',html)):
        tk.messagebox.showinfo('Update',"IP already up to date")

        self.updateIP.delete(0, tk.END)
        self.login.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.host.delete(0, tk.END)

        self.u_loggedip.set(ip)

        ret=True
      else:
        tk.messagebox.showinfo('Error!','Unable to update IP')
        #self.log_err('Unable to update ip')

        ret=False

      return ret

    ############################################################################

    def get_dat(self):
        logged_ip = "0"
        if os.path.isfile(self.dat):
            for line in open(self.dat,'r'):
                if re.search("(\d+.\d+.\d+.\d+)",line):
                    logged_ip = line

        self.u_loggedip.set(logged_ip)

    ############################################################################

    def about(self):
        tk.messagebox.showinfo('About',"DNSExit Updater Tool\nversion 1.0\n20140713\nGc0d3")

    ############################################################################

    def update_settings(x,y):
        tk.messagebox.showinfo('Restart',"You must restart the application\nfor changes to take affect.")

    ############################################################################

    def settings(self):
        self.settings = tk.Toplevel(self.master)
        self.settings.title("Settings")
        self.app = Settings(self.settings)

        self.app.bind("<Destroy>", self.update_settings)

################################################################################

class Settings(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.get_config()
        self.createWidgets()

    ############################################################################

    def createWidgets(self):
        self.top=self.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.datlbl = tk.Label(self, text="Data File Location: ", justify=tk.RIGHT)
        self.datlbl.grid(row=1, column=0)
        self.u_dat = tk.StringVar()
        self.updatedat = tk.Entry(self, textvariable=self.u_dat)
        self.u_dat.set(self.dat)
        self.updatedat.grid(row=1, column=1)

        self.checkip = tk.StringVar()
        self.getip = tk.Checkbutton(self, onvalue=1, offvalue=0, text=' Get IP startup', variable=self.checkip)
        if self.get_ip != '0':
            self.getip.select()
        self.getip.grid(row=2, column=0)

        update = tk.Button(self, text=u'Update', command=self.update_config)
        update.grid(row=10, column=0)

        close = tk.Button(self, text=u'Close', command=self.top.destroy)
        close.grid(row=10, column=1)

    ############################################################################

    def get_config(self):
        if os.path.isfile('dnsexit.cfg'):
            with open('dnsexit.cfg') as f:
                content = [line.rstrip() for line in f]

                self.dat = content[0]
                self.get_ip = content[1]

    ############################################################################

    def update_config(self):
        if os.path.isfile('dnsexit.cfg'):
            content = []
            content.append(self.u_dat.get())
            content.append(self.checkip.get())

            config = open('dnsexit.cfg', 'w')

            for item in content:
              config.write("%s\n" % item)

        self.top.destroy()

################################################################################

app = Application()
app.master.title('DNSExit Updater Tool')

app.mainloop()

#
#
#cnx.close()
