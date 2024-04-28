# SKIP
SKIP is an abbreviation for "**Sk**ip **I**ntro **P**roject".<br>
Its goal is to provide an easy to use and extend solution to skip intro videos in video games by either renaming or replacing them. 

## Configuration files
SK.I.P uses yaml based configuration files stored in the folder "configuration_files" and supports the following parameters:

Parameter|Description|Example
|--|--|--|
registry|List of lists containing registry information.<br>`[hkey, path, key name]`|[Apsulov: End Of Gods (one list entry)](configuration_files/Apsulov_End_Of_Gods.yaml)<br>[Darkstar One (two list entries)](configuration_files/Darkstar_One.yaml)
folder|List of strings to append to the installation folder got from registry.<br>`movies//eng`|[Apsulov: End Of Gods (one list entry)](configuration_files/Apsulov_End_Of_Gods.yaml)
files|List of files to rename **or** list of lists with files to replace.<br>`abc.mp4` for renaming **or** `[abc.mp4, black_pixel.mp4]` for replacement.|[Apsulov: End Of Gods (renaming)](configuration_files/Apsulov_End_Of_Gods.yaml)<br>[Darkstar One (replacement)](configuration_files/Darkstar_One.yaml)

## Execution
To rename/replace videos, simple execute<br>
`python SK.I.P.py all`<br>
which will apply all configurations or<br>
`python SK.I.P.py <configuration_file.yaml>`<br>
with <configuration_file.yaml> replaced by one of the files available in "configuration_files" to apply one specific configuration only.
<br><br>
The following arguments are supported:
Argument|Valid values|Optional|Description
|--|--|--|--|
--dryRun|`True` or `False`; defaults to `False`.|Yes|Produces output and log entries but does not rename/replace files.
--logLevel|`DEBUG`, `INFO` or `ERROR`; defaults to `ERROR`|Yes|Defines which type of messages will be logged. Higher levels contain lower levels, e.g. using `DEBUG` will also log `INFO` and `ERROR`.
configuration|`all` or `configuration_file.yaml`|No|Defines which configuration file to use, either `all` to apply all available files or `configuration_file.yaml` where `configuration_file.yaml` must be a file available in folder "configuration_files".

## License
Please see [LICENSE](LICENSE).