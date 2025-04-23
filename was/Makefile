_TMPDIR=$(TMPDIR)

open: setup
	nix-shell --run 'TMPDIR=${_TMPDIR} SHELL=/bin/zsh pycharm .'

# 개발용 프로젝트 설정
setup: venv
	nix-shell --run 'venv/bin/pip install pip==24.3.1'
	nix-shell --run 'venv/bin/pip install -e .'

# 파이선 Virtual Environment
venv:
	nix-shell --run 'python3.12 -m venv venv'

# mypy 타입 체크
mypy-check:
# daemon mypy 로 ex, bin 아래 소스들 체크
	venv/bin/dmypy run -- was bin

watch:
# watchmedo 는 최초 1회 실행이 없어서 그냥 먼저 실행한다.
# 실행 과정에서 오류가 발생해도 그냥 무시한다. 어차피 계속 실행되어야 한다.
	-$(MAKE) mypy-check
	venv/bin/watchmedo shell-command --patterns="*.py;*.ini;*.tsx" --recursive --ignore-directories --drop --command='echo ""; make api url mypy-check ' .

