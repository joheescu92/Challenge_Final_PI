def load_name_files(path):

    archivos = []
    with open(path, "r") as file:
        for line in file:
            archivos.append(line.strip())

    return archivos