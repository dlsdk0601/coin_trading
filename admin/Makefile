_TMPDIR=$(TMPDIR)

open: setup
	nix-shell --run 'TMPDIR=${_TMPDIR} SHELL=/bin/zsh webstorm .'

setup:
	nix-shell --run 'bun i'

run:
	nix-shell --run 'bun run dev'

watch:
	nix-shell --run 'bun --watch bin/generateUrl.ts --watch-dir src/app'
