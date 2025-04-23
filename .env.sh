#!/usr/bin/env bash

# remove xcrun from PATH if it's in there,
# flutter and '/usr/bin/arch -arm64e xcrun' are not compatible with nix version of xcrun
XCRUN=$(which xcrun)

if [[ -n "$XCRUN" ]]; then
	if [[ $XCRUN = /nix* ]]; then
		XCRUN_BIN=$(dirname $XCRUN)
		CLEAN_PATH=$(echo $PATH | sed -r "s|$XCRUN_BIN:?||g")
		export PATH=$CLEAN_PATH
		
		# unset env vars that are set by nix xcrun
		unset SDKROOT
		unset DEVELOPER_DIR
	fi
fi
