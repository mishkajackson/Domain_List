import yaml
import json

def parse_list_file(filename):
    domain_suffix = set()  # Используем set для избежания дубликатов
    domain_keyword = set()

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue  # Пропускаем строки с комментариями
            elif line:
                if 'DOMAIN-SUFFIX' in line:
                    domain = line.split(',', 1)[1].strip()
                    domain_suffix.add(domain)
                elif 'DOMAIN-KEYWORD' in line:
                    keyword = line.split(',', 1)[1].strip()
                    domain_keyword.add(keyword)

    return list(domain_suffix), list(domain_keyword)

def generate_karing_json(domain_suffix, domain_keyword):
    karing_config = {
        "version": 1,
        "rules": [{
            "domain_keyword": domain_keyword,
            "domain_suffix": domain_suffix
        }]
    }
    with open('Karing.json', 'w') as f:
        json.dump(karing_config, f, separators=(',', ':'))  # Генерация в одну строку

def generate_shadowrocket_conf(domain_suffix, domain_keyword):
    with open('Shadowrocket.conf', 'w') as f:
        f.write("[General]\n")
        f.write("bypass-system = true\n")
        f.write("skip-proxy = 127.0.0.1, 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local, captive.apple.com\n")
        f.write("bypass-tun = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, "
                "192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.18.0.0/15, 198.51.100.0/24, 203.0.113.0/24, "
                "224.0.0.0/4, 255.255.255.255/32\n")
        f.write("dns-server = https://dns.adguard-dns.com/dns-query, 8.8.8.8, 8.8.4.4\n")
        f.write("fallback-dns-server = system\n")
        f.write("update-url = https://raw.githubusercontent.com/mishkajackson/Domain_List/refs/heads/main/Shadowrocket.conf\n\n")
        f.write("[Rule]\n")
        for domain in domain_suffix:
            f.write(f"DOMAIN-SUFFIX,{domain},PROXY\n")
        for keyword in domain_keyword:
            f.write(f"DOMAIN-KEYWORD,{keyword},PROXY\n")

def generate_clash_yaml(domain_suffix, domain_keyword):
    with open('Clash.yaml', 'w') as f:
        f.write("payload:\n")
        for domain in domain_suffix:
            f.write(f"  - DOMAIN-SUFFIX,{domain}\n")
        for keyword in domain_keyword:
            f.write(f"  - DOMAIN-KEYWORD,{keyword}\n")

if __name__ == "__main__":
    domain_suffix, domain_keyword = parse_list_file('list.lst')
    generate_clash_yaml(domain_suffix, domain_keyword)
    generate_shadowrocket_conf(domain_suffix, domain_keyword)
    generate_karing_json(domain_suffix, domain_keyword)
