{
  description = "Create Nix development environment";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";

    # 3.12.1 release
    python-nixpkgs.url = "github:NixOS/nixpkgs/fd04bea4cbf76f86f244b9e2549fca066db8ddff";

    # 20.6.1 release
    nodejs-nixpkgs.url = "github:NixOS/nixpkgs/78058d810644f5ed276804ce7ea9e82d92bee293";

    # 0.17.1 release
    restic-nixpkgs.url = "github:NixOS/nixpkgs/d4f247e89f6e10120f911e2e2d2254a050d0f732";

    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      flake = false;
    };
  };

  outputs = {
    self,
    flake-utils,
    python-nixpkgs,
    nodejs-nixpkgs,
    restic-nixpkgs,
    pyproject-nix,
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = python-nixpkgs.legacyPackages.${system};
      python = pkgs.python312;
      nodejs = nodejs-nixpkgs.legacyPackages.${system}.nodejs_20;
      restic = restic-nixpkgs.legacyPackages.${system}.restic;
      pyproject = import (pyproject-nix + "/lib") {inherit (pkgs) lib;};
      project = pyproject.project.loadRequirementsTxt {
        requirements = ./dev_requirements.txt;
      };
      pythonEnv = pkgs.python3.withPackages (pyproject.renderers.withPackages {
        inherit project python;
      });
    in {
      devShells.default = pkgs.mkShell {
        packages = [
          pythonEnv
          nodejs
          restic
        ];
        shellHook = ''
          echo "node" "$(node --version)"
          echo "npm" "$(npm --version)"
          restic version
          python --version
        '';
      };

      formatter = pkgs.alejandra;
    });
}
