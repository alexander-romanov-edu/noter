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
        { pkgs, ... }:
        {
          imports = [ ./nix/treefmt.nix ];

          devShells.default = pkgs.mkShell {
            nativeBuildInputs = with pkgs; [ act ];
            buildInputs = with pkgs; [
              (python3.withPackages (
                ps: with ps; [
                  django
                  psycopg2
                  pylint-django
                  pip
                  sqlite
                ]
              ))
              poetry
              black
              ruff
            ];
          };
          apps.default = {
            type = "app";
            program = "${pkgs.writeShellScript "run-django" ''
              export PYTHONPATH=$PWD

              PYTHON=${
                (pkgs.python3.withPackages (
                  ps: with ps; [
                    django
                    psycopg2
                  ]
                ))
              }/bin/python

              $PYTHON $PWD/gym_tracker/manage.py migrate
              $PYTHON $PWD/gym_tracker/manage.py runserver 0.0.0.0:8000
            ''}";
          };
        };
    };
}
