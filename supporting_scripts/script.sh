LOGFILE=test.log
exec < new_sample_file.csv || exit 1
read header 
a="twint --user-full -o file.json --json -u "
while IFS='\n' read name; do
    a="twint --user-full -o file.json --json -u $name"
    eval $a
    test -n "$ip" && echo ip = "$ip"
done

