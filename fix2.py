path = r'c:\Users\Mauricio\Desktop\ghost_station\core\templates\core\evp_console.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Fix: {% endif\n + whitespace + %} => {% endif %}
    if '{% endif' in line and '%}' not in line:
        # Check if next line contains just %}
        if i + 1 < len(lines) and lines[i+1].strip() == '%}':
            fixed = line.rstrip().replace('{% endif', '{% endif %}') + '\n'
            out.append(fixed)
            i += 2  # skip the dangling %} line
            continue
    
    # Fix: {% endfor\n + whitespace + %} => same thing
    if '{% endfor' in line and line.strip() == '{%' or ('{% endfor' in line and line.count('%}') == 0):
        if i + 1 < len(lines) and lines[i+1].strip() == '%}':
            fixed = line.rstrip().replace('{% endfor', '{% endfor %}') + '\n'
            out.append(fixed)
            i += 2
            continue
    
    out.append(line)
    i += 1

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(out)

# Verify fix
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

problems = []
for idx, ln in enumerate(content.splitlines(), 1):
    stripped = ln.strip()
    if stripped == '%}':
        problems.append(f"Line {idx}: dangling '%}}' found")
    if '{% endif' in ln and '%}' not in ln:
        problems.append(f"Line {idx}: broken endif: {ln.strip()}")
    if '{% endfor' in ln and '%}' not in ln:
        problems.append(f"Line {idx}: broken endfor: {ln.strip()}")

if problems:
    print("REMAINING ISSUES:")
    for p in problems:
        print(p)
else:
    print("ALL TEMPLATE TAGS FIXED - no dangling tags found!")
