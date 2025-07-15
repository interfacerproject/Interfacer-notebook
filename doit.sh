#!/bin/bash

in_files="if_lib.py if_dpp.py"
python_wrapper=wrapper.py

out_file=if_wrapped # can be specified on command line
create_file=n

while getopts "co:s" options
do
  case "${options}" in
    c)
      create_file=y
      ;;
    o)
      out_file=${OPTARG}
      ;;
    s)
      start_webserver=y
      ;;
    :)
      echo "Error: -${OPTARG} requires an argument."
      exit -1
      ;;
    *)
      exit -1
      ;;
  esac
done

if [ "${create_file}" == "y" ]
then
  python ${python_wrapper} -i ${in_files} -o ${out_file}.py
else
  ls -l ${out_file}.py > /dev/null
fi

if [ "${?}" == "0" -a "${start_webserver} " == "y " ]
then
    uvicorn ${out_file}:app --host 0.0.0.0 --port 8000
fi

