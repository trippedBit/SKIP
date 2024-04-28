import argparse
import logging
import os
import shutil
import subprocess
import sys
import winreg
import yaml


def processConfiguration(configurationFile: str,
                         dryRun: bool = False) -> None:
    """
    Processes the given configuration file.
    :param configurationFile: Configuration file to use.
    :dryRun: True: Call follow-up functions during dryRun, False = Do NOT call follow-up functions during dryRun
    :return: None
    """
    print("Processing {}".format(configurationFile))
    logger.info("Processing {}".format(configurationFile))

    with open("configuration_files/" + configurationFile,
              "r") as file:
        configuration = yaml.safe_load(file)

    installationFolder = "not set"
    if sys.platform == "win32":
        for entry in configuration["registry"]:
            installationFolder = getFolderFromRegistry(entry[0],
                                                       entry[1],
                                                       entry[2])
            if installationFolder != "not set":
                break
    elif sys.platform == "linux":
        for entry in configuration["find"]:
            result = subprocess.run("find", "/", "-name", entry, "-type", "d" "2>/dev/null",
                                    stdout=subprocess.PIPE)
            installationFolder = result.stdout
            if installationFolder != "" and installationFolder != "not set":
                break
    else:
        print("Error: Your platform is not supported.")
        logger.error("Unsupported platform: {}".format(sys.platform))

    logger.debug("Installation folder: {}".format(installationFolder))
    if installationFolder == "not set":
        print("Installation folder not found!")
        logger.error("Installation folder not found!")
        return

    for folder in configuration["folder"]:
        for file in configuration["files"]:
            if isinstance(file, list):
                success: bool = renameFile(installationFolder=installationFolder,
                                           folder=folder,
                                           file=file[0],
                                           dryRun=dryRun)
                if success or dryRun:
                    copyReplacement(installationFolder=installationFolder,
                                    folder=folder,
                                    file=file[0],
                                    replacement=file[1],
                                    dryRun=dryRun)
                else:
                    print("ERROR: Renaming failed, skipped replacement.")
                    logger.error("Renaming failed, skipped replacement.")
            else:
                renameFile(installationFolder=installationFolder,
                           folder=folder,
                           file=file,
                           dryRun=dryRun)


def getFolderFromRegistry(hkeyType: str,
                          path: str,
                          name: str) -> str:
    """
    Retrieves the installation folder from the registry.
    :param hkeyType: HKEY containing the path.
    :param path: Path to the key inside HKEY.
    :param name: Key name to retrieve data from.
    :return: Retrieved data as string.
    """
    installedTo = "not set"
    try:
        hkey = winreg.ConnectRegistry(None,
                                      registryKeyMapping[hkeyType])
        key = winreg.OpenKey(hkey,
                             path,
                             0,
                             winreg.KEY_READ)

        for i in range(999):
            valueName, valueData, dataType = winreg.EnumValue(key,
                                                              i)
            if valueName == name:
                installedTo = valueData
                break
        winreg.CloseKey(key)
        winreg.CloseKey(hkey)

        logger.debug("Installed to: {}".format(installedTo))
        return installedTo
    except OSError:
        logger.exception("OS error")
        return installedTo


def renameFile(installationFolder: str,
               folder: str,
               file: str,
               dryRun: bool = False) -> bool:
    """
    Renames a file.
    :param installationFolder: Folder as retrieved in previous steps.
    :param folder: Subfolder to append to the installation folder.
    :param file: File to rename.
    :dryRun: True: Do NOT rename files, False = DO rename files
    :return: True if successfull, False if not successfull.
    """
    if os.path.exists(installationFolder + "/" + folder + "/" + file):
        print("Renaming {}".format(installationFolder + "/" + folder + "/" + file))
        logger.info("Renaming {}".format(installationFolder + "/" + folder + "/" + file))
        if dryRun is False:
            os.rename(installationFolder + "/" + folder + "/" + file,
                      installationFolder + "/" + folder + "/" + file + ".skip")
            if os.path.exists(installationFolder + "/" + folder + "/" + file) is False and os.path.exists(installationFolder + "/" + folder + "/" + file + ".skip"):
                print("Renaming file successfull.")
                logger.info("Renaming file successfull.")

                return True
            else:
                print("Renaming file NOT successfull")
                logger.error("Renaming file successfull.")

    return False


def copyReplacement(installationFolder: str,
                    folder: str,
                    file: str,
                    replacement: str,
                    dryRun: bool = False) -> bool:
    """
    Copies the replacement into the given folder.
    :param installationFolder: Folder as retrieved in previous steps.
    :param folder: Subfolder to append to the installation folder.
    :param file: File to replace.
    :param replacement: Video file to use as replacement.
    :dryRun: True: Do NOT replace files, False = DO replace files
    :return: True if successfull, False if not successfull.
    """
    if not os.path.exists(installationFolder + "/" + folder + "/" + file + ".skip"):
        print("ERROR: {} does not exist.".format(installationFolder + "/" + folder + "/" + file + ".skip"))
        logger.error("{} does not exist.".format(installationFolder + "/" + folder + "/" + file + ".skip"))
        return False

    if not os.path.exists("replacement_videos/" + replacement):
        print("ERROR: {} does not exist.".format("replacement_videos/" + replacement))
        logger.error("{} does not exist.".format("replacement_videos/" + replacement))
        return False

    print("Replacing {} with {}".format(installationFolder + "/" + folder + "/" + file, "replacement_videos/" + replacement))
    logger.info("Replacing {} with {}".format(installationFolder + "/" + folder + "/" + file, "replacement_videos/" + replacement))
    if dryRun is False:
        shutil.copy("replacement_videos/" + replacement,
                    installationFolder + "/" + folder + "/" + file)
        if os.path.exists(installationFolder + "/" + folder + "/" + file + ".skip") and os.path.exists(installationFolder + "/" + folder + "/" + file):
            print("Replacing file successfull.")
            logger.info("Replacing file successfull.")
            return True
        else:
            print("Replacing file NOT successfull")
            logger.error("Replacing file successfull.")
            return False
    else:
        return True


logger = logging.getLogger(__name__)

registryKeyMapping = {"HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
                      "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
                      "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
                      "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA,
                      "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
                      "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
                      "HKEY_USERS": winreg.HKEY_USERS}


def main():
    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("configuration",
                                help="Configuration to use OR 'all'")
    argumentParser.add_argument("--dryRun",
                                action="store_true",
                                default=False,
                                help="Do not rename files, just show what would happen.")
    argumentParser.add_argument("--logLevel",
                                choices=["DEBUG",
                                         "INFO",
                                         "ERROR"],
                                default="INFO")
    arguments = argumentParser.parse_args()

    if os.path.exists("SKIP.log"):
        os.remove("SKIP.log")

    logging.basicConfig(filename="SKIP.log",
                        level=logging.getLevelName(arguments.logLevel))

    logger.debug("Arguments: {}".format(arguments))

    if arguments.dryRun:
        print("Option --dryRun is enabled, no files will be renamed/replaced.")

    logger.info("Selected configuration: {}".format(arguments.configuration))
    if arguments.configuration == "all":
        for file in os.listdir("configuration_files"):
            if os.path.splitext(file)[1] == ".yaml":
                processConfiguration(configurationFile=file,
                                     dryRun=arguments.dryRun)
    else:
        processConfiguration(arguments.configuration)

    logging.shutdown()


if __name__ == "__main__":
    main()
