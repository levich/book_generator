import yaml

t = yaml.load(open("sample.yaml", "r"), Loader=yaml.CLoader)
print(t)
