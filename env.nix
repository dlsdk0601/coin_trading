let
  pkgs = import (fetchTarball {
    # 24.11 @ 2024.12.10 https://github.com/NixOS/nixpkgs/tree/e2605d0744c2417b09f8bf850dfca42fcf537d34
    url = "https://github.com/NixOS/nixpkgs/tarball/e2605d0744c2417b09f8bf850dfca42fcf537d34";
    sha256 = "1fsfkdjlqknzxi9jc38a0k0103rlxnjj59xg1s9a5bqb3scaxh9m";
  }) { };
was = with pkgs; [ python312 ];

packages = was;
in
{
  shellHook ? "",
}:
(if pkgs.stdenv.isDarwin then pkgs.mkShellNoCC else pkgs.mkShell) {
  name = "coin-trading";
  LD_LIBRARY_PATH = pkgs.lib.optionalDrvAttr (!pkgs.stdenv.isDarwin) [
    "${pkgs.stdenv.cc.cc.lib}/lib"
  ];

  inherit packages;

  shellHook = ''
    source ${builtins.toString ./.env.sh}
    ${shellHook}
  '';
}

