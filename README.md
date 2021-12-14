git_diff_lines
==============

Get a list of changed lines in git diff.

It does this by running `git diff` in the respective directory 
and parses the output. It converts the output into a list of 
tuples in the form `(filename, line_number)` for every line in
every file.
