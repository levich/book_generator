import codecs
import sys
import textwrap
from ruamel.yaml import YAML


yaml = YAML(typ='unsafe', pure=True)
file_name = r'toto.txt'
text = """
Привет!
Я твой корвет
"""
textDict = {"data": text}

yaml.default_style="|"
yaml.dump(textDict,sys.stdout)
# with open(file_name, 'w') as fp:
#     yaml.dump(textDict, stream=fp)
# print('yaml dump dict 1   : ' + open(file_name).read()),
# f = codecs.open(file_name,"w",encoding="utf-8")
# f.write('yaml dump dict 2   : ' + yaml.dump(textDict).decode('utf-8'))
# f.close()
# print(open(file_name).read())