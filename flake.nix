{
  description = "Create Nix development environment";

  # Python 3.12.1 release
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/fd04bea4cbf76f86f244b9e2549fca066db8ddff";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  inputs.pyproject-nix.url = "github:nix-community/pyproject.nix";
  # Don't use the pyproject.nix flake directly to avoid its inputs in our
  # closure.
  inputs.pyproject-nix.flake = false;

  outputs = { self, nixpkgs, flake-utils, pyproject-nix  }:
    let
      pyproject = import (pyproject-nix + "/lib") { inherit (nixpkgs) lib; };

      # Load/parse dev_requirements.txt
      project = pyproject.project.loadRequirementsTxt {
        requirements = ./dev_requirements.txt;
      };

    in
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python312;

      pythonEnv = (
          # Render requirements.txt into a Python withPackages environment.
          pkgs.python3.withPackages (pyproject.renderers.withPackages {
            inherit project python;
          })
        );
    in
    {
      devShell =
        pkgs.mkShell {
          packages = [
            pythonEnv
          ];
          shellHook = ''
            python --version
          '';
        };
    });
}
