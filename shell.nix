let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
      (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
        pygame
        numpy
        sympy
        numba
        anywidget
        (
          buildPythonPackage rec {
            pname = "kingdon";
            version = "1.3.1";
            src = fetchPypi {
              inherit pname version;
              sha256 = "sha256-5jNVXoUmkl/80vQdt3TKCnICbCcaHJSJfm/9smmj/mU=";
            };
            doCheck = false;
          }
        )
      ]))
      pkgs.graphviz
      pkgs.typst
    ];
}
