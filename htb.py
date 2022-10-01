#!/usr/bin/env python3
import sys
import re
import time
import base64
import requests

from htb.exceptions import HackTheBoxException
from htb.api import HackTheBox
from htb.machines import Machines
# from htb.challenges import Challenges
from htb.shoutbox import Shoutbox
from htb.pusher import Pusher
from htb.views import MachineViews
from htb.cli import HackTheBoxCLI
from htb.colorize import colorize
from htb.utils import Utils
from htb.utils import bcolors

class HackTheBoxClient(HackTheBox):
    '''HackTheBox Client app.'''
    def __init__(self):
        self.cli = HackTheBoxCLI()
        self._reset_pattern = re.compile(
            r'^([^ ]+) requested a reset on (\w+) \[([^\]]+)\] \[Type /cancel (\d+)'
        )
        self._timeout = 5

    def error(self, message: str):
        '''Error message logger.

        :param str message: error string.
        '''

        print(colorize('red', '[!] {}'.format(message)))
        sys.exit(1)

    def success(self, message: str):
        '''Success message logger.

        :param str message: message string.
        '''

        print(colorize('green', '[!] {}'.format(message)))

    def alert(self, message: str):
        '''Alert message logger.

        :param str message: message string.
        '''

        print(colorize('yellow', '[!] {}'.format(message)))

    def run(self):
        '''Main CLI aggregator.'''

        opts = self.cli.namespace
        if opts.reset:
            self.reset(opts)
        elif opts.flag:
            self.submit_flag(opts)
        elif opts.shout:
            self.shout(opts)
        elif opts.aggressive:
            self.aggressive(opts)
        elif opts.table:
            self.get_table(opts)
        else:
            self.list(opts)

    def reset(self, opts):
        '''Reset handler.'''

        if not opts.machine_name:
            self.error('Please specify exact machine name')

        machines = Machines()
        machine = machines.get_by_name(opts.machine_name)
        try:
            self.success(machines.reset(machine['id']))
        except HackTheBoxException as e:
            self.error(e)

    def submit_flag(self, opts):
        '''Flag submission handler.'''

        if not opts.machine_name:
            self.error('Please specify exact machine name')
        if opts.difficulty is None:
            self.error('Please specify difficulty')

        machines = Machines()
        machine = machines.get_by_name(opts.machine_name)
        try:
            self.success(
                machines.submit_flag(machine['id'], opts.difficulty, opts.flag)
            )
        except HackTheBoxException as e:
            self.error(e)

    def shout(self, opts):
        '''Shout handler.'''

        shoutbox = Shoutbox()
        result = shoutbox.send(opts.shout)
        self.success(result)

    def _wait_for_reset(self, machine: dict):
        chat = Pusher()
        while True:
            match = chat.match(self._reset_pattern)
            if match:
                self._handle_reset(machine, match)
            chat.flush()
            time.sleep(self._timeout)

    def _handle_reset(self, machine: dict, match: tuple):
        username, machine_name, vpn, reset_id = match
        self.alert('{} requested a reset on {} | {}. Reset id: {}'.format(
            username, machine_name, vpn, reset_id
        ))
        if machine_name == machine['name'] and vpn == 'us-free-1':
            shoutbox = Shoutbox()
            message = shoutbox.send('/cancel {}'.format(reset_id))
            self.success(message)

    def aggressive(self, opts):
        '''Aggressive handler.'''

        if not opts.machine_name:
            self.error('Please specify exact machine name')

        machines = Machines()
        machine = machines.get_by_name(opts.machine_name)
        self.success('Aggressive on {}'.format(machine['name']))
        try:
            self._wait_for_reset(machine)
        except KeyboardInterrupt:
            pass
        except HackTheBoxException as e:
            self.error(e)

    def list(self, opts):
        '''List machines handler.'''

        machines = Machines().load()
        machines.machines = machines._filter(
            retired=True, owned_root=True,
        )
        if opts.machine_name:
            machines.machines = machines._filter(name=opts.machine_name)        

        print(MachineViews(machines.machines))

    def get_table(self, opts):
        '''JSON machine handler.'''

        machines = Machines()
        util = Utils()
        table_machine = Machines()
        makers = ""
        difficulty = {50:"Insane",40:"Dificil",30:"Media",20:"Facil"}
        machines.machines = machines._filter()

        if opts.table:
            machines.machines = machines._filter(name=opts.table)
        # Machine info
        machine_info = table_machine.get(machines.machines[0]['id'])
        # Machine Matrix
        matrix = table_machine.get_matrix(machines.machines[0]['id'])

        # Machine Makers
        if machine_info["maker2"]:            
            #makers = f"""<span><p class="user_maker" style="margin: auto;"> [{machine_info['maker']['name']}](https://www.hackthebox.eu/home/users/profile/{machine_info['maker']['id']})<img src="https://www.hackthebox.eu/badge/image/{machine_info['maker']['id']}" class="img_user_maker"/> </p> <hr style="opacity:25%;"> <p class="user_maker" style="margin: auto;"> [{machine_info['maker2']['name']}](https://www.hackthebox.eu/home/users/profile/{machine_info['maker2']['id']})<img src="https://www.hackthebox.eu/badge/image/{machine_info['maker2']['id']}" class="img_user_maker"/> </p></span>"""
            makers = f"""<span><p class="user_maker"> [{machine_info['maker']['name']}](https://www.hackthebox.eu/home/users/profile/{machine_info['maker']['id']})<img src="https://www.hackthebox.eu/badge/image/{machine_info['maker']['id']}" class="img_user_maker"/> </p> <hr style="opacity:25%;"> <p class="user_maker2"> [{machine_info['maker2']['name']}](https://www.hackthebox.eu/home/users/profile/{machine_info['maker2']['id']})<img src="https://www.hackthebox.eu/badge/image/{machine_info['maker2']['id']}" class="img_user_maker"/> </p></span>"""
        else:
            #makers = f"""<span><p class="user_maker" style="margin: auto;"> [{machine_info['maker']['name']}](https://www.hackthebox.eu/home/users/profile/{machine_info['maker']['id']})<img src="https://www.hackthebox.eu/badge/image/{machine_info['maker']['id']}" class="img_user_maker"/></p></span>"""
            makers = f"""<span><p class="user_maker"> [{machine_info['maker']['name']}](https://www.hackthebox.eu/home/users/profile/{machine_info['maker']['id']})<img src="https://www.hackthebox.eu/badge/image/{machine_info['maker']['id']}" class="img_user_maker"/></p></span>"""
        
        # OS Type
        if machine_info['os']:
            #print(machine_info['os'])
            if machine_info['os'] == "Linux":
                # print("Linux")
                machine_type = '<span><p class="os_type"> Linux <img src="/images/icons/linux.png" class="img_type_os"/></p></span>'
            elif machine_info['os'] == "Windows":
                # print("Windows")
                machine_type = '<span><p class="os_type"> Windows <img src="/images/icons/win.png" class="img_type_os"/></p></span>'
            elif machine_info['os'] == "OpenBSD":
                # print("OpenBSD")
                machine_type = '<span><p class="os_type"> OpenBSD <img src="/images/icons/openbsd.png" class="img_type_os"/></p></span>'
            elif machine_info['os'] == "Android":
                # print("Android")
                machine_type = '<span><p class="os_type"> Android <img src="/images/icons/android.png" class="img_type_os"/></p></span>'            
            elif machine_info['os'] == "Other":
                # print("Other")
                machine_type = 'Other'
            elif machine_info['os'] == "FreeBSD":
                # print("FreeBSD")
                machine_type = '<span><p class="os_type"> FreeBSD <img src="/images/icons/freebsd.png" class="img_type_os"/></p></span>'
            else:
                # print("System type not found")
                machine_type = 'OS'




        avatar_machine = util.get_img_machine(machine_info['avatar_thumb'])
        if avatar_machine == False:
            avatar_machine = util.get_img_machine(machine_info['avatar'])

        # Machine Table Markdown
        table =f"""| Nombre | [{ machine_info['name']}](https://www.hackthebox.eu/home/machines/profile/{machine_info['id'] }) { avatar_machine }
|----------|:-------------:|
| **OS** | {machine_type}
| **Puntos**   |  {machine_info['points']}
| **Dificultad** | {difficulty[machine_info['points']]}
|**IP** | {machine_info['ip']}
|**Maker** | {makers} """+"""
|{{< button pointer="none">}}Matrix{{< /button >}} | {{< boxmd >}}
```chart
{
   "type":"radar",
   "data":{
      "labels":["Enumeration","Real-Life","CVE","Custom Explotation","CTF-Like"],
      "datasets":[
         {
            "label":"User Rate", """ + f""" "data":{matrix['aggregate']},
            "backgroundColor":"rgba(75, 162, 189,0.5)",
            "borderColor":"#4ba2bd"
         }},
         {{ """ + f"""
            "label":"Maker Rate",
            "data":{matrix['maker']},
            "backgroundColor":"rgba(154, 204, 20,0.5)",
            "borderColor":"#9acc14"
         }}""" + """
      ]
   },
    "options": {"scale": {"ticks": {"backdropColor":"rgba(0,0,0,0)"},
            "angleLines":{"color":"rgba(255, 255, 255,0.6)"},
            "gridLines":{"color":"rgba(255, 255, 255,0.6)"}
        }
    }
}
``` 
{{< /boxmd >}} |
"""
        print(bcolors.HEADER+str("*"*40))
        print("\t\t"+str(opts.table))
        print(str("*"*40)+bcolors.END)
        print(bcolors.OKGREEN + table + bcolors.END)

        

if __name__ == '__main__':
    try:
        HTB = HackTheBoxClient()
        HTB.run()
    except HackTheBoxException as e:
        print(e, file=sys.stderr)
        sys.exit(1)
