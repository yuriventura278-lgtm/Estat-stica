#!/usr/bin/env python3
"""Split ef7cf93c-procedimentov62.html into 17 individual service files."""

import re
import os

SRC = '/root/.claude/uploads/3a8471dc-f72f-4823-898f-e3c8c807de9c/ef7cf93c-procedimentov62.html'
OUT = '/home/user/Estat-stica/procedimentos'

SPECIALTIES = [
    {'id': 'ortopedia',      'label': 'Ortopedia',              'icon': '🦴'},
    {'id': 'cuid_intermedio','label': 'Cuidados Intermédios',   'icon': '🏥'},
    {'id': 'uci',            'label': 'UCI',                    'icon': '❤️'},
    {'id': 'cirurgia',       'label': 'Cirurgia',               'icon': '🔪'},
    {'id': 'maxilo',         'label': 'Maxilo Facial',          'icon': '🦷'},
    {'id': 'bloco_op',       'label': 'Bloco Operatório',       'icon': '🩺'},
    {'id': 'bloco_urgente',  'label': 'Bloco Op. Urgente',      'icon': '🚑'},
    {'id': 'bloco_electiva', 'label': 'Bloco Op. Electiva',     'icon': '📅'},
    {'id': 'consulta_ext',   'label': 'Consulta Externa',       'icon': '📋'},
    {'id': 'nefrologia',     'label': 'Nefrologia',             'icon': '🫘'},
    {'id': 'hosp_dia',       'label': 'Hospital de Dia',        'icon': '☀️'},
    {'id': 'med_homem',      'label': 'Medicina Homem',         'icon': '👨‍⚕️'},
    {'id': 'med_mulher',     'label': 'Medicina Mulher',        'icon': '👩‍⚕️'},
    {'id': 'medicina',       'label': 'Medicina (Auto)',         'icon': '💊'},
    {'id': 'neurocirurgia',  'label': 'Neurocirurgia',          'icon': '🧠'},
    {'id': 'otorrino',       'label': 'Otorrinolaringologia',   'icon': '👂'},
    {'id': 'banco_urg',      'label': 'Banco de Urgência',      'icon': '🚨'},
]

with open(SRC, 'r', encoding='utf-8') as f:
    original = f.read()

# Find the exact SPECIALTIES block to replace
# It starts with "const SPECIALTIES = [" and ends with "];"
specialties_pattern = re.compile(
    r'(const SPECIALTIES = \[)[^\]]*(\];)',
    re.DOTALL
)

for sp in SPECIALTIES:
    sid   = sp['id']
    label = sp['label']
    icon  = sp['icon']

    # Build single-entry SPECIALTIES replacement
    new_array = (
        f"const SPECIALTIES = [\n"
        f"  {{ id:'{sid}', label:'{label}', icon:'{icon}' }},\n"
        f"];"
    )

    modified = specialties_pattern.sub(new_array, original)

    # Update <title>
    modified = modified.replace(
        '<title>Serviço de Procedimentos de Enfermagem</title>',
        f'<title>Procedimentos — {label}</title>'
    )

    # Update splash service span
    modified = modified.replace(
        '<span>Serviço de Procedimentos de Enfermagem</span>',
        f'<span>Serviço de Procedimentos — {label}</span>'
    )

    filename = f'proc_{sid}.html'
    out_path = os.path.join(OUT, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(modified)

    print(f'  ✓  {filename}  ({label})')

print(f'\nGerados {len(SPECIALTIES)} ficheiros em {OUT}/')
