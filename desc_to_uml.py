import subprocess
from pathlib import Path
from typing import List, Any

from desc import ClassDesc


def desc_to_uml(data: List[Any], plantuml_path: Path) -> None:
    with plantuml_path.open('w') as uml:
        uml.write("```mermaid\n\n")
        uml.write("classDiagram\n\n")
        uml.write(class_defs(data))
        # uml.write("hide empty members\n\n")

        uml.write(inheritance(data))
        uml.write(docstrings(data))
        uml.write("\n```")
    create_plantuml(plantuml_path)


def class_defs(data: List[ClassDesc]) -> str:
    string = ""
    for class_def in data:
        string += f"class {class_def.name}" + "{\n"
        if len(funcs_in_class(class_def)) > 0:
            string += vars_in_class(class_def)
            string += funcs_in_class(class_def)
            string += "}\n\n"
        else:
            string += "<<abstract>>\n"
            string += "}\n\n"

    return string


def vars_in_class(class_def: ClassDesc) -> str:
    string = ""
    for var in class_def.vars:
        string += f"    {var}\n"
    return string


def funcs_in_class(class_def: ClassDesc) -> str:
    string = ""
    for func in class_def.functions:
        if len(func.name) > 1:
            string += f"    {func.name}("
            first = True
            for arg in func.args:
                if first:
                    first = False
                else:
                    string += ", "
                string += f"{arg}"
            string += ")\n"
        else:
            string += ")*\n"
    return string


def inheritance(data: List[ClassDesc]) -> str:
    string = ""
    for class_def in data:
        for base in class_def.bases:
            string += f"{base} <|-- {class_def.name}\n"

    return string


def dependencies(data: List[ClassDesc]) -> str:
    string = ""
    for class_def in data:
        for dep in class_def.dependencies:
            string += f"{dep} <-- {class_def.name}\n"
    return string


def docstrings(data: List[ClassDesc]) -> str:
    string = "\n"
    for class_def in data:
        if not class_def.docstring:
            continue
        string += f"note top of {class_def.name}\n"
        string += f"{class_def.docstring}\n"
        string += f"end note\n\n"
    return string


def create_plantuml(plantuml_path: Path) -> None:
    print(f"Creating mermaid diagram")
    subprocess.run(['java', '-jar', 'plantuml.jar', '-duration', str(plantuml_path)])
    print(f"Mermaid diagram created: {plantuml_path}")
