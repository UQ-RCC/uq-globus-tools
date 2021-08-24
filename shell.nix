{ pkgs ? (import <nixpkgs> {}), stdenv ? pkgs.stdenv }:
let
  # Match the version on CentOS8
  xlibsepol = pkgs.libsepol.overrideDerivation(old: rec {
    inherit (old) se_url;
    se_release = "20190315";
    version    = "2.9";

    src = pkgs.fetchurl {
      url = "${se_url}/${se_release}/libsepol-${version}.tar.gz";
      sha256 = "0p8x7w73jn1nysx1d7416wqrhbi0r6isrjxib7jf68fi72q14jx3";
    };

  });
in
stdenv.mkDerivation {
  pname   = "uq-globus-tools-devshell";
  version = "1.0.0";

  nativeBuildInputs = with pkgs; [
    fakeroot
    rpm
    gnumake
    python3
    file
    (checkpolicy.override { libsepol = xlibsepol; })
    semodule-utils
  ];
}
