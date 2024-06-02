# shell.nix

{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "python3.10-environment";

  buildInputs = [
    (pkgs.python310)
    (pkgs.git)
    (pkgs.python310Packages.pygame)
    (pkgs.python310Packages.numpy)
    (pkgs.python310Packages.scipy)
  ];
}
