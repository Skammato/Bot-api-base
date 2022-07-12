import re
from io import StringIO
from html.parser import HTMLParser
from typing import Union, List, Optional
import requests

text = requests.get('https://core.telegram.org/bots/api#available-methods').text

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
        self.excluded = [
        "getUpdates",
        "setWebhook",
        "deleteWebhook",
        "getWebhookInfo"
        ]
        path = './tg_api/methods/'
        text = requests.get('https://core.telegram.org/bots/api#available-methods').text
        #'<h4><a class="anchor" name="\w+" href="#\w+"><i class="anchor-icon"></i></a>(\w+)</h4>\n<p>(.+)</p>\n(?!<h4>)<table class="table">\n<thead>\n<tr>(\n<th>\w+</th>){1,4}\n</tr>\n</thead>\n<tbody>(\n<tr>\n<td>(\w+)</td>\n<td>(.+)</td>\n<td>(\w+)</td>\n<td>(.+)</td>\n</tr>)+\n</tbody>\n</table>'
        pattern = '<h4><a class="anchor" name="\w+" href="#\w+"><i class="anchor-icon"></i></a>(\w+)</h4>(\n<p>(.+)</p>)*\n(?!<h4>)<table class="table">\n<thead>\n<tr>(\n<th>\w+</th>){1,4}\n</tr>\n</thead>\n<tbody>((\n<tr>\n<td>(\w+)</td>\n<td>(.+)</td>\n<td>(\w+)</td>\n<td>(.+)</td>\n</tr>)+)\n</tbody>\n</table>'
        for m in re.finditer(pattern, text):
            r = self.getminfo(m.groups())
            if r['name'] not in self.excluded:
                if r['name'] == "sendMessage":
                    self.create(path, r)
                    #print(r)
    def getminfo(self, groups: tuple) -> list:
        name, desc = groups[0], groups[1]
        paramns_list = re.findall(
        r'\n<tr>\n<td>(\w+)</td>\n<td>(.+)</td>\n<td>(\w+)</td>\n<td>(.+)</td>\n</tr>',
        groups[4]
        )
        plist = []
        for param_info in paramns_list:
            plist.append({
            "name":param_info[0],
            "type":self.get_py_type(param_info[1]),
            "required":True if param_info[2] == 'Yes' else False,
            "desc":param_info[3]
            })
        return {
        "name":name,
        "desc":desc,
        "paramns":plist,
        "rtype":self.get_return_type(desc)
        }
    def get_return_type(self, desc: str):
        rtype = ""
        if re.search(r'On success, the sent <a href="#message">Message</a> is returned\.', desc):
            rtype = "Message"
        elif re.search(r'Returns the <a href="#messageid">MessageId</a>', desc):
            rtype = "MessageId"
        elif re.search(r'Returns <i>True</i> on success', desc):
            return bool
        elif re.search(r'Returns the uploaded <a href="#file">File</a> on success', desc):
            rtype = "File"
        elif re.search(r'as <i>String</i> on success', desc):
            return str
        else:
            m = re.search(r'Returns .+ as <a href="#\w+">(?P<obj>\w+)</a> object', desc)
            if m:
                obj = m.group('obj')
                rtype = obj if obj else ""
        #if rtype == "": print("Non trovato nessuno type")
        return rtype if rtype else ""

    def get_py_type(self, types_str: str):
        #pattern = r'(\w+|(<a href="#\w+">\w+</a>))\sor\s(\w+|())'
        accepted = []
        for type_str in re.split(r'\sor\s', types_str):
            py_type = None
            m = re.findall(r'(\w+)|(<a href="#\w+">\w+</a>)', type_str)[0]
            if m[0] == 'Array':
                obj = re.split(r'\s?Array\sof\s', type_str)[1::]
                n = len(obj)
                py_type = "List["*n+Builder.decode_a_tag(obj[-1])+"]"*n
            elif m[0] != '':
                py_type = Builder.get_type_by_str(m[0])
            elif m[1] != '':
                py_type = Builder.decode_a_tag(m[1])#Custom(re.match(r'<a href="#\w+">(\w+)</a>').group(1))
            else:
                if m[2] != '':
                     print("m[2]", m[2])
            accepted.append(py_type)
        return accepted
    def build_types(self, ptype: str) -> str:
        text = ""
        if len(ptype) > 0:
            text += f"Union[{', '.join([str(t) for t in ptype])}]"
        else:
            text += str(ptype[0])
        return text
    def build_args(self, paramns: list) -> str:
        final = ""
        for param in paramns:
            a = param['name']
            if param['required']:
                a += ": "+self.build_types(param['type'])
            else:
                a += f": Optional[{self.build_types(param['type'])}]"
            final += a+', '
        return final
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()
    def remove_html(self, html: str):
        self.feed(html)
        return self.get_data()
    def create(self, path: str, m: dict):
        string = 'from typing import *\n\nasync def {name}(self, {arguments}){rtype}:\n'+' '*4
        string += '"""{desc}"""\n'+' '*4
        string += 'args = locals()\n'+' '*4
        string += 'return (await self.send({name}, args, {rtype}))'
        #string += 'default = [{default_paramns}]\n'+' '*4
        #string += ''
        final = string.format(
        name=m['name'],
        desc=self.remove_html(m['desc']),
        arguments=self.build_args(m['paramns']),
        rtype=m['rtype']
        )
        f = open(path+m['name']+".py", "w")
        f.write(final)
        f.close()

class Builder:
    table = {
    "Integer":'int',
    "String":'str',
    "Boolean":'bool',
    "Float":'float',
    }
    def get_type_by_str(t: str):
        return Builder.table[t]
    def decode_a_tag(text: str):
        m = re.match(r'<a href="#\w+">(\w+)</a>', text)
        if m:
            return m.group(1)
        else:
            return str(Builder.get_type_by_str(text))
