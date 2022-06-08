#!/bin/bash

WATCH_EVENTS="modify,delete,create,move"
SYNC_DELAY=0
SYNC_INTERVAL=3600

SYNC_PATH=$1
SYNC_REMOTE=$2

synchronize() {
    set -x
    rsync -av --exclude="*.pyc" --exclude="*/__pycache__" --exclude=".git" ${SYNC_PATH} ${SYNC_REMOTE}
}

# Do initial sync immediately:
synchronize
# Watch for file events and do continuous immediate syncing
# and regular interval syncing:
while [[ true ]] ; do
	inotifywait --recursive --timeout ${SYNC_INTERVAL} -e ${WATCH_EVENTS} \
		        --exclude='\.git|\.#|\.pyc' ${SYNC_PATH} 2>/dev/null
	if [ $? -eq 0 ]; then
	    # File change detected, sync the files after waiting a few seconds:
	    sleep ${SYNC_DELAY} && synchronize && \
		    echo "Synchronized new file changes"
	elif [ $? -eq 1 ]; then
	    # inotify error occured
	    echo "inotifywait error exit code 1"
        sleep 10
	elif [ $? -eq 2 ]; then
	    # Do the sync now even though no changes were detected:
	    synchronize
	fi
done
