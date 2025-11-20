{
  description = "Create Nix development environment";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";

    # 3.12.1
    python-nixpkgs.url = "github:NixOS/nixpkgs/fd04bea4cbf76f86f244b9e2549fca066db8ddff";

    # 20.6.1
    nodejs-nixpkgs.url = "github:NixOS/nixpkgs/78058d810644f5ed276804ce7ea9e82d92bee293";

    # 0.18.1
    restic-nixpkgs.url = "github:NixOS/nixpkgs/01b6809f7f9d1183a2b3e081f0a1e6f8f415cb09";

    # 0.9.7
    uv-nixpkgs.url = "github:NixOS/nixpkgs/1d4c88323ac36805d09657d13a5273aea1b34f0c";
  };

  outputs = {
    self,
    flake-utils,
    python-nixpkgs,
    nodejs-nixpkgs,
    restic-nixpkgs,
    uv-nixpkgs,
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = python-nixpkgs.legacyPackages.${system};
      python = pkgs.python312;
      nodejs = nodejs-nixpkgs.legacyPackages.${system}.nodejs_20;
      restic = restic-nixpkgs.legacyPackages.${system}.restic;
      uv = uv-nixpkgs.legacyPackages.${system}.uv;
    in {
      devShells.default = pkgs.mkShell {
        packages = [
          python
          nodejs
          restic
          uv
        ];
        shellHook = ''
          echo "node" "$(node --version)"
          echo "npm" "$(npm --version)"
          restic version
          uv --version
          python --version
        '';
      };

      formatter = pkgs.alejandra;
    });
}
