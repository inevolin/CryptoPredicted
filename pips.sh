#!/usr/bin/env bash

# # when new dependencies added, add the name(s) here
source ./ENV/bin/activate
pip3 install --upgrade pip
cat piplibs.txt | xargs -n 1 pip3 install

# extra requirements
python << END
import nltk
nltk.download('punkt')
END

deactivate