{
  description = "Create Nix development environment";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";

    # 3.12.1 release
    python-nixpkgs.url = "github:NixOS/nixpkgs/fd04bea4cbf76f86f244b9e2549fca066db8ddff";

    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      flake = false;
    };
  };

  outputs = {
    self,
    flake-utils,
    python-nixpkgs,
    pyproject-nix,
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = python-nixpkgs.legacyPackages.${system};
      python = pkgs.python312;
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
        ];
        shellHook = ''
          python --version
        '';
      };

      formatter = pkgs.alejandra;
    });
}
