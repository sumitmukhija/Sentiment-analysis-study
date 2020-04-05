LOGFILE=username-to-info.log
exec < iava-mod.csv || exit 1
read header # read (and ignore) the first line
a="twint --user-full -o file.json --json -u "
while IFS='\n' read name; do
	# $name=$name | xargs
    a="twint --user-full -o user_info.json --json -u $name"
    # b= "${tmp/$'\r'/}name"
    # a="${a}".
    eval $a
    test -n "$ip" && echo ip = "$ip"
done

# awk 'BEGIN{FS=OFS=","}NR>1{for(i=1;i<=NF;i++) print $i}' iava.csv
