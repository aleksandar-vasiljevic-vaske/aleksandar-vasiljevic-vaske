#!/bin/env bash

#################################################################
# Promenljive

# Ulazni fajl
input_file="./prilog (1).txt"


# brojac za niz clean_list 
br=0

# brojac za niz good_files
gfbr=0

# Nizovi
###

# Lista svih fajlova ociscena od specijalnih karaktera \r
declare -a clean_list=()

# Lista fajlova cija imena odgovaraju paternu kABCDEFGH.kod
declare -a good_files=()


#################################################################
#################################################################
###Funkcije

# Provera navedenog fajla i sortiranje fajla u dobre ili lose po nazivu
##### file_check

function file_check {
   fine_line="$(echo "$line"|tr -d '\r')"
   clean_list[br]=$fine_line
   touch ${clean_list[br]}
   let br++
}
##### Kraj funkcije file_check



# Funkcija za proveru parnog i neparnog broja, kreiranje direktorijuma i premestanje fajla u odgovarajuci direktorijum
##### par_nepar

function par_nepar {
if [[ "${good_files[i]}" = k??????[2,4,6,8]?.kod ]] ; then
# Promenljiva G uzima vrednost karaktera G
        G="${good_files[i]:7:1}"
        `mkdir -p "${G}0/${good_files[i]:5:1}0"`
        `mv "${good_files[i]}" "${G}0/${good_files[i]:5:1}0"`
   else
        if [[ "${good_files[i]}" = k??????[1,3,5,7,9]?.kod ]] ; then
# Promenljiva G uzima vrednost karaktera G
                G="${good_files[i]:7:1}"
# Promenljiva X dobija vrednost oduzimanjem 1 od parnog broja na mestu G. Ovde se radi konverzija tipova.
				X=$(($((G))-1))
                `mkdir -p "${X}0/${good_files[i]:5:1}0"`
                `mv "${good_files[i]}" "${X}0/${good_files[i]:5:1}0"`
        else
                echo "Naziv fajla ${good_files[i]} ne poklapa se sa obrascem za parne i neparne brojeve i ostace neprocesiran" | tee -a log.txt
        fi
   fi
}
##### Kraj funkcije par_nepar



##################################################################
# Iscitavanje ulaznog fajla, iteriranjem kroz linije fajla do EOF#
##################################################################

 while IFS= read -r line
 do
    file_check
 done < "$input_file"

# Kako poslednja procitana linija ulaznog fajla nije obradjena, moramo naknadno obraditi i nju

    file_check



########################################################################
# Citanje fajlova iz ociscenog niza,provera i izdvajanje validnih imena#
########################################################################

	for filename in "${clean_list[@]}"
	do
	    if [[ "$filename" = k????????.kod ]] ; then
       		good_files[gfbr]=${filename}
		let gfbr++ 
    	else
        	echo "Fajl $filename ne odgovara obrascu kABCDEFGH.kod" | tee -a log.txt
    	fi
	done




######################################################################
# Provera pripadnosti fajla i premestanje u odgovarajuci direktorijum#
######################################################################

# Postavljanje promenljive i koja je brojac na vrednost 0
i=0

for ((	i=0; i<$gfbr; i++ ))
do
	par_nepar	
done

