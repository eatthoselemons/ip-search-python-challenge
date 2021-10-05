class MyWriter:
    def write_ip_list(self, data: list[str], output_file: str):
        textfile = open(output_file, "w")
        for element in data:
            textfile.write(element + "\n")
        textfile.close()

    def write_data_list(self, data: dict[str, str], output_file: str, calling_function: str):
        textfile = open(output_file, "w")
        for key, value in data.items():
            textfile.write(f"{key}: {calling_function} {value}" + "\n")
        textfile.close()