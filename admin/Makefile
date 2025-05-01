_TMPDIR=$(TMPDIR)

open: setup
	nix-shell --run 'TMPDIR=${_TMPDIR} SHELL=/bin/zsh webstorm .'

setup:
	nix-shell --run 'bun i'

run:
	nix-shell --run 'bun run dev'

watch:
	nix-shell --run 'bun --watch=src/app --extension=tsx bin/generateUrl.ts'
