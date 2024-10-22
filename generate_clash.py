import yaml
import json

def parse_list_file(filename):
    rules = {}
    with open(filename, 'r') as f:
        current_category = None
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                current_category = line[1:].strip()
                rules[current_category] = {'domain_suffix': [], 'domain_keyword': []}
            elif line:
                if 'DOMAIN-SUFFIX' in line:
                    domain = line.split(',', 1)[1].strip()
                    rules[current_category]['domain_suffix'].append(domain)
                elif 'DOMAIN-KEYWORD' in line:
                    keyword = line.split(',', 1)[1].strip()
                    rules[current_category]['domain_keyword'].append(keyword)
    return rules

def generate_karing_json(rules):
    karing_rules = []
    for category, domains in rules.items():
        karing_rules.append({
            "domain_keyword": domains.get('domain_keyword', []),
            "domain_suffix": domains.get('domain_suffix', [])
        })
    karing_config = {"version": 1, "rules": karing_rules}
    with open('Karing.json', 'w') as f:
        json.dump(karing_config, f, separators=(',', ':'))  # Генерация в одну строку

def generate_shadowrocket_conf(rules):
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
        for category, domains in rules.items():
            f.write(f"#{category}\n")
            for domain in domains['domain_suffix']:
                f.write(f"DOMAIN-SUFFIX,{domain},PROXY\n")
            for keyword in domains['domain_keyword']:
                f.write(f"DOMAIN-KEYWORD,{keyword},PROXY\n")

def generate_clash_yaml(rules):
    with open('Clash.yaml', 'w') as f:
        f.write("payload:\n")
        for category, domains in rules.items():
            f.write(f"  # {category}\n")
            for domain in domains['domain_suffix']:
                f.write(f"  - DOMAIN-SUFFIX,{domain}\n")
            for keyword in domains['domain_keyword']:
                f.write(f"  - DOMAIN-KEYWORD,{keyword}\n")

if __name__ == "__main__":
    rules = parse_list_file('list.lst')
    generate_clash_yaml(rules)
    generate_shadowrocket_conf(rules)
    generate_karing_json(rules)
