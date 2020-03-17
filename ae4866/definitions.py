def read_succesfull(path):
    with open(path, "r") as f:
        v = int(f.read())

    if v == 1:
        return True
    
    else:
        return False

def read_number(path):
    with open(path, "r") as f:
        return float(f.read())