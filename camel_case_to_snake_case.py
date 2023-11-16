import os, fnmatch
import shutil
from distutils.dir_util import copy_tree

src_directory_location = ""
file_patterns = ["*.c", "*.h", "*.cpp", "*.hpp"]

def convert_source_from_camel_case_to_snake_case(src_directory_location):
    for path, dirs, files in os.walk(os.path.abspath(src_directory_location)):
        for i in file_patterns:
            for filename in fnmatch.filter(files, i):
                filepath = os.path.join(path, filename)
                with open(filepath) as f:
                    src_content = f.read()
                    converted_src_content = ""

                    #Find areas to underscore
                    token = ""
                    parse_state = "is_reading_lower_characters"
                    indices_to_underscore = []
                    
                    for i in range(0, len(src_content), 1):
                        character = src_content[i]
                        if (character.isalnum()):
                            token += character
                            
                            if token[0].islower():
                                if (character.isupper() and parse_state == "is_reading_lower_characters"):
                                    indices_to_underscore.append(i)
                                    parse_state = "is_reading_upper_characters"
                                elif (character.islower() and parse_state == "is_reading_upper_characters"):
                                    parse_state = "is_reading_lower_characters"

                                #Lowercase every character that matches the variable/function criteria
                                converted_src_content += lower_character
                            else:
                                converted_src_content += character
                                
                        else:        
                            token = ""
                            parse_state = "is_reading_lower_characters"
                            converted_src_content += character

                    #Insert the underscores
                    indices_to_underscore.reverse()
                    for i in indices_to_underscore:
                        converted_src_content = converted_src_content[:i] + "_" + converted_src_content[i:]
                    
                with open(filepath, "w") as f:
                    f.seek(0, 0)
                    f.write(converted_src_content)

def main():
    src_directory_location = input("Enter the src directory path: ")
    
    print("Backing up '" + src_directory_location + "' ...")
    if (os.path.exists(src_directory_location + "_backup")):
        copy_tree(src_directory_location, src_directory_location + "_alt_backup")
    else:
        copy_tree(src_directory_location, src_directory_location + "_backup")
        
    convert_source_from_camel_case_to_snake_case(src_directory_location)
    
    print("Done.\n")
    input("Press any key to exit.")

if __name__ == "__main__":
    main()
