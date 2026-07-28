import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {'venv', '.git', '__pycache__', 'staticfiles', 'node_modules'}
total = 0

for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                contenido = fh.read()
            n = contenido.count('.odontólogo')
            if n:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(contenido.replace('.odontólogo', '.odontologo'))
                total += n
                print(f'{os.path.relpath(path, ROOT)}: {n} reemplazo(s)')

print(f'\nTotal: {total} reemplazo(s)')
