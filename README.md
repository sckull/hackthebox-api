# HackTheBox API

* Unofficial python wrapper for hackthebox.eu API.
* Simple CLI application.
* **Original version : [sp1ral-vx/hackthebox-api](https://github.com/sp1ral-vx/hackthebox-api)**
* Added Simple Custom Markdown Table for ZZO Theme check it on [sckull](https://sckull.github.io).


# Install
`pip install -r requirements.txt`

# Usage
```
$ ./htb.py -h
usage: htb.py [-h] [-l] [-n NAME] [--reset] [-f flag] [-d difficulty] [--shout message] [-t NAME] [--aggressive]

HackTheBox CLI

optional arguments:
  -h, --help            show this help message and exit
  -l                    list available machines
  -n NAME               filter machine by name
  --reset               reset machine
  -f flag, --flag flag  Submit flag
  -d difficulty         Rate difficulty
  --shout message       Write message to shoutbox
  -t NAME, --table NAME
                        Table for machine in markdown context.
  --aggressive          Monitor shoutbox for machine resets and automatically cancel them
$
```

**Note:** Some options may not work.

## API KEY
Change API KEY in box.sh or just export it.
```
$ cat box.sh
#!/bin/bash

HTB_API_KEY=ZG9udGxvb2thdHRoaXNhd2Vzb21lQVBJS0VZ ./htb.py -t $1

$ export HTB_API_KEY=ZG9udGxvb2thdHRoaXNhd2Vzb21lQVBJS0VZ
$ ./htb.py -h
```

## Create table 
Check `get_table()` function on htb.py to modify the table.
```
$ ./box.sh -t Horizontall
Linux
Linux
>>>>> https://www.hackthebox.eu/storage/avatars/e4ec7d8504fdb58b5e6b7ddc82aafc77_thumb.png <<<<<<<<<< MAIN
****************************************
                Horizontall
****************************************
| Nombre | [Horizontall](https://www.hackthebox.eu/home/machines/profile/374) ![box_img_maker](data:image/png;base64,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)
|----------|:-------------:|
| **OS** | <span><p class="os_type"> Linux <img src="/images/icons/linux.png" class="img_type_os"/></p></span>
| **Puntos**   |  20
| **Dificultad** | Facil
|**IP** | 10.10.11.105
|**Maker** | <span><p class="user_maker"> [wail99](https://www.hackthebox.eu/home/users/profile/4005)<img src="https://www.hackthebox.eu/badge/image/4005" class="img_user_maker"/></p></span> 
|{{< button pointer="none">}}Matrix{{< /button >}} | {{< boxmd >}}
\```chart
{
   "type":"radar",
   "data":{
      "labels":["Enumeration","Real-Life","CVE","Custom Explotation","CTF-Like"],
      "datasets":[
         {
            "label":"User Rate",  "data":[5.8, 5.3, 6, 4, 4.7],
            "backgroundColor":"rgba(75, 162, 189,0.5)",
            "borderColor":"#4ba2bd"
         },
         { 
            "label":"Maker Rate",
            "data":[6, 9, 10, 0, 1],
            "backgroundColor":"rgba(154, 204, 20,0.5)",
            "borderColor":"#9acc14"
         }
      ]
   },
    "options": {"scale": {"ticks": {"backdropColor":"rgba(0,0,0,0)"},
            "angleLines":{"color":"rgba(255, 255, 255,0.6)"},
            "gridLines":{"color":"rgba(255, 255, 255,0.6)"}
        }
    }
}
\``` 
{{< /boxmd >}} |

```


