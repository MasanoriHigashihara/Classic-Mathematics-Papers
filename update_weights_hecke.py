import re
import sys

def update_hugo_toml():
    toml_path = r"c:\Users\natsu\.gemini\antigravity\scratch\notebooklm-classics\hugo.toml"
    with open(toml_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split('[[menu.before]]')
    
    # blocks[0] is everything before the first [[menu.before]]
    # blocks[1] is name = "新着" ...
    
    new_block = """
name = "代数的整数論講義 第II章 §6"
url = "/papers/hecke/algebraic-numbers/slides/chapter2-6/"
parent = "新着"
weight = 2
"""
    
    if 'name = "新着"' in blocks[1]:
        # insert as blocks[2]
        blocks.insert(2, new_block)
    else:
        print("Could not find 新着 block")
        sys.exit(1)
        
    # Now fix numerical weights sequentially starting from block 1.
    current_weight = 1
    for i in range(1, len(blocks)):
        block = blocks[i]
        # Replace weight = X with weight = current_weight
        # Every block should have exactly one weight = X
        if 'weight =' in block:
            blocks[i] = re.sub(r'weight\s*=\s*\d+', f'weight = {current_weight}', block)
            current_weight += 1
            
    final_content = blocks[0] + '[[menu.before]]' + '[[menu.before]]'.join(blocks[1:])
    
    with open(toml_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"Done. Updated weights up to {current_weight-1}")

if __name__ == "__main__":
    update_hugo_toml()
