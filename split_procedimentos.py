#!/usr/bin/env python3
"""Split ef7cf93c-procedimentov62.html into individual service files."""

import re
import os

SRC = '/root/.claude/uploads/3a8471dc-f72f-4823-898f-e3c8c807de9c/ef7cf93c-procedimentov62.html'
OUT = '/home/user/Estat-stica/procedimentos'

# Individual services (single-specialty files)
INDIVIDUAL = [
    {'id': 'ortopedia',      'label': 'Ortopedia',            'icon': '🦴'},
    {'id': 'cuid_intermedio','label': 'Cuidados Intermédios', 'icon': '🏥'},
    {'id': 'uci',            'label': 'UCI',                  'icon': '❤️'},
    {'id': 'cirurgia',       'label': 'Cirurgia',             'icon': '🔪'},
    {'id': 'maxilo',         'label': 'Maxilo Facial',        'icon': '🦷'},
    {'id': 'consulta_ext',   'label': 'Consulta Externa',     'icon': '📋'},
    {'id': 'nefrologia',     'label': 'Nefrologia',           'icon': '🫘'},
    {'id': 'hosp_dia',       'label': 'Hospital de Dia',      'icon': '☀️'},
    {'id': 'neurocirurgia',  'label': 'Neurocirurgia',        'icon': '🧠'},
    {'id': 'otorrino',       'label': 'Otorrinolaringologia', 'icon': '👂'},
    {'id': 'banco_urg',      'label': 'Banco de Urgência',    'icon': '🚨'},
]

# Combined groups: (filename_id, page_label, specialties_js_block)
GROUPS = [
    (
        'bloco_op',
        'Bloco Operatório',
        """const SPECIALTIES = [
  { id:'bloco_op',       label:'Bloco Operatório',  icon:'🩺' },
  { id:'bloco_urgente',  label:'Bloco Op. Urgente', icon:'🚑' },
  { id:'bloco_electiva', label:'Bloco Op. Electiva',icon:'📅' },
];"""
    ),
    (
        'medicina',
        'Medicina',
        """const SPECIALTIES = [
  { id:'med_homem',  label:'Medicina Homem',  icon:'👨‍⚕️' },
  { id:'med_mulher', label:'Medicina Mulher', icon:'👩‍⚕️' },
  { id:'medicina',   label:'Medicina (Auto)', icon:'💊' },
];"""
    ),
]

with open(SRC, 'r', encoding='utf-8') as f:
    original = f.read()

specialties_pattern = re.compile(r'const SPECIALTIES = \[.*?\];', re.DOTALL)

def make_file(content, label, filename):
    content = content.replace(
        '<title>Serviço de Procedimentos de Enfermagem</title>',
        f'<title>Procedimentos do Serviço de {label}</title>'
    )
    content = content.replace(
        '<span>Serviço de Procedimentos de Enfermagem</span>',
        f'<span>Procedimentos do Serviço de {label}</span>'
    )
    out_path = os.path.join(OUT, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✓  {filename}  →  Procedimentos do Serviço de {label}')

# Individual files
for sp in INDIVIDUAL:
    new_array = (
        f"const SPECIALTIES = [\n"
        f"  {{ id:'{sp['id']}', label:'{sp['label']}', icon:'{sp['icon']}' }},\n"
        f"];"
    )
    modified = specialties_pattern.sub(new_array, original)
    make_file(modified, sp['label'], f"proc_{sp['id']}.html")

# Combined group files
for (fid, label, array_js) in GROUPS:
    modified = specialties_pattern.sub(array_js, original)
    make_file(modified, label, f"proc_{fid}.html")

total = len(INDIVIDUAL) + len(GROUPS)
print(f'\nGerados {total} ficheiros em {OUT}/')
