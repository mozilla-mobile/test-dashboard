"""Telemetry Probe Expiry Monitor.

PURPOSE:
The purpose of this module is to:
1. Monitor telemetry probe YAML files for expired probes
2. Send a slack notification for (soon-to-be) expired probes

"""
import argparse
import configparser
import datetime
import sys
import re
import urllib.request
import yaml


CONFIG_INI = 'check_metrics.ini'
PAYLOAD_JSON = 'slack-payload.json'
WARN_THRESHOLD_DAYS = 7
expired_already = []
expiring_soon = []


METRICS_FILENAME = 'metrics.yaml'


def parse_args(cmdln_args):
    p = projects(CONFIG_INI)
    parser = argparse.ArgumentParser(
        description=f"Generate {PAYLOAD_JSON} file"
    )

    parser.add_argument(
        "-p", "--project",
        help="Indicate project",
        required=True,
        choices=p
    )
    return parser.parse_args(args=cmdln_args)


def filestream(filename):
    with open(filename, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f'YAML error: {exc}')


def soon_expiring(date_input, warn_threshold_days):
    """ Parse dates into 3 categories:
    1. Already expired - date_input <= today (i.e. before today)
    2. Soon expiring - date_input > today but <= the number of upcoming days to watch
    3. Not expiring - date_input > the number of upcoming days to watch
    """

    # format dates
    date_input_formatted = datetime.datetime.strptime(date_input, '%Y-%m-%d')
    today_formatted = datetime.datetime.today()

    # date differential as # of days to warning threshold
    differential_days = (date_input_formatted -  today_formatted).days

    return differential_days

def is_date_format(date_input):
    pattern_str = r'^\d{4}-\d{2}-\d{2}$'
     
    if re.match(pattern_str, date_input):
        return True 
    else:
        return False


def projects(CONFIG_INI):
    config = configparser.ConfigParser()
    config.read(CONFIG_INI)
    s = config.sections()
    return list(s)


def project(CONFIG_INI, project_name):
    """ Given a project name, download telemetry yaml, return warn window """

    config = configparser.ConfigParser()
    #c = config.read(CONFIG_INI)
    #config.read('check_metrics.ini')
    config.read(CONFIG_INI)

    # pull data from a single project
    url = config.get(project_name, 'file')
    warn = config.get(project_name, 'WARN_THRESHOLD_DAYS')

    # download metrics yaml file
    urllib.request.urlretrieve(url, METRICS_FILENAME)
    return warn


def output_format(metric):
    tmp = metric.replace("']['", ".")
    return tmp.replace("'","").replace("]", "").replace("[", "")


def output_json_row(name_probe, date_expire, days):
   
    prefix = '{ "type": "section", "text": { "type": "mrkdwn", "text": ' 
    suffix = ' } },'
    if int(days) == 0:
        row = f"{name_probe} - expiration: {date_expire} (today)"
    elif int(days) < 0:
        days = abs(days)
        row = f"{name_probe} - expiration: {date_expire} ({days} days ago)"
    else:
        row = f"{name_probe} - expiration: {date_expire} (in {days} days)"
    return f'{prefix} "{row}" {suffix} \n'

def create_probe_lists(metrics, prefix=''):

    if isinstance(metrics, dict):
        for k, v2 in metrics.items():
            p2 = "{}['{}']".format(prefix, k)
            create_probe_lists(v2, p2)

    elif isinstance(metrics, list):
        for i, v2 in enumerate(metrics):
            p2 = "{}[{}]".format(prefix, i)
            create_probe_lists(v2, p2)
    else:
        result = str(metrics)
        tmp = []
        if 'expires' in prefix:
            if is_date_format(result):
                exp = soon_expiring(result, WARN_THRESHOLD_DAYS)
                if exp:
                    #print(f'WARN_THRESHOLD_DAYS: {WARN_THRESHOLD_DAYS}: {prefix}: {result}, {exp}')
                    #tmp = [prefix, result]
                    tmp = [prefix, result, exp]
                    if exp <=0:
                        expired_already.append(tmp)
                    elif (exp > 0 and exp <= WARN_THRESHOLD_DAYS):
                        expiring_soon.append(tmp)
                    else:
                        print('not expiring!')
                        

def generate_payload(name_project, expired_already, expiring_soon):
    
    payload = ""
    p_expired = ""
    p_expiring = ""

    # payload section: already expired
    if expired_already:
        p_expired+= '{ "type": "divider" }, { "type": "section", "text": { "type": "mrkdwn", "text": "*ALREADY EXPIRED* :traffic-red:" } },'

        for item in expired_already:
            name_probe = output_format(item[0])
            date_expire = item[1] 
            days = item[2]
            p_expired += output_json_row(name_probe, date_expire, days)

    # payload section: expiring soon 
    if expiring_soon:
        payload += '{ "type": "divider" }, { "type": "section", "text": { "type": "mrkdwn", "text": "*EXPIRING SOON* :traffic-yellow:" } },'

        for item in expiring_soon:
            name_probe = output_format(item[0])
            date_expire = item[1] 
            days = soon_expiring(item[1], warn_threshold_days=WARN_THRESHOLD_DAYS)
            p_expiring += output_json_row(name_probe, date_expire, days)


    # payload header
    payload += '{ "blocks": [ { "type": "header", "text": { "type": "plain_text", "text": "telemetry probe expiry: '
    payload += name_project
    payload += ' :firefox: " } },'

    if p_expired or p_expiring:
       payload += p_expired
       payload += p_expiring
    else:
        payload += '{ "type": "divider" }, { "type": "section", "text": { "type": "mrkdwn", "text": "*NONE EXPIRING* :traffic-green:" } },'

    # payload footer
    payload += '{ "type": "divider" }, { "type": "context", "elements": [ { "type": "mrkdwn", "text": ":testops-notify: created by <https://mozilla-hub.atlassian.net/wiki/spaces/MTE/overview|Mobile Test Engineering>" } ] } ] }'

    with open(PAYLOAD_JSON, 'w') as f:
        f.write(payload)

def main():
    """
    name_project = 'firefox-android'
    name_project = 'focus-android'
    #name_project = 'android-components'
    name_project = 'focus-ios'
    name_project = 'firefox-android'
    """

    args = parse_args(sys.argv[1:])
    name_project = args.project

    project(CONFIG_INI, name_project) 
    metrics = filestream(METRICS_FILENAME)
    create_probe_lists(metrics)
    generate_payload(name_project, expired_already, expiring_soon)


if __name__ == '__main__':
    main()











