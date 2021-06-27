{ pkgs ? (import <nixpkgs> {}), stdenv ? pkgs.stdenv }:
stdenv.mkDerivation {
  pname   = "uq-globus-tools-devshell";
  version = "1.0.0";

  nativeBuildInputs = with pkgs; [ rpm gnumake ];
}
