# clean all the whitespaces (\t, \r, \n, \v etc) from the beginning of lines, and save it.
sed -ie 's/^[[:space:]]*//g' pashto_demo.txt
# we only need the odd or even lines
awk 'NR%2==0' pashto_demo.txt > pashto_only.txt
# we only need the  lines
awk 'NR%2==1' pashto_demo.txt > english_only.txt
# clean all the whitespaces (\t, \r, \n, \v etc) from the beginning of lines, and save it.
sed -ie 's/^[[:space:]]*//g' pashto_only.txt
# remove all the special characters in the pashto_only.txt
sed -ie 's|[",]||g' pashto_only.txt