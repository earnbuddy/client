from requests import get


def get_ip_info():
    ip = get('https://api.ipify.org').content.decode('utf8')
    return (ip)
