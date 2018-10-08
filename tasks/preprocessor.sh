#!/usr/bin/env bash
while [[ "$#" > 0 ]]; do case $1 in
  -i|--input-dir) INPUT_DIR="$2"; shift 2;;
  -o|--output-dir) OUTPUT_DIR="$2"; shift 2;;
  -t|--date_time) DATE_TIME=$2; shift 2;;
  -s|--sleep) SLEEP=$2; shift 2;;
  *) echo "Unknown parameter passed: $1"; exit 2;;
esac; done

PREPROCESSED_DIR=${OUTPUT_DIR}/${DATE_TIME//-/\/}
mkdir -p ${PREPROCESSED_DIR}
sleep ${SLEEP}
cp ${INPUT_DIR}/* ${PREPROCESSED_DIR}
touch ${PREPROCESSED_DIR}/_SUCCESS
