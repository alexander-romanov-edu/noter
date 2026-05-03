{
  description = "Gym Tracker";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    { flake-parts, treefmt-nix, ... }@inputs:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ treefmt-nix.flakeModule ];

      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem =
        { pkgs, ... }: let
          python = pkgs.python313;

          pythonEnv = python.withPackages (ps: with ps; [
            fastapi
            uvicorn
            sqlalchemy
            pydantic
            passlib
            bcrypt
            python-jose
            pytest
            httpx
            typing-extensions
          ]);
        in {
          imports = [ ./nix/treefmt.nix ];

          devShells.default = pkgs.mkShell {
            nativeBuildInputs = with pkgs; [ act ];
            buildInputs = with pkgs; [
            pythonEnv
            ];
          };
          apps.default = {
            type = "app";
            program = "${pkgs.writeShellScript "noter" ''
              uvicorn main:app --host 127.0.0.1 --reload
            ''}";
          };
        };
    };
}
