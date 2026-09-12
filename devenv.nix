{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{

  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.moon
    pkgs.opam
    pkgs.gmp
    pkgs.dune
    pkgs.pkg-config
    pkgs.sqlx-cli
  ];

  # https://devenv.sh/languages/
  languages = {
    haskell.enable = true;
    rust.clangLinker.enable = true;
    ocaml = {
      enable = true;
    };
    rust.enable = true;
    javascript = {
      enable = true;
      pnpm.enable = true;
    };
  };
  enterShell = ''
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    PURPLE='\033[0;35m'
    CYAN='\033[0;36m'
    NC='\033[0m' # No Color

    echo -e "''${CYAN}moon''${NC}  $(moon --version 2>/dev/null || echo 'not found')"
    echo -e "''${GREEN}git''${NC}   $(git --version)"
    echo -e "''${YELLOW}cargo''${NC} $(cargo --version)"
    echo -e "''${BLUE}node''${NC}  $(node --version)"

    echo -e "''${YELLOW}opam''${NC}  $(opam --version)"
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
