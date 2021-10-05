import re

class MyParser:
    def parse_input_file(self, input_file: str) -> list[str]:
        ipv6_check = re.compile(
            r"\b((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))\b")

        ipv4_check = re.compile(
            r"\b(((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\b")

        full_list_ips: list[str] = []

        #ipv4 check
        full_list_ips.extend(self._check_for_specific_ip(ipv4_check, input_file))
        #ipv6 check
        full_list_ips.extend(self._check_for_specific_ip(ipv6_check, input_file))
        return full_list_ips

    def _check_for_specific_ip(self, ip_check, input_file: str) -> list[str]:
        ips: list[str] = []

        with open(input_file) as file:
            for line in file:
                results = re.findall(ip_check, file)
                for item in results:
                    ips.append(item[0])
        return ips

    def parse_config(self) -> dict[str, str]:
        config_items: dict[str, str] = {}
        variable_search = re.compile(r"^(\w*)=([0-9a-zA-Z]*)$")
        with open('./setup/config.cfg') as file:
            for line in file:
                results = re.findall(variable_search, line)
                config_items[results[0]] = results[1]
        return config_items

    def parse_ip_file(self, input_file: str) -> list[str]:
        ips: list[str] = []
        with open(input_file) as file:
            for line in file:
                ips.append(line)
        return ips
