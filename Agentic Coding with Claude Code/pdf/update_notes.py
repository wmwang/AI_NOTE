import re
import sys

file_path = '/Users/wmwangf/Documents/repo/AI_NOTE/Agentic Coding with Claude Code/pdf/Claude_Code_Presentation_Master_Notes.md'
try:
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract labs from the appendix
    labs = {}
    for i in range(1, 7):
        pattern = rf"## Lab {i}: .*?\n(.*?(?=\n## Lab |\Z))"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            lab_content = match.group(0).strip()
            # Change header to #### Hands-on Lab: ...
            lab_header_match = re.match(rf"## Lab {i}: (.*?) \(Chapter", lab_content)
            if lab_header_match:
                title = lab_header_match.group(1).strip()
                # Replace the first line
                new_lab_content = re.sub(rf"## Lab {i}: .*", f"#### Hands-on Lab: {title}", lab_content)
                labs[i] = "\n" + new_lab_content + "\n"
            else:
                print(f"Failed to match header for Lab {i}")
        else:
            print(f"Failed to extract Lab {i}")

    # Now we need to insert these labs into the specific chapters
    # 1. Lab 2 -> End of Chapter 1
    content = re.sub(r"(\n---\n\n### Chapter 2:)", lambda m: "\n" + labs[2] + m.group(1), content)

    # 2. Lab 1 -> End of Chapter 3
    content = re.sub(r"(\n---\n\n### Chapter 4:)", lambda m: "\n" + labs[1] + m.group(1), content)

    # 3. Lab 3 -> End of Chapter 5
    content = re.sub(r"(\n---\n\n## Part 2:)", lambda m: "\n" + labs[3] + m.group(1), content)

    # 4. Lab 4 -> End of Chapter 11
    content = re.sub(r"(\n---\n\n### Suggested Slide Distribution)", lambda m: "\n" + labs[4] + m.group(1), content)

    # 5. Lab 6 -> End of Chapter 7
    content = re.sub(r"(\n---\n\n### Chapter 8:)", lambda m: "\n" + labs[6] + m.group(1), content)

    # 6. Lab 5 -> End of Chapter 8
    content = re.sub(r"(\n---\n\n### Chapter 9:)", lambda m: "\n" + labs[5] + m.group(1), content)

    with open(file_path, 'w') as f:
        f.write(content)
        
    print("Successfully updated the file.")
except Exception as e:
    print(f"Error: {e}")

