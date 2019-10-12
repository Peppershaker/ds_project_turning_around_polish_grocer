#!bin/bash

# Author: Victor Xu
#
# This script fixes a bug in Kaggle where notebooks using custom Python kernel
# version does not run after being uploaded. This is because in order to commit
# changes on Kaggle you must have notebook kernelspec "name": "python3". Any
# other value will cause the commit to fail.
#
# The script will replace all kernel name references in the notebooks to 
# the generic Python 3 one used by all Kaggle cloud notebooks.

CUSTOM_KERNEL_NAME="python3.7"

rm -r ./kaggle_notebooks
mkdir kaggle_notebooks

# allows filename patterns which match no files to expand to a null 
# string, rather than themselves. In other words don't execute the for loop
# if no file matching given pattern is found
shopt -s nullglob

for f in *.ipynb; do
  sed "s/$CUSTOM_KERNEL_NAME/python3/" "$f" > "kaggle_notebooks/$f"
  echo "Fixed $f"
done
