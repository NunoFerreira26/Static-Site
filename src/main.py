import os
import shutil
import sys
from split_nodes_delimiter import markdown_to_html_node,extract_title
from htmlnode import HTMLnode

def copy_files(source:str,destination:str) -> None:
    #Ensure target destination directory exists
    if not os.path.exists(destination):
        os.mkdir(destination)

    #Iterate through all times in the current source foulder
    for item in os.listdir(source):
        source_path = os.path.join(source,item)
        destination_path = os.path.join(destination,item)

        print(f"Copying: {source_path} to {destination_path}") #Logging

        if os.path.isfile(source_path):
            shutil.copy(source_path,destination_path)
        else:
            copy_files(source_path,destination_path)

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str="/") -> None:
    #Print generating message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    #Read markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        text_source = f.read()

    #Read template file
    with open(template_path, "r", encoding="utf-8") as f:
        text_template = f.read()

    #Convert markdown to HTML string
    html_source = markdown_to_html_node(text_source).to_html()

    #Extract page title
    page_title = extract_title(text_source)

    #Replace template placeholders
    full_template = text_template.replace("{{ Title }}", page_title)
    full_template = full_template.replace("{{ Content }}", html_source)
    #Update root-relative links to respect basepath
    full_template = full_template.replace('href="/', f'href="{basepath}')
    full_template = full_template.replace('src="/', f'src="{basepath}')

    #Ensure target directory exists and write full HTML file
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_template)

def generate_pages_recursively(source_directory:str,template:str,destination_directory:str,basepath:str="/") -> None:
    for item in os.listdir(source_directory):
        source_path = os.path.join(source_directory,item)
        if os.path.isfile(source_path):
            #Swap .md extension to .html
            if item.endswith(".md"):
                html_file = item[:-3] + ".html"
                destination_path = os.path.join(destination_directory,html_file)
                #Logging
                print(f"Generating page from {source_path} to {destination_path} using {template}")
                #Open and read the markdown file at source
                with open(source_path,"r",encoding="utf-8") as f:
                    text_source = f.read()
                page_title = extract_title(text_source) #Extract the title
                HTML_source = markdown_to_html_node(text_source).to_html() #Generate the Body
                #Open and read the mardown file at template 
                with open(template,"r",encoding="utf-8") as f:
                    text_template = f.read()
                full_template = text_template.replace("{{ Title }}", page_title)
                full_template = full_template.replace("{{ Content }}", HTML_source)
                #Update root-relative links to respect basepath
                full_template = full_template.replace('href="/', f'href="{basepath}')
                full_template = full_template.replace('src="/', f'src="{basepath}') 
                #Extract target directory path
                dest_dir = os.path.dirname(destination_path) 
                #Creates a directory tree if it doesn't exists
                if dest_dir != "": 
                    os.makedirs(dest_dir,exist_ok=True)
                #Open and write the destination file
                with open(destination_path,"w",encoding="utf-8") as f:
                    f.write(full_template)
        else:
            sub_destination_directory = os.path.join(destination_directory,item)
            generate_pages_recursively(source_path,template,sub_destination_directory,basepath)

def main():
     #If an argument is not given, default to / - For local testing
    basepath = "/"
    #Grab the first CLI argument to the program - For production via build.sh
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
   
    souce = STATIC_DIR
    destination = DOCS_DIR

    #Clear the destination directory first
    if os.path.exists(destination):
        shutil.rmtree(destination,ignore_errors=True) #Remove/delete all the contents of the destination directory

    #Re-create empty destination directory
    os.mkdir(destination)

    #Run recursive copy
    copy_files(souce,destination)

    generate_pages_recursively(CONTENT_DIR,TEMPLATE_PATH,DOCS_DIR,basepath)

SRC_DIR = os.path.dirname(os.path.abspath(__file__)) #Path to src
PROJECT_ROOT = os.path.dirname(SRC_DIR) #Path to the root
#Dynamic absolute paths
STATIC_DIR = os.path.join(PROJECT_ROOT,"static")
DOCS_DIR = os.path.join(PROJECT_ROOT,"docs")
CONTENT_DIR = os.path.join(PROJECT_ROOT,"content")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "template.html")

if __name__ == "__main__":
    main()