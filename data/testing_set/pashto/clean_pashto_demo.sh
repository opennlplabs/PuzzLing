# clean all the whitespaces (\t, \r, \n, \v etc) from the beginning of lines, and save it.
sed -ie 's/^[[:space:]]*//g' pashto_demo.txt


