"""
Fix evp_console.html: joins all broken Django template tags that span multiple lines.
A broken tag looks like:  {% some_tag\n   %} or {% endif\n   %}
"""
import re

path = r'c:\Users\Mauricio\Desktop\ghost_station\core\templates\core\evp_console.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Join any {%...tag... that doesn't have a closing %} on the same line
# Pattern: {% ... \n ... %} (where the %} is on a new line with only whitespace before it)
fixed = re.sub(r'(\{%[^%]*?)\n\s*(%\})', r'\1 \2', content)

# Also fix {{ ... \n ... }} 
fixed = re.sub(r'(\{\{[^}]*?)\n\s*(\}\})', r'\1 \2', fixed)

with open(path, 'w', encoding='utf-8') as f:
    f.write(fixed)

# Verify
problems = []
for idx, line in enumerate(fixed.splitlines(), 1):
    stripped = line.strip()
    if stripped == '%}':
        problems.append(f"  Line {idx}: dangling '%}}'")
    if stripped == '}}':
        problems.append(f"  Line {idx}: dangling '}}}}'")
    if re.match(r'^\s*\{%\s*$', line):
        problems.append(f"  Line {idx}: dangling '{{% '")

if problems:
    print("REMAINING ISSUES:")
    for p in problems: print(p)
else:
    print("SUCCESS: No broken template tags found!")
