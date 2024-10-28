### Sorter for JSON files according to rules from Audit Task

Before running, know you can run this script from any where using base_path as {BASE_DIRECTORY}.

<em>For running script</em>

```python
python -m main {BASE_DIRECTORY}
```

This means that you can run this script on any path you want.

But before running, you need to create a ```modified.json``` file in the specific folder of the audit task. 
Example:
```
Can be created in the folder of specific atomic. In my case, it is <product_name>__definition_workflow_02AK3KCXMEC8A0EKa1UdtQDq6d3FCiKUfzI/
```

Where folder is the name of atomic. Under the original version from the repo, we create a modified.json file, where you put your changes.

After that you run the script, for example, my script is in:
> /Users/\<username>\/<path_to_folder>/accessSortJSON

Need to put the path to your folder in variable ```BASE_DIRECTORY```.

```python
python -m main  ~/<path_to_folder>  --save
```

This script works with specific folders of the name of atomic. That is why in <b>constants.py</b> you need to put the first part of the name per-product. The list of products I will live on comment in <b>constants.py</b>

<em>Example</em>
```python
# Base directory to start searching for specific products directories
BASE_DIRECTORY = '<base directory>'

# Pattern to match original files
ORIGINAL_FILE_PATTERN = '<original file name pattern>'

# Pattern to match directories starting with
DIRECTORY_PATTERN = '<product name>'

# Pattern to match modified files
MODIFIED_FILE_PATTERN = '<modified file name>'

# Pattern to match corrected files
CORRECTED_FILE_PATTERN = '<corrected file name>'
```

### v1.0
<b>Added a list of flags to make a work more easy and fresh.</b>
<em>List of flags you can see if you input</em>

```python
python -m main -help
```

<b>At now you do not need to create modified.json file and remove corrected.json files by your own. Just to need to run the script.</b>

### Few changes what is made fixed:

:white_check_mark:
At now this script do not put descriptions in *output variables*</br>
:white_check_mark:
You can choose how to save changes: in original version or in corrected version </br>
:white_check_mark: 
Automated script for creating modified.json files according to product, which you provided </br>
:white_check_mark: 
Automated for removing after all changes and modification, corrected.json files according to product, which you provided </br>
:white_check_mark: Do not need to switch between different script, just use flag according to your needs </br>
:white_check_mark:Change variables_string_format for: *datatype.string*, *datatype.secure_string* it put "text" or if you choose <b>json</b>, it not changed and leave as it is


v1.2
1) :white_check_mark:
Added an ability in automated way to change <em>"title"</em>, <em>"name"</em> and <em>"display_name"</em> in all files after you export an atomic and put into <i>modified.json</i> file.
2) :white_check_mark:
At now you can customize your logger and see appropriate information in console, also remove print() from every step of changing and creating.
3) :white_check_mark:
Few fixes in conditional branches, before we have only *text* and *json*, at now we have *text*, *json* and *xml*
4) :white_check_mark:
Removed not needed code in *sortJson.py* and *buildStructure.py* at the end, because all things were done in *main.py*

## Enjoy :fire:
