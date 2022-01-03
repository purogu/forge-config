from pathlib import Path
import shutil
import os
import sys
import re

modid = "testmod"
group = "purogu"
class_name = "TestMod"
display_name = "Test Modification"

def replace_strings(file: Path, replacements: dict):
    content = file.read_text(encoding="utf8")
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    file.write_text(content, encoding="utf8")

def get_mod_path(modid):
    return Path("..").joinpath(modid)

def create(modid, group, class_name, display_name):
    print(f"Creating mod {modid} with group={group}, class name={class_name}, display name={display_name}")
    REPLACEMENTS = {
        "MOD_ID": modid,
        "CLASS_NAME": class_name,
        "DISPLAY_NAME": display_name,
        "GROUP": group,
        "PACKAGE_NAME": f"{group}.{modid}",
        "GITHUB_PATH": f"{group}/{modid}",
    }

    TEMPLATE_PATH = Path("template")
    DEST_PATH = get_mod_path(modid)
    MAIN_JAVA_PATH = DEST_PATH.joinpath("src/main/java")
    JAVA_PATH = MAIN_JAVA_PATH.joinpath(REPLACEMENTS["PACKAGE_NAME"].replace(".", "/"))

    IGNORE = ["gradlew", "gradle-wrapper.jar", "gradlew.bat"]

    shutil.copytree(TEMPLATE_PATH, DEST_PATH)
    JAVA_PATH.mkdir(exist_ok=True, parents=True)
    MAIN_CLASS_PATH = JAVA_PATH.joinpath("{}.java".format(REPLACEMENTS["CLASS_NAME"]))
    shutil.move(MAIN_JAVA_PATH.joinpath("Entry.java"), MAIN_CLASS_PATH)
    for dirpath, dirnames, filenames in os.walk(DEST_PATH):
        for filename in filenames:
            if filename not in IGNORE:
                replace_strings(Path(dirpath).joinpath(filename), REPLACEMENTS)

def sub_strings(file: Path, subs: list):
    content = file.read_text(encoding="utf8")
    for regex, sub in subs:
        content = re.sub(regex, sub, content)
    file.write_text(content, encoding="utf8")


def upgrade(modid, version):
    DEST_PATH = get_mod_path(modid)
    VERSION_FIELDS = {
        "1.16": (8, "1.16.5", "1.16.5-36.2.20", 36, 6),
        "1.17": (16, "1.17.1", "1.17.1-37.1.1", 37, 7),
        "1.18": (17, "1.18.1", "1.18.1-39.0.9", 39, 8),
    }
    fields = VERSION_FIELDS[version]

    BUILD_FILE = DEST_PATH.joinpath("build.gradle")
    sub_strings(BUILD_FILE, [
        (r"def minecraftVersion.*", f'def minecraftVersion = "{version}"'),
        (r"java.toolchain.languageVersion.*", f'java.toolchain.languageVersion = JavaLanguageVersion.of({fields[0]})'),
        (r"mappings channel.*", f"mappings channel: 'official', version: '{fields[1]}'"),
        (r"minecraft 'net.*", f"minecraft 'net.minecraftforge:forge:{fields[2]}'")
    ])

    TOML_FILE = DEST_PATH.joinpath("src/main/resources/META-INF/mods.toml")
    sub_strings(TOML_FILE, [
        (r"loaderVersion.*\"", f'loaderVersion="[{fields[3]},)"')
    ])

    PACK_FILE = DEST_PATH.joinpath("src/main/resources/pack.mcmeta")
    sub_strings(PACK_FILE, [
        (r"\"pack_format.*\d", f'"pack_format": {fields[4]}')
    ])

args = sys.argv
argc = len(sys.argv)
if argc < 3:
    raise "Specify the operation and mod id"
op = args[1]
modid = args[2]
if op == "create":
    if argc < 6:
        raise "Specify the group, class name, and display name for the new mod"
    group = args[3]
    class_name = args[4]
    display_name = args[5]
    create(modid, group, class_name, display_name)
elif op == "upgrade":
    if argc < 4:
        raise "Specify the version to upgrade to"
    version = args[3]
    upgrade(modid, version)
else:
    raise "Unrecognized operation"