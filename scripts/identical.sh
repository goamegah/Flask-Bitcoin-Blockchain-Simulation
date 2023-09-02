#!/bin/bash
#store the number of files from the command line argument
number_files=$1
for ((i=0; i<number_files; i++))
do
  for ((j=i+1; j<number_files; j++))
  do
    # Store the names of the two files to be compared
    file1="../noeud${i}_blockchain.json"
    file2="../noeud${j}_blockchain.json"
    # Store the difference between the two files
    diff_command=$(diff "$file1" "$file2")
    diff_exit_status=$?
    $diff_command > /dev/null 2>&1 # This is used to suppress any error messages and redirect to /dev/null
    if [ $diff_exit_status -eq 1 ]
    then
      echo "The contents of $file1 and $file2 are different."
      echo $diff_files
      exit 1
    fi
    if [ $diff_exit_status -eq 2 ]
        then
          echo "A problem occur with" $file1 "and" $file2
          exit 2
    fi
  done
done

echo "The contents of all the files are identical. Removing all blockchain of all nodes .."
#remove all the files
rm -r ../noeud*_blockchain.json
exit 0



