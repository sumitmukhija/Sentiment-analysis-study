LOGFILE=username-to-tweets.log
exec < data/filtered_vets_username.csv || exit 1
# read header
while IFS='\n' read name; do
    a="twint -o data/$name.csv --csv -u $name"
    eval $a
    test -n "$ip" && echo ip = "$ip"
done
