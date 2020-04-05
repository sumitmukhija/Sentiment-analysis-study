LOGFILE=username-to-info.log
exec < iava-mod.csv || exit 1
read header
while IFS='\n' read name; do
    a="twint --user-full -o user_info.json --json -u $name"
    eval $a
    test -n "$ip" && echo ip = "$ip"
done
