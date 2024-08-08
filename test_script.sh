#!/bin/bash

declare -A size

get_data() {
	list=$(ls -A)
	for file in $list; do
		size[$file]=$(du -hs $file 2>/dev/null | cut -f1)
	done
	echo $size
}

get_data

printf "%-27s %s\n" "Name" "Size"
printf "%s\n" "------------------------------------"



for key in "${!size[@]}"; do
	value=${size[$key]}
	printf "%-27s %s\n" "$key" "$value"
done | sort -k2 -rh | column -t > temp.txt

x=1
n=10
l=$(cat temp.txt | wc -l)
cat temp.txt | sed -n "${x},${n}p;${n}q"
printf "%s\n" "------------------------------------"
PS3="Выберите действие: "
#30
select option in "Previos" "Next" "Quit"
do
	case $option in
		"Previos")
			if [[ $x -gt 10 ]]; then
				x=$(($x-10))
				n=$(($x+9))
				printf "%-27s %s\n" "Name" "Size"
				printf "%s\n" "------------------------------------"
				cat temp.txt | sed -n "${x},${n}p;${n}q"
				printf "%s\n" "------------------------------------"
	else
				if [[ $x -gt 1 ]]; then
					x=1
					n=10
					printf "%-27s %s\n" "Name" "Size"
					printf "%s\n" "------------------------------------"
					cat temp.txt | sed -n "${x},${n}p;${n}q"
					printf "%s\n" "------------------------------------"
				else
					echo "This is the first line, there is no previous line"
				fi
			fi
			;;
		"Next")
			k=$(($l-10))
			if [[ $n -le $k ]]; then
				x=$(($x+10))
				n=$(($x+9))
				printf "%-27s %s\n" "Name" "Size"
				printf "%s\n" "------------------------------------"
				cat temp.txt | sed -n "${x},${n}p;${n}q"
				printf "%s\n" "------------------------------------"
			else
				if [[ $n -gt $l ]]; then
					n=$l
					x=$(($n-9))
					printf "%-27s %s\n" "Name" "Size"
					printf "%s\n" "------------------------------------"
					cat temp.txt | sed -n "${x},${n}p;${n}q"
					printf "%s\n" "------------------------------------"
			else
					echo "That's the last line, there's no next line"
				fi
			fi
			;;
		"Quit")
			break
			;;
		*)
			echo "Incorrect choice"
			;;
	esac
done

rm ./temp.txt
